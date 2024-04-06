userID = sessionStorage.getItem('userID');
// userID = 6
console.log(userID);
var urlParams = new URLSearchParams(window.location.search);
var sessionID = urlParams.get('sessionID');
if(sessionID !== null){
sessionStorage.setItem('sessionID',sessionID);
}
sessionID = sessionStorage.getItem('sessionID');

console.log(sessionID);


function getSessionID(userID){

    axios.get('http://localhost:5006/session/' + userID)
    .then(function (response) {
      console.log(response);
      var sessionID = response.data.data.sessionID;
      // Now you can use sessionID as needed
      console.log(sessionID);
      // alert('Current session retrieved!');
    })
    .catch(function (error) {
      console.log("Error: " + error.response.data);
    });
  
console.log('getsessionid');
};

// after clicking submit button
document.getElementById('infoform').addEventListener('submit', async function(event) {
    event.preventDefault();
    console.log(sessionID);
    new_endtime = document.getElementById('endtime').value;
    console.log(new_endtime);
    // getSessionID(userID);
    // sessionID=5;
    console.log(sessionID);
    var isConfirmed = confirm("Confirm extension of session till " + new_endtime + "?");
    console.log('isconfirmed'+isConfirmed);
    if (isConfirmed) {
        askForNotificationPreference(new_endtime,sessionID);
    }
})

function askForNotificationPreference(new_endtime,sessionID) {
    console.log("askfornotif");
    var isConfirmed = confirm("Do you want to receive notifications about your parking session?");
    console.log('isconfirmed'+isConfirmed);
    if (isConfirmed) {
        // session wants to receive notifications
        updateSelectedCP(new_endtime, true, sessionID); 
    } else {
        // session does not want to receive notifications
        updateSelectedCP(new_endtime, false, sessionID); 
    }
}


// This updates details of the carpark and parking session to session database
async function updateSelectedCP(new_endtime, notifAllowed, sessionID) {
    console.log("updateselectedcp");
    confirmmessage = document.getElementById('confirmmessage')
    const data = {
        endtime: new_endtime, 
        notifAllowed: notifAllowed
    };
    
    console.log(data);

        axios.put('http://localhost:5006/session/' + sessionID, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json'
        }
        })
        .then(function (response) {
        // confirm('Update successful!');
            confirmmessage.style.color='green';
            confirmmessage.innerHTML = 'Update successful.<br>New end time: '+new_endtime;
            alert('Update successful. New end time: '+new_endtime);
            console.log(response.data);
            console.log('update successful!');
        })
        .catch(function (error) {
            confirmmessage.style.color='red';
            confirmmessage.innerHTML = error.response.data.message
            alert(error.response.data.message);
            console.log("Error: ", error.response.data);
        });
}
