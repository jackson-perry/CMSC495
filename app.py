import os
from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv

# Only load .env file when running locally (i.e., not on GitHub Actions)
if os.getenv('FLASK_ENV') != 'production':  # Adjust this condition based on your setup
    load_dotenv()


class CurrencyClient:
    """this class makes the connection to the API and has methods to convert currencies"""
    def __init__(self, app_id):
        self.app_id = app_id
        self.currency_list_url= "https://openexchangerates.org/api/currencies.json"
        self.base_currency= "USD"
        self.target_currency= "EUR"
        self.currency_choices= {"USD": "US Dollaer", "EUR": "Euro"}
        self.base_value=0
    def set_base_value(self, value):
        """sets the base value for the currency being converted from"""
        self.base_value=value
    def get_currency_choices(self):
        """retrieves all the currency choices avaible at the endpoint"""
        response = requests.get(self.currency_list_url, timeout =8)
        if response.status_code ==200:
            data = response.json()
            self.currency_choices = data
        else:
            raise ValueError("Expected a JSON object (dict) from /currencies")
    def set_base_currency(self,base):
        """sets the base currency"""
        self.base_currency=base
    def set_target_currency(self,target):
        """sets teh target currency"""
        self.target_currency= target
   
   
#this is only allowing USD base at the free subscription consider:
        #UniRate
        #FxFeed.io
        #currencyAI
        #national Bank of Ploan as alternatives
    def calculate(self):
        """calcultes teh conversion currenly only wokring for USD base"""
        url=f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}&base={self.base_currency}&symbols={self.target_currency}&prettyprint=false&show_alternative=false"
        response = requests.get(url, timout =8)
        if response.status_code ==200:
            data =response.json()["rates"][self.target_currency]*self.base_value
            return data
        else:
            return response.status_code
            
    
# Retrieve the `APP_ID` from environment variables (either GitHub Secrets or .env)
app_id = os.getenv('app_id')  # This will work with both GitHub Secrets or .env

if not app_id:
    raise ValueError("Aapp_idis required but not set in environment variables.")

app_id = os.environ["app_id"]
app = Flask(__name__)


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



# Initialize client and get currency list
client = CurrencyClient(app_id)
client.get_currency_choices()

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

    if request.method == "POST":
        try:
            base = request.form["base_currency"]
            target = request.form["target_currency"]
            value = float(request.form["amount"])

            client.set_base_currency(base)
            client.set_target_currency(target)
            client.set_base_value(value)
            result = f"{value} {client.base_currency} is {client.calculate()} {client.target_currency}"
        # clean up the exceptions needed 
        except Exception as e:
            error = str(e)

    return render_template("index.html", currencies=client.currency_choices, result=result, error=error)



if __name__ == "__main__":
 
    if os.getenv('FLASK_ENV') == 'production':
        main()
    else:
        app.run(debug=True, port=5001)