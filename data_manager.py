import requests
import os

SHEETY_HEADER = os.environ['HEADER']
SHEETY_ENDPOINT = "https://api.sheety.co/1caa3acfb549ef4ee6a4f3723d79b708/lowestFlightPrices/"
HEADERS = {
    "Authorization": SHEETY_HEADER,
}


class DataManager:
    def __init__(self):
        self.flight_data = {}
        self.emails = []
        self.home_airports = []

    def get_data(self):
        response = requests.get(url=f'{SHEETY_ENDPOINT}prices', headers=HEADERS)
        data = response.json()
        self.flight_data = data['prices']
        return self.flight_data

    def put_iata_codes(self):
        for city in self.flight_data:
            city_id = city['id']
            new_codes = {
                'price': {
                    "iataCode": city['iataCode']
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}prices/{city_id}", json=new_codes, headers=HEADERS)

    def add_city(self, city):
        city = {
            'price': {
                'city': city.title(),
                'lowestPrice': 2000
            }
        }
        response = requests.post(url=f'{SHEETY_ENDPOINT}prices', json=city, headers=HEADERS)

    def change_price(self, price, city_id):
        params = {
            'price': {
                'lowestPrice': price,
            }
        }
        response = requests.put(url=f"{SHEETY_ENDPOINT}prices/{city_id}", json=params, headers=HEADERS)

    def get_emails(self):
        response = requests.get(url=f'{SHEETY_ENDPOINT}users', headers=HEADERS)
        data = response.json()['users']
        for user in data:
            email = user['email']
            self.emails.append(email)
        return self.emails
