from flask import Flask,request,jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/google_results',methods=['POST','GET'])
def make_google_request():
        
         coords_object=request.get_json()['value']
         print(coords_object)
         coords_lat=coords_object['lat']
    
         coords_lon=coords_object['lng']
         coords_str=str(coords_lat)+","+str(coords_lon)
        
         print(coords_str)
         url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius=2000&types=parking&sensor=false&key=AIzaSyBNWtyHG53pXtomi6KJL9ZH4Erituy6FNE".format(coords_str)
         response = requests.get(url)
         response.raise_for_status()
         response=response.json()
         print(response)
         return response












if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=False)
