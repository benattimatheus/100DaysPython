import requests
import os
from datetime import datetime

APP_ID = os.environ["SHEETY_ID"]
API_KEY = os.environ["SHEETY_API_KEY"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
exercise_endpoint = os.environ["EXERCISE_ENDPOINT"]
sheet_endpoint = os.environ["SHEETY_SHEET"]

headers_exercise = {
    "x-app-key": API_KEY,
    "x-app-id": APP_ID,
}

data_exercise = {
    "query": input("Tell me which exercises you did:\n")
}

response_exercise = requests.post(exercise_endpoint, headers=headers_exercise, json=data_exercise)
result_exercise = response_exercise.json()
# print(result_exercise)
# print(result_exercise["exercises"][0]["name"])

today = datetime.now()

sheet_header = {
    "Authorization": f"Bearer {SHEETY_TOKEN}",
}

data_sheet = {
    "workout": {
        "date": today.strftime("%d/%m/%Y"),
        "time": today.strftime("%H:%M:%S"),
        "exercise": result_exercise["exercises"][0]["name"].title(),
        "duration": result_exercise["exercises"][0]["duration_min"],
        "calories": result_exercise["exercises"][0]["nf_calories"],
    }
}

response_sheet = requests.post(sheet_endpoint, json=data_sheet,headers=sheet_header)
print(response_sheet.text)

rows = requests.get(sheet_endpoint, headers=sheet_header).json()
print(rows)