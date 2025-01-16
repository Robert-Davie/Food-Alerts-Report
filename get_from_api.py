import requests
import json
import sqlite3
import time

conn = sqlite3.connect("food_alerts.db")
cursor = conn.cursor()

def insert_from_api(json_file):
    for item in json_file["items"]:
        current_item = item
        business = ""
        try:
            business = current_item["reportingBusiness"]["commonName"]
        except KeyError:
            pass

        pathogen = ""
        try:
            pathogen = current_item["problem"][0]["pathogenRisk"]["pathogen"]
        except KeyError:
            pass

        type_of_incident = ""
        try:
            type_of_incident = current_item["type"][1].split("/")[-1]
        except KeyError:
            pass

        date = ""
        try:
            date = current_item["created"]
        except KeyError:
            pass

        allergen = ""
        try:
            allergen = current_item["problem"][0]["allergen"][0]["label"]
        except KeyError as e:
            pass

        products_affected = ""
        try:
            products_affected = len(current_item["productDetails"])
        except KeyError:
            pass

        risk_statement = ""
        try:
            risk_statement = current_item["problem"][0]["riskStatement"]
        except KeyError:
            pass

        conn.execute("""
            INSERT INTO food_alerts (
                entry, 
                type, 
                date, 
                business, 
                pathogen, 
                allergen, 
                risk_statement, 
                number_products_affected, 
                is_published
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
        current_item["@id"],
        type_of_incident,
        date,
        business,
        pathogen,
        allergen,
        risk_statement,
        products_affected,
        current_item["status"]["label"] == "Published"
    ))

PAGE_LENGTH = 100
counter = 0
number_of_repsonses = -1
while counter < 2000 and number_of_repsonses != 0:
    base_url = "https://data.food.gov.uk/food-alerts"
    response = requests.get(f"{base_url}/id?_limit=100&_offset={counter}&_view=full", headers={"Accept": "application/json"})
    r = response.json()
    insert_from_api(r)
    number_of_repsonses = len(r["items"])
    counter += 100
    time.sleep(1)
    print(counter)


conn.commit()
conn.close()