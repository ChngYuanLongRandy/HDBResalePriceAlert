// Use window.onload to run the function when the page has finished loading
window.onload = function () {
    // Call the function to populate the combo boxes initially
    updateComboBoxes();

    const configPath = "config/config.yaml"

    // Additional JavaScript code can go here

    function updateComboBoxes(configPath) {
        // Assume your YAML content is stored in a variable named 'configPath'
        const config = jsyaml.load(configPath);

        // Use the config values to update the combo boxes
        repopulateComboBox('flatType', config.flat_type_combobox);
        repopulateComboBox('hdbTown', config.hdb_town_combobox);
    }

    function repopulateComboBox(comboBoxId, options) {
        const comboBox = document.getElementById(comboBoxId);

        // Clear existing options
        comboBox.innerHTML = '';

        // Populate with new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.text = option;
            comboBox.add(optionElement);
        });
    }
};

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
