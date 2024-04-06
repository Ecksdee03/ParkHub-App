from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os
app = Flask(__name__)
CORS(app)


@app.route("/nearby_amenities_request", methods=['POST', 'GET']) #receive from search amenities
def nearby_amenities_request():
    data = request.get_json()
    # print(data)

    coords_lat=data['latitude']
    coords_lng=data['longitude']
    coords_str=str(coords_lat)+","+str(coords_lng)
    
    filters_str = data['selectedFilters']
    try:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius=2000&types={}&key=AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY".format(
            coords_str, filters_str)
        
        response = requests.get(url)
        response.raise_for_status()
        response_data=response.json()
       
        
        formatted_results = []
        for result in response_data.get('results', []):
            print(result)
            print()
            
            photo_url = ''
            if 'photos' in result:
                photo_reference = result['photos'][0].get('photo_reference', '')
                photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key=AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY".format(photo_reference)

                formatted_result = {    
                'name': result.get('name', ''),
                'type': ', '.join(result.get('types', [])),
                'address': result.get('vicinity', ''),
                'photo': photo_url
                }

                # print(formatted_result)
                formatted_results.append(formatted_result)

        # print(formatted_results, 11111111111)
        
        if not formatted_results:
            if filters_str == 'car_wash': 
                filters_str = 'Car Wash'
            elif filters_str == 'convenience_store':
                filters_str = 'Convenience Store'
            elif filters_str == 'gas_station':
                filters_str = 'Gas Station'
            
            message = f"No matching results found for: {filters_str}"
            return jsonify({'message': message}), 200

        return jsonify(formatted_results), 200  # Return formatted results as JSON
    
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return jsonify({'error': 'Failed to retrieve nearby amenities'}), 500




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
    app.run(host='0.0.0.0', port=5011, debug=True)

