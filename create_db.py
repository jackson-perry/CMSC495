import sqlite3
import json
import base64

# Load the countries data from the JSON file
# I used my local direct path to JSON file here so will need to be edited 
with open('C:\\Users\\erblo\\source\\repos\\CMSC495\\Project_Group1\\CMSC495\\templates\\countries.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

# Create a new SQLite database (or connect if it exists)
conn = sqlite3.connect('countries.db')
cursor = conn.cursor()

# Create a table to store country information
cursor.execute('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso_alpha2 TEXT NOT NULL,
    currency_name TEXT NOT NULL,
    currency_code TEXT NOT NULL,
    currency_symbol TEXT NOT NULL,
    flag BLOB NOT NULL
)
''')

# Insert country data into the database
for country in countries_data:
    name = country['name']
    iso_alpha2 = country['isoAlpha2']
    currency_code = country['currency']['code']
    currency_name = country['currency']['name']
    currency_symbol = country['currency']['symbol']
    flag_base64 = country['flag']
    flag_data = base64.b64decode(flag_base64.split(',')[0])  # Decode Base64 flag data

    cursor.execute('''
    INSERT INTO countries (name, iso_alpha2, currency_code, currency_name, currency_symbol, flag)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, iso_alpha2, currency_code, currency_name, currency_symbol, flag_data))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database populated with country information.")
