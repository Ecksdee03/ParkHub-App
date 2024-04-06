console.log("running...")


document.getElementById('loginform').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    try{
    const email = document.getElementById('emaillogin').value;
    console.log(email);
    const password = document.getElementById('passwordlogin').value;

    sendSession(email,password);
    
    } 
    catch (error) {
        console.error('Error:', error.message);
        // Handle the error
    }
});

async function sendSession(email,password) {
    const data = {
        email: email,
        password: password
    };
    console.log(data);

        $.ajax({ 
            url: 'http://localhost:5010/checkuser',
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(data), 
            // xhrFields: {
            //     withCredentials: true
            // },
            success: function(response) {
                if (response.code === 201 && response.data) {
                    // Assuming response.data contains the user object, including userID
                    // Store user data in session storage
                    sessionStorage.setItem('userID', response.data.userID);
                    // sessionStorage.setItem('userID',6)
                    // Optionally, redirect the user to another page or update the UI to reflect successful login
                    console.log('Login successful! User ID:', response.data.userID);
                    alert('Login successful!');
                    window.location.href = 'http://localhost:8000/views';
                } else {
                    // Handle login failure
                    document.getElementById('message').innerHTML = 'Incorrect details';
                    alert('Login failed. Please check your credentials.');
                }
            },
            error: function(xhr, status, error) {
                console.log("Error: " + xhr.responseText);
                alert("Login error: Please check your credentials");
            }
        });

}