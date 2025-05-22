from flask import Flask
import requests
import os
from dotenv import load_dotenv

# Only load .env file when running locally (i.e., not on GitHub Actions)
if os.getenv('FLASK_ENV') != 'production':  # Adjust this condition based on your setup
    load_dotenv()

# Retrieve the `APP_ID` from environment variables (either GitHub Secrets or .env)
app_id = os.getenv('app_id')  # This will work with both GitHub Secrets or .env

if not app_id:
    raise ValueError("Aapp_idis required but not set in environment variables.")

#app_id = os.environ["app_id"]
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