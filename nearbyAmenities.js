if (sessionStorage.getItem('userID') == null){
    window.location.href = 'http://localhost:8000/views/login';
    };

document.getElementById("carparkname").innerHTML = sessionStorage.getItem('carpark_name')

async function request_nearby_amenities() {
    // Event listener for the submit button click


    document.getElementById('search_amenities_btn').addEventListener('click', function() {
        let selectedFilters = '';

        // if either radio buttons are clicked and submitted
        if (document.getElementById('carwash-checkbox').checked) {
            selectedFilters = document.getElementById('carwash-checkbox').value
        }
        if (document.getElementById('convenience-store-checkbox').checked) {
            selectedFilters = document.getElementById('convenience-store-checkbox').value
        }
        if (document.getElementById('gas-station-checkbox').checked) {
            selectedFilters = document.getElementById('gas-station-checkbox').value
        }

        userID = sessionStorage.getItem('userID')

        // console.log(userID)
        try {
            
            $.ajax({ 
                url: 'http://localhost:5012/search_amenities', 
                type: 'POST', 
                contentType: 'application/json', 
                data: JSON.stringify(
                    { 
                        selectedFilters: selectedFilters,
                        userID: userID
                     }
                ), 
                success: function(response) { 

                    // console.log(response)
                    result_string = ''
                    no_matching_results_string = ''

                    nearby_amenities_container = document.getElementById("nearby_amenities_results")
                    no_matching_results_container = document.getElementById("no_matching_results")
                    let location_array_of_dicts = response

                    console.log(response.message)

                    if (response.message) {
                        no_matching_results_string += `<p>${response.message}</p>`
                    }
                    else {
                        if (selectedFilters == '') {
                            no_matching_results_string = "<p class='text-red-500 font-semibold'>Please select filters.</p>"
                        }
                        if (selectedFilters != '') {
    
                            location_array_of_dicts.forEach(function(each_result) {
                                console.log(each_result)
                                let typesArray = each_result.type.split(',').map(type => type.trim());
                                console.log(typesArray)
                                if (typesArray.includes(selectedFilters)) {
                                    place_name = each_result.name;
                                    place_type = selectedFilters;
    
                                    if (place_type == 'car_wash') {
                                        place_type = 'Car Wash';
                                    } else if (place_type == 'convenience_store') {
                                        place_type = 'Convenience Store';
                                    } else if (place_type == 'gas_station') {
                                        place_type = 'Gas Station';
                                    }
    
                                    place_address = each_result.address;
                                    place_photo = each_result.photo;
    
                                    result_string += `<div class="max-w-xs w-full sm:w-1/2 md:w-1/3 lg:w-1/4 mr-5">
                                                        <div class="flex flex-col justify-center items-center outline outline-1 rounded bg-white overflow-hidden shadow-lg pt-5">
                                                            <div class="items-start px-6 py-4">
                                                                <img src="${place_photo}" class="rounded w-64 h-64 " >
                                                                <div class="text-left px-6 py-4">
                                                                    <p class="mb-2">Type: ${place_type}</p>
                                                                    <p class="mb-2">Name: ${place_name}</p>
                                                                    <p class="mb-2">Address: ${place_address}</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>`;
    
                                    
                                    // selectedFilters = selectedFilters.filter(item => item !== selectedFilters[index]);
                                }
                            });
                            
                        }  
                    }
                    
                    nearby_amenities_container.innerHTML = result_string
                    no_matching_results_container.innerHTML = no_matching_results_string
                }, 
                error: function(error) { 
                    console.log(error); 
                } 
            });
        } 
        catch (error) {
            console.error('Error:', error.message);
            throw error;
        }
        
    });
}

request_nearby_amenities()

