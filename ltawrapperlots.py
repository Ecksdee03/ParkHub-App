from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

lta_url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"
custom_headers = {
    'AccountKey': 'kkFPEYubRJqbnVDK5CmanA==',
    'User-Agent': 'PostmanRuntime/7.28.4',
    'accept':'application/json'
    }




@app.route('/lta_results')
def make_get_request(lta_url=lta_url, headers=custom_headers):
        response = requests.get(lta_url, headers=headers)
        
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        response=response.json()
        values=[]
        for result in response['value']:
              if(result['Agency']=='URA' and result['LotType']=='C'):
                    values.append(result)
        return {"value":values}           
    






if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001,debug=False)
