import os
from datetime import datetime, timezone
from collections import deque
from flask import Flask, request, render_template
from dotenv import load_dotenv
from flask import g
from models.models import db, Country
from utils.currency_logging import log_event
from currency.client import CurrencyClient



# Only load .env file when running locally (i.e., not on GitHub Actions)
if os.getenv('FLASK_ENV') != 'production':  # Adjust this condition based on your setup
    load_dotenv()

app = Flask(__name__)

# Retrieve the `APP_ID` from environment variables (either GitHub Secrets or .env)
app_id = os.getenv('app_id')  # This will work with both GitHub Secrets or .env
pg_password= os.getenv("pg_password")
pg_user=os.getenv('pg_user')
pg_ip=os.getenv('pg_ip')
DATABASE_URL= f"postgresql://{pg_user}:{pg_password}@{pg_ip}/currency_logs"

conversion_history = deque(maxlen=10) 

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # optional, suppresses warnings
db.init_app(app)

def get_countries():
    if 'countries' not in g:
        try:
            g.countries = Country.query.order_by(Country.name).all()
        except Exception as e:
            app.logger.warning(f"Could not retrieve countries: {e}")
            g.countries = []
    return g.countries


# Initialize client and get currency list
with app.app_context():
    client = CurrencyClient(app_id)
#client.get_currency_choices()

@app.before_request
def log_visit():
    """log user visits to page /"""
    if request.method == "GET":
        log_event(event_type="visit")

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Clean up the database session after each request."""
    db.session.remove()


def main():
    """This is an api test function it is run wehn code is uploaded to github to test logic not for users"""    
    API = CurrencyClient(app_id)
    API.get_currency_choices()
    base = "GBP"
    assert base in API.currency_choices.keys(), "base currency not found in currency choices"
    base_label = API.currency_choices[base]
    target = "NZD"
    assert target in API.currency_choices.keys(), "target currency not found in currency choices"
    target_label = API.currency_choices[target]
    value = 5000
    assert isinstance(value, (int, float, complex)), "Variable is not numeric!"
    API.set_base_currency(base)
    API.set_target_currency(target)
    API.set_base_value(value)
    data = API.calculate()
    print(f"{API.base_value} {base_label} is {data} {target_label}")


@app.route("/test")
def test_route():
    print("Test route accessed")
    return "Test successful"


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Renders the currency converter form and handles form submissions.

    - On GET: Displays the form for selecting base/target currencies and entering an amount.
    - On POST: Processes the form data, performs the currency conversion using the API, 
      and displays the result or any error that occurs.

    Returns:
        A rendered HTML page (index.html) with the conversion form, result, and optional error message.
    """
    result = None
    error = None
    #currencies = client.currency_choices
    #flags = client.currency_flags
    # Use database for dropdown labels and flags
    countries = get_countries()
    currency_options = [
        {
            "code": c.currency_code,
            "label": f"{c.name} {c.currency_name} ({c.currency_code})",
            "flag": c.flag
        }
        for c in countries
    ]

    flags = {c.currency_code: c.flag for c in countries}

    if request.method == "POST":
        try:
            base = request.form["base_currency"]
            target = request.form["target_currency"]
            value = float(request.form["amount"])
            client.set_base_currency(base)
            client.set_target_currency(target)
            client.set_base_value(value)
            converted=client.calculate()
            result = f"{value} {client.base_currency} is {converted} {client.target_currency}"
            #log events
            
            try:
                log_event(
                    event_type="conversion",
                    base=base,
                    target=target,
                    amount=value,
                    result=converted
                )
            except Exception:
                 error = "⚠️ We were unable to log your activity, but your conversion was successful."

            # Save query to history
            conversion_history.appendleft({
                "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "base": base,
                "target": target,
                "amount": value,
                "result": result
            })

        # clean up the exceptions needed 
        except Exception as e:
            error = str(e)

    return render_template("index.html", currencies=currency_options, flags=flags, result=result, error=error, history=conversion_history)
@app.route("/flag-preview", methods=["POST"])
def flag_preview():
    code = request.form.get("base_currency", "USD")
    country = next((c for c in get_countries() if c.currency_code == code), None)
    flags = client.currency_flags
    flag = flags.get(code, "")
    if country:
        label = f"{country.name} {country.currency_name}"
    else:
        label = f"Unknown ({code})"
    return render_template("partials/flag_preview.html", code=code, name=label, flag=flag)
@app.route("/target-flag-preview", methods=["POST"])
def target_flag_preview():
    code = request.form.get("target_currency", "EUR")
    country = next((c for c in get_countries() if c.currency_code == code), None)
    flags = client.currency_flags
    code = request.form.get("target_currency", "EUR")
    flag = flags.get(code, "")
    if country:
        label = f"{country.name} {country.currency_name}"
    
    else:
        label = f"Unknown ({code})"
    
    return render_template("partials/flag_preview.html", code=code, name=label, flag=flag)



if __name__ == "__main__":
 
    if os.getenv('FLASK_ENV') == 'production':
        main()
    else:
        app.run(debug=True, port=5001)