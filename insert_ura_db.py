import requests
from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("dbURL") or "mysql+mysqlconnector://root@localhost:3306/ura_rates"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True


class UraRates(db.Model):
    __tablename__ = 'ura_rates'
    id = db.Column(db.Integer, primary_key=True)
    ppCode = db.Column(db.String(20))
    ppName = db.Column(db.String(255))
    weekdayMin = db.Column(db.String(20))
    weekdayRate = db.Column(db.DECIMAL(10, 2))
    satdayMin = db.Column(db.String(20))
    satdayRate = db.Column(db.DECIMAL(10, 2))
    sunPHMin = db.Column(db.String(20))
    sunPHRate = db.Column(db.DECIMAL(10, 2))
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)

api_url = os.environ.get("API_URL")
api_key = os.environ.get("API_KEY")
token = os.environ.get("API_TOKEN")
user_agent = os.environ.get("USER_AGENT")
cookie = os.environ.get("COOKIE")
print(api_key)

@app.route('/ura_rates')
def fetch_and_insert_data():
    raw_data = fetch_data_from_api(api_url, api_key, token,user_agent, cookie)
    
    if raw_data and 'Result' in raw_data:
        cleaned_data = [remove_geometries(carpark) for carpark in raw_data['Result']]
        preprocessed_data = [preprocess_data(carpark) for carpark in cleaned_data]
        
        try:
            for carpark in preprocessed_data:
                if carpark['weekdayRate'] > 0 and carpark['satdayRate'] > 0 and carpark['sunPHRate'] > 0:
                    new_rate = UraRates(**carpark)
                    db.session.add(new_rate)
                # else:
                #     print("Skipped insertion due to a rate being 0:", carpark)
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()
            
        return 'Data fetched and inserted successfully!'
    else:
        return 'Failed to fetch data or no data available', 400


# Function to fetch data from API
def fetch_data_from_api(api_url, api_key, token,user_agent, cookie):
    headers = {
        'AccessKey': api_key,
        'Token': token,
        'User-Agent': user_agent,
        'Cookie': cookie,
        'Connection': "keep-alive"
    }
    response = requests.get(api_url, headers=headers,allow_redirects=True)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: HTTP status code {response.status_code}")
            return None
    except ValueError as e:
        # The response body does not contain valid JSON
        print(f"Error decoding JSON: {e}")
        print(f"Response Content: {response.text}")
        return None
    
def remove_geometries(carpark):
    # Create a copy of the carpark dictionary without the 'geometries' key
    carpark_copy = {key: value for key, value in carpark.items() if key != 'geometries'}
    return carpark_copy

def preprocess_data(carpark):
    def parse_minutes(min_string):
        return int(min_string.split(' ')[0])

    def parse_rate(rate_string):
        return float(rate_string.replace('$', ''))

    def convert_time(time_string):
        return datetime.strptime(time_string, "%I.%M %p").strftime("%H:%M")

    preprocessed = {}

    preprocessed = {
        'ppCode': carpark.get('ppCode'),
        'ppName': carpark.get('ppName'),
        'weekdayMin': parse_minutes(carpark.get('weekdayMin', '0 mins')),
        'weekdayRate': parse_rate(carpark.get('weekdayRate', '$0.00')),
        'satdayMin': parse_minutes(carpark.get('satdayMin', '0 mins')),
        'satdayRate': parse_rate(carpark.get('satdayRate', '$0.00')),
        'sunPHMin': parse_minutes(carpark.get('sunPHMin', '0 mins')),
        'sunPHRate': parse_rate(carpark.get('sunPHRate', '$0.00')),
        'startTime': convert_time(carpark.get('startTime', '00:00 AM')),
        'endTime': convert_time(carpark.get('endTime', '00:00 AM'))
    }

    return preprocessed
    
if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5013, debug=True)
