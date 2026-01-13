import requests
import os
from twilio.rest import Client

API_KEY = os.environ.get("API_KEY")
LAT = 123
LON = 123
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

parameters = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()
print(data)

will_rain = False
for item in data["list"]:
    weather = item["weather"][0]["id"]
    if int(weather) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella.",
        from="+number",
        to="+number"
    )
