import requests
from flight_data import FlightData
import os

TEQUILA_API_KEY = os.environ['APIKEY']
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"


class FlightSearch:
    def get_iata_codes(self, city):
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        parameters = {
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=headers, params=parameters)
        data = response.json()['locations']
        code = data[0]['code']
        return code

    def get_flight(self, fly_from, fly_to, date_from, date_to):
        global flight_data
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "USD",
            "max_stopovers": 0
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=params)
        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f"There is no direct flight to {fly_to}.")
            params['max_stopovers'] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=params)
            trip_data = response.json()['data'][0]
            flight_data = FlightData(price=trip_data['price'],
                                     origin_city=trip_data['route'][0]['cityFrom'],
                                     origin_airport=fly_from,
                                     destination_city=trip_data['route'][1]['cityTo'],
                                     destination_airport=trip_data['route'][1]['flyTo'],
                                     departure_date=trip_data['route'][0]['local_departure'].split("T")[0],
                                     return_date=trip_data['route'][1]['local_departure'].split("T")[0],
                                     stopovers=1,
                                     via_city=trip_data['route'][0]['cityTo']
                                     )
                                     
        else:
            flight_data = FlightData(price=data['price'],
                                     origin_city=data['route'][0]['cityFrom'],
                                     origin_airport=data['route'][0]['flyFrom'],
                                     destination_city=data['route'][0]['cityTo'],
                                     destination_airport=data['route'][0]['flyTo'],
                                     departure_date=data['route'][0]['local_departure'].split("T")[0],
                                     return_date=data['route'][1]['local_departure'].split("T")[0],
                                     )
        finally:
            return flight_data
