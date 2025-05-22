from flask import Flask
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app_id = os.environ["app_id"]
app = Flask(__name__)

baseurl = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols=GBP,EUR,AED,CAD"

response = requests.get(baseurl)

if response.status_code == 200:
    data = response.json()
else:
    data = "no data"   



@app.route("/")
def home():
    return str(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)