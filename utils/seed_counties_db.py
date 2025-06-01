# seed_countries.py
import os
import json
import base64
from flask import Flask
from models import db, Country

app = Flask(__name__)

# Configure your PostgreSQL URI
pg_password = os.getenv("pg_password")
pg_user = os.getenv("pg_user")
pg_ip = os.getenv("pg_ip")
DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_ip}/currency_logs"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)

with app.app_context():
    db.create_all()  # Ensures the countries table exists

    with open('templates/countries.json', 'r', encoding='utf-8') as f:
        countries_data = json.load(f)

    for country in countries_data:
        name = country['name']
        iso_alpha2 = country['isoAlpha2']
        currency_code = country['currency']['code']
        currency_name = country['currency']['name']
        currency_symbol = country['currency']['symbol']
        flag_base64 = country['flag']
        flag_data = base64.b64decode(flag_base64.split(',')[0])

        # Avoid duplicates (optional)
        if not Country.query.filter_by(iso_alpha2=iso_alpha2).first():
            db.session.add(Country(
                name=name,
                iso_alpha2=iso_alpha2,
                currency_code=currency_code,
                currency_name=currency_name,
                currency_symbol=currency_symbol,
                flag=flag_data
            ))
    
    db.session.commit()
    print("Countries imported into PostgreSQL.")
