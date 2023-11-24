function submitForm() {
    const flatType = document.getElementById('flatType').value;
    const streetName = document.getElementById('streetName').value;
    const resaleDate = document.getElementById('resaleDate').value;

    // Replace the URL with the actual endpoint for submitting the form data
    const submitEndpoint = '/submit';

    // Make an API call or perform any necessary action with the form data
    console.log('Submitting form data:', { flatType, streetName, resaleDate });

    // Make a POST request to the submit endpoint
    fetch(submitEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ flatType, streetName, resaleDate }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle the response data as needed
        console.log('Submission successful:', data);
    })
    .catch(error => {
        console.error('Error during submission:', error.message);
    });
}

function registerUser() {
    const email = document.getElementById('email').value;

    // Replace the URL with the actual endpoint for registering a user
    const registerEndpoint = '/register';

    // Make an API call or perform any necessary action with the user's email
    console.log('Registering user with email:', email);

    // Make a POST request to the register endpoint
    fetch(registerEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
    })
}
