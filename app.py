import os
import base64
from datetime import datetime, timezone
from collections import deque
from flask import Flask, request, render_template
from dotenv import load_dotenv
from flask import g
from models.models import db, Country
from utils.currency_logging import log_event
from currency.client import CurrencyClient


def create_app(test_config=None):
    # Only load .env file when not in production
    if os.getenv('FLASK_ENV') != 'production':
        load_dotenv()

    app = Flask(__name__)
    
    # Load default or test config
    if test_config is None:
        app_id = os.getenv('app_id')
        pg_password = os.getenv("pg_password")
        pg_user = os.getenv('pg_user')
        pg_ip = os.getenv('pg_ip')
        DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_ip}/currency_logs"
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    else:
        app.config.update(test_config)
        app_id = test_config.get("APP_ID", "test")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    client = CurrencyClient(app_id)
    conversion_history = deque(maxlen=10)

    def get_countries():
        """retrieve and cache countries from database"""
        if 'countries' not in g:
            try:
                g.countries = Country.query.order_by(Country.name).all()
            except Exception as e:
                app.logger.warning(f"Could not retrieve countries: {e}")
                g.countries = []
        return g.countries


    @app.before_request
    def handle_before_request():
        """inital setup of client session before users pick anything"""
        if not hasattr(g, "_currency_preloaded"):
            try:
                client.get_currency_choices_from_db()
            except Exception as e:
                app.logger.warning(f"Failed to preload currency data: {e}")
            g._currency_preloaded = True

        if request.method == "GET" and request.path == "/":
            log_event(event_type="visit")


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Clean up the database session after each request."""
        db.session.remove()

    @app.route("/test")
    def test_route():
        """simple test route to see if server is up"""
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
        currency_client = client
        countries = get_countries()
        currency_options = [
            {
                "code": c.currency_code,
                "label": f"{c.name} {c.currency_name} ({c.currency_code})",
                "flag": c.flag
            }
            for c in countries
        ]

        flags = {
            c.currency_code: base64.b64encode(c.flag).decode("utf-8")
            for c in countries
    }


        if request.method == "POST":
            try:
                base = request.form["base_currency"]
                target = request.form["target_currency"]
                value = float(request.form["amount"])
                currency_client.set_base_currency(base)
                currency_client.set_target_currency(target)
                currency_client.set_base_value(value)
                converted=currency_client.calculate()
                result = f"{value} {currency_client.base_currency} is {converted} {currency_client.target_currency}"
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
        """create a flag icon for the source currencyfrom base64 encoded databse entry"""
        currency_client = client
        code = request.form.get("base_currency", "USD")
        country = next((c for c in get_countries() if c.currency_code == code), None)
        flags = currency_client.currency_flags
        flag = flags.get(code, "")
        if country:
            label = f"{country.name} {country.currency_name}"
        else:
            label = f"Unknown ({code})"
        return render_template("partials/flag_preview.html", code=code, name=label, flag=flag)
    @app.route("/target-flag-preview", methods=["POST"])

    def target_flag_preview():
        """create a flag icon for the target currencyfrom base64 encoded databse entry"""
        currency_client = client
        code = request.form.get("target_currency", "EUR")
        country = next((c for c in get_countries() if c.currency_code == code), None)
        flags = currency_client.currency_flags
        flag = flags.get(code, "")
        if country:
            label = f"{country.name} {country.currency_name}"
        
        else:
            label = f"Unknown ({code})"
        
        return render_template("partials/flag_preview.html", code=code, name=label, flag=flag)
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=5001)