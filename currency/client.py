# currency/client.py
import requests
import base64
from models.models import Country

class CurrencyClient:
    """this class makes the connection to the API and has methods to convert currencies"""
    def __init__(self, app_id):
        self.app_id = app_id
        self.currency_list_url= "https://openexchangerates.org/api/currencies.json"
        self.base_currency= "USD"
        self.target_currency= "EUR"
        self.currency_choices= {"USD": "US Dollar", "EUR": "Euro"}
        self.currency_flags={}
        self.base_value=0
        self.get_currency_choices_from_db()
    def set_base_value(self, value):
        """sets the base value for the currency being converted from"""
        self.base_value=value
    def get_currency_choices_from_db(self):
        """gets the currency choices from the PG db"""
        db_choices = {}
        for country in Country.query.all():
            flag_base64 = base64.b64encode(country.flag).decode('utf-8')
            db_choices[country.currency_code] = country.currency_name
            self.currency_flags[country.currency_code] = flag_base64 
        self.currency_choices=db_choices       
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
        """sets the target currency"""
        self.target_currency= target
    #this is only allowing USD base at the free subscription
    #fixed calls dollars to both currency and uses divison  
    def calculate(self):
        """calcultes the conversion currenly only working for USD base"""
        url=f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}&base=USD&symbols={self.base_currency},{self.target_currency}&prettyprint=false&show_alternative=false"
        response = requests.get(url, timeout =8)
        if response.status_code ==200:
            raw_data =response.json()
            data=(raw_data["rates"][self.target_currency]/raw_data["rates"][self.base_currency])*self.base_value
            return round(data,2)
        else:
            return response.status_code