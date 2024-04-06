# G9T5-ParkHub
An app that lets users find and compare parking options based on real-time lot availability, rates and location, view nearby amenities, and notifies users nearing their end time.

# Prerequisites

Run wampserver before starting on the scenario set-ups.

Run docker compose up --build and python app.py on two separate CMD windows. Once the flask app is served on your server, click on the link and include /views in the URL.

Import ura_rates.sql, user.sql, and session.sql into localhost/phpmyadmin on user:root and password:"".

# Scenario 1
To run the search:
1. Import ura_rates.sql into phpmyadmin.
2. Change the token if you are inserting results in the database as it needs to be retrieved daily. Firstly,
   - call url https://www.ura.gov.sg/uraDataService/insertNewToken.action, with
     AccessKey Header in Postman : e61ff773-ba6b-4e89-aeda-759e0bc55604.
    - result of api call will be token.
    - In the .env file, replace the token (API_TOKEN) with your own token in the following lines of code in the file
    - api_url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details'
API_KEY = 'e61ff773-ba6b-4e89-aeda-759e0bc55604'
API_TOKEN = ****** replace your token here
USER AGENT = 'PostmanRuntime/7.36.3'
COOKIE = '__nxquid=HOIH8mjcscbjbYyu/M4fhlrXabqh+A==0014'
3. Next, Run the insert_db_ura script in terminal by typing 'python insert_db_ura.py'. Then, type localhost:5070/ura_rates in your browser. 
4. Due to the limitations of the URA API, certain places will not return nearby carparks, as URA carparks are limited to certain locations. To get results, use locations in the search bar such as - Pasir Panjang Food Centre, East Coast Lagoon Food Village, nus engineering e4, tanjong pagar singapore, lower kent ridge nus.


# Scenario 2
1. Make sure scenario 1 is completed (car park is selected), or there will be redirection back to search car parks.
2. Select respective radio button filter and click 'Search Amenities' button, selected filtered location results wil be shown in the form of cards, showing the place photo, place type, place name, and place address
   
# Scenario 3
1. Create new Twilio account
2. Update TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env file to your own
3. Change 'from' phone number (line 41) in notification.py to your Twilio phone number
4. After running docker compose up --build and python app.py, go to http://localhost:8000/views
5. Login to ParkHub that has the receiving phone number registered with Twilio
6. Follow Scenario 1 to create a new parking session record (allow notifications for the session) that ends within the next 15 minutes to test the notification function
7. To test notification: 1. Wait for the batch job to be executed again (every 5 minutes) or 2. Go to http://localhost:5100/monitor_session to manually trigger the check for ending parking sessions
8. After receiving the SMS, follow the link to extend end time (due to limitations, please open the link on your computer browser instead of on your mobile)

# PORTS
For dockerised microservices
1. session.py - 5006
2. googlewrapper.py - 5000
3. user.py - 5010
4. searchinfo.py - 5002
5. urawrapper_rates.py - 5003
6. ltawrapperlots.py  - 5001
7. monitor_session.py - 5100
8. searchAmenities.py - 5012
9. nearby_amenities_wrapper.py - 5011
10. rabbitmq - 5672 and 15672

Local Flask Apps (for front-end pages and insertion scripts, not microservices)
1. insert_ura_db.py - 5070
2. app.py - 8000
