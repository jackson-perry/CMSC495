from flask import Flask
import requests
import os
import json
from dotenv import load_dotenv

# Only load .env file when running locally (i.e., not on GitHub Actions)
if os.getenv('FLASK_ENV') != 'production':  # Adjust this condition based on your setup
    load_dotenv()


class CurrencyClient:
    def __init__(self, app_id):
        self.app_id = app_id
        self.currencyListUrl= "https://openexchangerates.org/api/currencies.json"
        self.baseCurrency= "USD"
        self.targetCurrency= "EUR"
        self.currencyChoices= {"USD": "US Dollaer", "EUR": "Euro"}
        self.baseValue=0
    def setBaseValue(self, value):
        self.baseValue=value
    def getCurrencyChoices(self):
        response = requests.get(self.currencyListUrl)
        if response.status_code ==200:
            data = response.json
            self.currencyChoices = data
        else:
            raise ValueError("Expected a JSON object (dict) from /currencies")
    def setBaseCurrency(self,base):
        self.baseCurrency=base
    def setTargetCurrency(self,target):
        self.targetCurrency= target
    def calculate(self):
        url=f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}&symbols={self.targetCurrency}&base={self.baseCurrency}"
        response = requests.get(url)
        if response.status_code ==200:
            data =response.json()["rates"][self.targetCurrency]*self.baseValue
            return data
        else:
            return 0
            
    
# Retrieve the `APP_ID` from environment variables (either GitHub Secrets or .env)
app_id = os.getenv('app_id')  # This will work with both GitHub Secrets or .env

if not app_id:
    raise ValueError("Aapp_idis required but not set in environment variables.")

#app_id = os.environ["app_id"]
app = Flask(__name__)

def main():
    API = CurrencyClient(app_id)
    API.setBaseCurrency("USD")
    API.setTargetCurrency("GBP")
    API.setBaseValue(50)
    data = API.calculate()
    print(data)



@app.route("/")
def home():

    return str(data)

if __name__ == "__main__":
  #  app.run(debug=True, port=5001)
    main()