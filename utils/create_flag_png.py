import sys
import os
import base64
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


with open("static/countries.json","r") as f:
    data=json.load(f)

for country in data:
    currency_code = country['currency']['code']
    flag_base64 = country['flag']
    image_data = base64.b64decode(flag_base64) 
    with open(f"static/{currency_code}.png", "wb") as png:
        png.write(image_data)