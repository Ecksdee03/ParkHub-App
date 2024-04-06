const apiKey = "AIzaSyDuWCAvENcOz861ihyW1EOF8WTJAzKfHfY"
if (sessionStorage.getItem('userID') == null){
    window.location.href = 'http://localhost:8000/views/login';
    };

console.log(sessionStorage.getItem('userID'));
function autocompleteInputFunction() {
    var input = document.getElementById("autocompleteInput")
    
    let autocomplete = new google.maps.places.Autocomplete(input)
}

autocompleteInputFunction()


// When form is submitted
document.getElementById('infoform').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission
    console.log(sessionStorage.getItem('userID'))
    // Get form data
    try{
    const location = document.getElementById('autocompleteInput').value;

    console.log(location)
    // Send data to microservice
    const coordinates = await getCoordsForAddress(location);
    console.log('Coordinates:', coordinates);

    const COORDINATES_JSON = JSON.stringify(coordinates);
    console.log(COORDINATES_JSON)
    
    } 
    catch (error) {
        console.error('Error:', error.message);
        // Handle the error
    }
});

async function getCoordsForAddress(address) {
    try {
        const response = await axios.get(
            `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${apiKey}`
        );

        const data = response.data;
        console.log(data);

        if (!data || data.status === 'ZERO_RESULTS') {
            throw new Error('Could not find location for the specified address.');
        }

        const coordinates = data.results[0].geometry.location;
        
        // Send the coordinates to the microservice using Axios
        const searchResultsResponse = await axios.post('http://localhost:5002/search_results', { value: coordinates });
        
        console.log('Search results:', searchResultsResponse.data);
        
        // Process the response data and update the HTML accordingly
        const carparkResults = searchResultsResponse.data;

        // Check if carparkResults array is empty
        if (carparkResults.length === 0) {
            document.getElementById('carparktopresults').innerHTML = '<p>No results found</p>';
        } else {
            let newHTML = '';

            // Generate HTML for each car park result
            for (const carpark of carparkResults) {
                newHTML += `
                    <div class="flex justify-center">
                        <div class="max-w-sm rounded overflow-hidden shadow-lg">
                            <div class="px-6 py-4">
                                Car park Name:<div class="text-xl mb-2">${carpark['carpark_name']}</div>
                            </div>
                            <div class="px-6 pt-4 pb-2">
                                <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">lots available: ${carpark['lotsavailable']}</span>
                                <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekday rate: ${carpark['rates']['weekdayrate']}</span>
                                <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">weekend rate: ${carpark['rates']['weekendrate']}</span>
                            </div>
                            <button onclick="confirmSelection('${carpark['carpark_name']}', '${carpark['google_lat']}', '${carpark['google_lon']}', '${carpark['carparkid']}')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mb-5 border border-2 rounded-full">
                                Select Car park
                            </button>
                        </div>
                    </div>`;
            }

            console.log('Generated HTML:', newHTML);
            document.getElementById('carparktopresults').innerHTML = newHTML;
        }
        return coordinates;
    } catch (error) {
        console.error('Error:', error.message);
        throw error
        // Handle the error
    }
}


function askForNotificationPreference(lat, lng, carparkID) {
    var isConfirmed = confirm("Do you want to receive notifications about your parking session?");
    if (isConfirmed) {
        // User wants to receive notifications
        sendSelectedCP(lat, lng, true, carparkID); 
    } else {
        // User does not want to receive notifications
        sendSelectedCP(lat, lng, false, carparkID); 
    }
}

function confirmSelection(carparkName, lat, lng, carparkID) {
    var isConfirmed = confirm("Confirm selection of " + carparkName + "?");
    if (isConfirmed) {
        askForNotificationPreference(lat, lng, carparkID);
        sessionStorage.setItem('carpark_name', carparkName);
    }
}

// This sends details of the carpark and parking session to session database
async function sendSelectedCP(lat,lng, notifAllowed, carparkID) {
    const data = {
        starttime: document.getElementById('starttime').value,
        endtime: document.getElementById('endtime').value,
        // userID: '007',  
        userID: sessionStorage.getItem('userID'),
        latitude: lat,
        longitude: lng,
        notifAllowed: notifAllowed,
        ppCode: carparkID
    };
    console.log(data);

        $.ajax({ 
            url: 'http://localhost:5006/session',
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(data), 
            success: function(e) { 
                console.log(e)
                if (e.code == 200){
                alert('Selection successful!');
                window.location.href = 'http://localhost:8000/views/nearbyAmenities';
                }
                else{
                    document.getElementById('errormsg').innerHTML = e.data;
                }
            }, 
            error: function(xhr, status, error) { 
                console.log("Error: " + xhr.responseText);
                document.getElementById('errormsg').innerHTML = JSON.parse(xhr.responseText).data;
            }
        });

        // $.ajax({ 
        //     url: 'http://localhost:5006/session',
        //     type: 'POST', 
        //     contentType: 'application/json', 
        //     data: JSON.stringify(data)
        // }).done(function(e) {
        //     console.log(e);
        //     alert('Selection successful!');
        //     window.location.href = 'http://localhost:8000/views/nearbyAmenities';
        // }).fail(function(xhr, status, error) {
        //     console.log("Error: " + xhr.responseText);
        //     document.getElementById('errormsg').innerHTML = JSON.parse(xhr.responseText).message;
        // });
        

}

