# G9T5-ParkHub
An app that lets users find and compare parking options based on real-time lot availability, rates and location, view nearby amenities, and notifies users nearing their end time.

# Prerequisites

Run Wampserver before starting on the scenario set-ups.

Run docker compose up --build and python app.py on two separate CMD windows. Once the flask app is served on your server, click on the link and include /views in the URL.

Import ura_rates.sql, user.sql, and session.sql into localhost/phpmyadmin on user:root and password:"".

Create new .env file and make sure to create API_URL = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details', and your own API_KEY and API_TOKEN generated from URA API, and USER_AGENT = 'PostmanRuntime/7.36.3' and COOKIE = '__nxquid=HOIH8mjcscbjbYyu/M4fhlrXabqh+A==0014'

Also, create your own API keys for Twilio SMS service and update .env with these variables: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN

Note that some of these tokens change daily.

# Scenario 1
To run the search:
1. Import ura_rates.sql into phpmyadmin.
2. Next, Run the insert_db_ura script in terminal by typing 'python insert_db_ura.py'. Then, type localhost:5070/ura_rates in your browser. 
3. Due to the limitations of the URA API, certain places will not return nearby carparks, as URA carparks are limited to certain locations. To get results, use locations in the search bar such as - Pasir Panjang Food Centre, East Coast Lagoon Food Village, nus engineering e4, tanjong pagar singapore, lower kent ridge nus.


# Scenario 2
1. Make sure scenario 1 is completed (car park is selected), or there will be redirection back to search car parks.
2. Select respective radio button filter and click 'Search Amenities' button, selected filtered location results wil be shown in the form of cards, showing the place photo, place type, place name, and place address
   
# Scenario 3
1. Change 'from' phone number (line 41) in notification.py to your Twilio phone number
2. After running docker compose up --build and python app.py, go to http://localhost:8000/views
3. Login to ParkHub that has the receiving phone number registered with Twilio
4. Follow Scenario 1 to create a new parking session record (allow notifications for the session) that ends within the next 15 minutes to test the notification function
5. To test notification: 1. Wait for the batch job to be executed again (every 5 minutes) or 2. Go to http://localhost:5100/monitor_session to manually trigger the check for ending parking sessions
6. After receiving the SMS, follow the link to extend end time (due to limitations, please open the link on your computer browser instead of on your mobile)

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
