from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys, requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

nearby_amenities_wrapper_url = 'http://nearby_amenities_wrapper:5011/nearby_amenities_request'


@app.route("/search_amenities", methods=['POST', 'GET'])
def search_amenities():
    data = request.json
    # print(data)
    selectedFilters = data.get('selectedFilters')
    userID = data.get('userID')
    # print(userID)

    #location
    session_getlocation_url=f'http://session:5006/session/location/{userID}'
    location_result = invoke_http(session_getlocation_url, method='GET')
    latitude = location_result['data']['latitude']
    longitude = location_result['data']['longitude']

    # Package the data into JSON
    payload = {
        'selectedFilters': selectedFilters,
        'latitude': latitude,
        'longitude': longitude
    }
    
    print(payload)
    response = invoke_http(nearby_amenities_wrapper_url, method='POST', json=payload)

    print(response)

    return jsonify(response)




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
    app.run(host='0.0.0.0', port=5012, debug=True)
