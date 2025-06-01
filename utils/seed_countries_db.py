import os
import json
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.models import Country

# Configure your PostgreSQL URI
pg_password = os.getenv("pg_password")
pg_user = os.getenv("pg_user")
pg_ip = os.getenv("pg_ip")
DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_ip}/currency_logs"

# Create an engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session to interact with the DB
session = Session()

# Read the JSON data from the file
with open('templates/countries.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

# Iterate over each country in the JSON data
for country in countries_data:
    name = country['name']
    iso_alpha2 = country['isoAlpha2']
    currency_code = country['currency']['code']
    currency_name = country['currency']['name']
    currency_symbol = country['currency']['symbol']
    flag_base64 = country['flag']

    # Check if flag data exists and decode if it does
    flag_data = None
    if flag_base64:
        # If flag is a base64 string in the format "data:image/png;base64,..."
        if flag_base64.startswith("data:"):
            flag_data = base64.b64decode(flag_base64.split(',')[1])  # Get the data after the comma
        else:
            flag_data = base64.b64decode(flag_base64)  # Just decode the string directly
    
    # Avoid duplicates: Check if the country already exists
    existing_country = session.query(Country).filter_by(iso_alpha2=iso_alpha2).first()
    if not existing_country:
        # Create new Country instance
        new_country = Country(
            name=name,
            iso_alpha2=iso_alpha2,
            currency_code=currency_code,
            currency_name=currency_name,
            currency_symbol=currency_symbol,
            flag=flag_data
        )
        session.add(new_country)

# Commit the transaction once after processing all countries
session.commit()

# Close the session
session.close()

print("Countries imported into PostgreSQL.")

