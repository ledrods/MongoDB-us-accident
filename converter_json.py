import json
import pandas as pd

# Caminho do JSON original
input_file = "us-accident.json"

# Carrega os dados
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

accidents = []
airports_dict = {}

for entry in data:
    # Cria ou atualiza aeroporto na coleção separada
    airport_code = entry["Airport_Code"]
    if airport_code not in airports_dict:
        airports_dict[airport_code] = {
            "_id": airport_code,
            "Name": entry["Airport_Name"],
            "Timezone": entry["Timezone"]
        }

    # Documento de acidente com dados incorporados (embed)
    accident_doc = {
        "_id": entry["Accident_ID"],
        "Severity": entry["Severity"],
        "Start_Time": entry["Start_Time"],
        "End_Time": entry["End_Time"],
        "Distance": entry["Distance"],
        "Description": entry["Accident_Description"],
        "Year": entry["Year"],
        "Weather": {
            "Timestamp": entry["Weather_Timestamp"],
            "Temperature": entry["Temperature"],
            "Humidity": entry["Humidity"],
            "Pressure": entry["Pressure"],
            "Visibility": entry["Visibility"],
            "Wind_Direction": entry["Wind_Direction"],
            "Wind_Speed": entry["Wind_Speed"],
            "Precipitation": entry["Precipitation"],
            "Condition": {
                "ID": entry["Weather_Condition_ID"],
                "Description": entry["Weather_Description"]
            },
            "Day_Period": {
                "Sunrise_Sunset": entry["Sunrise_Sunset"],
                "Civil_Twilight": entry["Civil_Twilight"],
                "Nautical_Twilight": entry["Nautical_Twilight"],
                "Astronomical_Twilight": entry["Astronomical_Twilight"]
            }
        },
        "Location": {
            "Street": entry["Street"],
            "City": entry["City"],
            "County": entry["County"],
            "State": entry["State"],
            "Zipcode": entry["Zipcode"],
            "Country": entry["Country"],
            "Airport_Code": airport_code  # referência
        },
        "Road_Features": {
            "Amenity": bool(entry["Amenity"]),
            "Bump": bool(entry["Bump"]),
            "Crossing": bool(entry["Crossing"]),
            "Give_Way": bool(entry["Give_Way"]),
            "Junction": bool(entry["Junction"]),
            "No_Exit": bool(entry["No_Exit"]),
            "Railway": bool(entry["Railway"]),
            "Roundabout": bool(entry["Roundabout"]),
            "Station": bool(entry["Station"]),
            "Stop": bool(entry["Stop"]),
            "Traffic_Calming": bool(entry["Traffic_Calming"]),
            "Traffic_Signal": bool(entry["Traffic_Signal"]),
            "Turning_Loop": bool(entry["Turning_Loop"])
        }
    }

    accidents.append(accident_doc)

# Salva os dois arquivos finais
with open("accidents_mongo.json", "w", encoding="utf-8") as f:
    json.dump(accidents, f, ensure_ascii=False, indent=2)

with open("airports_mongo.json", "w", encoding="utf-8") as f:
    json.dump(list(airports_dict.values()), f, ensure_ascii=False, indent=2)

print("Arquivos gerados com sucesso!")
