import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self):
        self.sheet_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.sheet_header = {
            "Authorization": f"Bearer {os.getenv('SHEETY_BEARER')}",
        }
        self.destination_data = {}

    def get_data(self):
        response = requests.get(url=self.sheet_endpoint, headers=self.sheet_header)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_iata(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{self.sheet_endpoint}/{city['id']}", json=new_data,headers=self.sheet_header)
            print(response.text)