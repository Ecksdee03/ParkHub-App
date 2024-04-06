#5002 is the port for searchinfo microservice (complex)
from flask import Flask, request
import requests
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2
import json

app = Flask(__name__)
CORS(app)

# googlewrapper_url='http://localhost:5000/google_results'
ltawrapper_url='http://ltawrapper:5001/lta_results'
urawrapper_url='http://urawrapper:5003//ura_rates/'

#helper function to calculate distance between 2 points
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in meters (mean value)
    earth_radius = 6371000

    # Calculate the distance
    distance = earth_radius * c

    return distance

SUPPORTED_HTTP_METHODS = set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])

#helper function for http requests with get and post
def invoke_http(url, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            r = requests.request(method, url, json = json, **kwargs)
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300):
        return result

    ## Check http call result
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result



@app.route('/search_results', methods=['GET','POST'])
def processreturntopcarparks():
    #invoke googlewrapper function and return results
    results=request.get_json()
    print(results)
    google_response=invoke_http('http://googlewrapper:5000/google_results',method='POST',json=results)
    print(google_response)
    google_result=google_response['results']
    print(google_result)
    #invoke ltawrapperlots and return results
    lta_response=invoke_http(ltawrapper_url,method='GET')
    lta_carparks=lta_response['value']
    # print(lta_carparks)
    #invoke urawrapper_rates and return results
    
    #nested loop to match google and lta results. 
    
    #Some offset is needed here as both APIs return results around 20m away from each other. We use the helper function to match the results.
    results_list=[]
    for google_car_park in google_result:
        google_lat=google_car_park['geometry']['location']['lat']
        google_lon=google_car_park['geometry']['location']['lng']  
        carpark_name=google_car_park['name']
        # print(google_lat,google_lon)
        for lta_carpark in lta_carparks:    
        
          lta_coordinates=lta_carpark['Location']
          
          split_str=lta_coordinates.split()
          
          if len(split_str)>0:
             lta_lat=float(split_str[0])
             lta_lon=float(split_str[1])
          
             if(haversine_distance(google_lat,google_lon,lta_lat,lta_lon)<20) and lta_carpark['CarParkID'] not in results_list:
       
                results_list.append({'google_lat':google_lat,'carparkid':lta_carpark['CarParkID'],'google_lon':google_lon,'carpark_name':carpark_name,'lotsavailable':lta_carpark['AvailableLots']})

    for result in results_list:
       ura_response=invoke_http(urawrapper_url+result['carparkid'],method='GET')
       result['rates']=ura_response
    return json.dumps(results_list)
   
    



    





if __name__=='__main__':
    app.run(host='0.0.0.0', port=5002,debug=False)
