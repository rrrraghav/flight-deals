import os
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()

iata_codes = [city['iataCode'] for city in sheet_data]
if '' in iata_codes:
    for row in sheet_data:
        row['iataCode'] = flight_search.get_iata_codes(row['city'])
    sheet_data = data_manager.flight_data
    data_manager.put_iata_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_later = tomorrow + timedelta(days=180)

mailing_list = data_manager.get_emails()
fly_from = os.environ['HOMEAIRPORT']

for email in mailing_list:
    index = mailing_list.index(email)
    for destination in sheet_data:
        flight = flight_search.get_flight(fly_from=fly_from, fly_to=destination['iataCode'],
                                          date_from=tomorrow.strftime("%d/%m/%Y"),
                                          date_to=six_months_later.strftime("%d/%m/%Y"))
        try:
            if flight.price < destination['lowestPrice']:
                data_manager.change_price(flight.price, destination['id'])
                print(f"{destination['city']}: ${flight.price}")
                if flight.stopovers == 0:
                    notification_manager = NotificationManager(email=email,
                                                               message=f"Subject: Low price alert!\n\n"
                                                                       f"Only ${flight.price} to fly from "
                                                                       f"{flight.origin_city}-{flight.origin_airport}"
                                                                       f" to "
                                                                       f"{flight.destination_city}-"
                                                                       f"{flight.destination_airport}"
                                                                       f", from "
                                                                       f"{flight.departure_date}"
                                                                       f" to {flight.return_date}.")
                else:
                    notification_manager = NotificationManager(email=email,
                                                               message=f"Subject: Low price alert!\n\n"
                                                                       f"Only ${flight.price} to fly from "
                                                                       f"{flight.origin_city}-{flight.origin_airport}"
                                                                       f" to "
                                                                       f"{flight.destination_city}-"
                                                                       f"{flight.destination_airport}"
                                                                       f", from "
                                                                       f"{flight.departure_date} to "
                                                                       f"{flight.return_date}."
                                                                       f"Flight has {flight.stopovers} stopover, "
                                                                       f"via {flight.via_city}")
                notification_manager.send_message()
            else:
                print(f"{destination['city']}: ${destination['lowestPrice']}")
        except AttributeError:
            pass
