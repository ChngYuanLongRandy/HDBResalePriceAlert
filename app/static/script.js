document.addEventListener('DOMContentLoaded', function () {
    // Fetch YAML data
    fetch('/config/config.yaml')
        .then(response => response.text())
        .then(yamlContent => {
            // Parse YAML into a JavaScript object
            const data = jsyaml.load(yamlContent);

            console.log(data);

           // Repopulate your comboboxes or perform other actions with the data
           repopulateComboboxes(data);
        })
        .catch(error => console.error('Error fetching YAML:', error));

    // Function to repopulate comboboxes
    function repopulateComboboxes(data) {
        // Access data and update your comboboxes
        const flatTypeCombobox = document.getElementById('flatType');
        const streetNameCombobox = document.getElementById('streetName');

        // Example: Repopulate flatTypeCombobox
        data.flat_type_combobox.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.text = option;
            flatTypeCombobox.add(optionElement);
        });

        // Example: Repopulate streetNameCombobox
        data.street_name_combobox.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.text = option;
            streetNameCombobox.add(optionElement);
        });
    }
});

async function submitForm() {

    const flatType = document.getElementById('flatType').value;
    const streetName = document.getElementById('streetName').value;
    const blkNumberFrom = document.getElementById('blkNumberFrom').value;
    const blkNumberTo = document.getElementById('blkNumberTo').value;

    // Replace the URL with the actual endpoint for submitting the form data
    const submitEndpoint = '/submit';

    // Make an API call or perform any necessary action with the form data
    console.log('Submitting form data:', { flatType, streetName, blkNumberFrom, blkNumberTo});

    // Make a POST request to the submit endpoint
    await fetch(submitEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ flatType, streetName, blkNumberFrom, blkNumberTo }),
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
        console.log('data column ', data.columns)
        console.log('datas data ' , data.data)
        // Display the results
        displayResults(data); // Assuming your response data has a similar structure to the example in the previous message
        
    })
    .catch(error => {
        console.error('Error during submission:', error.message);
    });
}

    // Function to handle result display
    function displayResults(results) {

        if (results.data.length > 0 ) {
            // Assuming you have a div with id "resultContainer" to display the results
            const resultContainer = document.getElementById('resultContainer');

            // Clear previous results
            resultContainer.innerHTML = '';

            // Create a table to display the results
            const table = document.createElement('table');
            table.border = '1';

            // Create table header
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');

            results.columns.forEach(column => {
                const th = document.createElement('th');
                th.textContent = column;
                headerRow.appendChild(th);
            });

            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Create table body
            const tbody = document.createElement('tbody');

            results.data.forEach(rowData => {
                const tr = document.createElement('tr');

                rowData.forEach(cellData => {
                    const td = document.createElement('td');
                    td.textContent = cellData;
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });

            table.appendChild(tbody);

            // Append the table to the result container
            resultContainer.appendChild(table);
        }
        
        else {
            // Handle the case where results is empty
            resultContainer.innerHTML = "No results for your query"
            console.log('No results to display.');
        }
    }

async function registerUser() {
    const email = document.getElementById('email').value;
    const flatType = document.getElementById('flatType').value;
    const streetName = document.getElementById('streetName').value;
    const blkNumberFrom = document.getElementById('blkNumberFrom').value;
    const blkNumberTo = document.getElementById('blkNumberTo').value;

    // Replace the URL with the actual endpoint for registering a user
    const registerEndpoint = '/register';

    // Make an API call or perform any necessary action with the user's email
    console.log('Registering user with email:', email, 'flatType:', flatType, 'streetName:', streetName);

    // Make a POST request to the register endpoint
    await fetch(registerEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email , flatType, streetName, blkNumberFrom, blkNumberTo}),
    })
    .then(response => {
        console.log('Full response object:', response);
        console.log('Response.json():', response.json());
        console.log('Response.text():', response.text());
        console.log('Response status:', response.status);
        if (!response.status.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle the response data as needed
        console.log('Submission successful, registered email address :', data['data']);
    })
    .catch(error => {
        console.error('Error during submission:', error.message);
    });

    //     // Make a POST request to the register endpoint
    // const response =fetch(registerEndpoint, {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({ email , flatType, streetName, blkNumberFrom, blkNumberTo}),
    //     })
    //     .then(response => {
    //         console.log('Full response object:', response);
    //         if (!response.status.ok) {
    //             throw new Error(`Error ${response.status}: ${response.statusText}`);
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         // Handle the response data as needed
    //         console.log('Submission successful, registered email address :', data['data']);
    //     })
    //     .catch(error => {
    //         console.error('Error during submission:', error.message);
    //     });
    // }
}
