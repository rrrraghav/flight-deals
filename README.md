# flight-deals
Finds the cheapest flight deals available from a given airport and emails the user with details.


How It Works

- The project uses the Tequila Flight Search API to find flights that are available from a given location to select locations for the next six months.
- It then compares the prices of these flights to the flight prices already stored.
- If a flight deal is found below the previous lowest price, then the user is sent an email with the details of the flight.


Configuration

Before running the project, you need to configure the following settings:

- Email Configuration: Provide your email server details (SMTP), including your email address and password for sending flight deal notifications.
- API Configurations: This project uses the Sheety API to store data such as the airport and a flight's price as well as user data. It also uses the Tequila Flight Search API to find deals. For the code to run smoothly, you will need to get access to both of these APIs.
- Data Settings: All data is stored in a Google Sheet. It must have 2 sheets: 'prices' and 'users'. The prices sheet needs 3 columns: 'City' (the city you want to travel to), 'IATA Code' (the IATA code for the city's airport), and 'Lowest Price' (to start, you can just set this to $2000 for all cities). The users sheet needs 3 columns: 'First Name', 'Last Name' and 'Email'. This is so that you can send any deals to as many emails as you would like.
- Flight Search Settings: Specify the airport from which you want to find flight deals. In 'main.py', set the 'fly_from' variable to the IATA code of your home airport. 

