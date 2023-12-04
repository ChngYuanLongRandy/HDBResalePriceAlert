document.addEventListener('DOMContentLoaded', async function () {
    try {
        // Fetch YAML data
        const response = await fetch('/config/config.yaml');
        const yamlContent = await response.text();

        // Parse YAML into a JavaScript object
        const data = jsyaml.load(yamlContent);

        console.log(data);

        // Repopulate your comboboxes or perform other actions with the data
        repopulateComboboxes(data);

        // Attach event listener to the "Test send emails" button

        const testSendEmailButton = document.getElementById('testSendEmailButton');
        if (testSendEmailButton) {
            testSendEmailButton.addEventListener('click', testSendEmail);
        }
    } catch (error) {
        console.error('Error fetching YAML:', error);
    }
    
});

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

    // data.flatTypeCombobox.forEach(item => {
    //     const option = document.createElement('option');

    //     option.value = item.value;
    //     option.textContent = item.label;

    //     flatTypeCombobox.appendChild(option)
    // })

    // Example: Repopulate streetNameCombobox
    data.street_name_combobox.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.text = option;
        streetNameCombobox.add(optionElement);
    });
}

async function submitForm() {
    const flatType = document.getElementById('flatType').value;
    const streetName = document.getElementById('streetName').value;
    const blkNumberFrom = document.getElementById('blkNumberFrom').value;
    const blkNumberTo = document.getElementById('blkNumberTo').value;

    // When submit form is clicked, it will show the spinning wheel and hide content
    showLoader()
    hideContent()

    async function showLoader() {
        const loader = document.getElementById("loader");
        loader.classList.add("loader")
        loader.style.display = "block";
    }
    
    
    
    async function hideContent() {
        const content = document.getElementById("resultContainer");
        content.style.display = "none";
    }

    // Replace the URL with the actual endpoint for submitting the form data
    const submitEndpoint = '/submit';

    try {
        // Make a POST request to the submit endpoint
        const response = await fetch(submitEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ flatType, streetName, blkNumberFrom, blkNumberTo }),
        });

        console.log('Full response object:', response);

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Handle the response data as needed
        console.log('Submission successful:', data);
        console.log('Data type:', typeof data);
        console.log('Data column:', data.columns);
        console.log('Data rows:', data.data);

        // Display the results
        displayResults(data);
    } catch (error) {
        console.error('Error during submission:', error.message);
    }
}

// Function to handle result display
function displayResults(results) {
    const resultContainer = document.getElementById('resultContainer');
    const loadingContainer = document.getElementById('loadingContainer');


    // Hide the loading container and show content
    hideLoader()
    showContent()

    async function hideLoader() {
        const loader = document.getElementById("loader");
        loader.style.display = "none";
    }
    
    async function showContent() {
        const content = document.getElementById("resultContainer");
        content.style.display = "block";
    }

    if (results.data.length > 0) {
        // Clear previous results
        resultContainer.innerHTML = '';

        // Create a table to display the results
        const table = document.createElement('table');
        table.classList.add("table")
        // table.classList.add("table table-light table-hover")
        table.border = '1';

        // Create table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        // headerRow.classList.add(".table-light")

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
    } else {
        // Handle the case where results are empty
        resultContainer.innerHTML = 'No results for your query';
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

    try {
        // Make a POST request to the register endpoint
        const response = await fetch(registerEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, flatType, streetName, blkNumberFrom, blkNumberTo }),
        });

        console.log('Full response object:', response);        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        console.log('Before going to take response:');

        const data = await response.json();

        console.log('Data:', data);
        // Handle the response data as needed
        console.log('Submission successful:', data);
    } catch (error) {
        console.error('Error during submission:', error.message);
    }

}


function formatTimestamp(timestamp) {
    const date = new Date(timestamp);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    const formattedTimestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

    return formattedTimestamp;
}


async function testSendEmail() {
    console.log('testSendEmail() function called');

    // Replace the URL with the actual endpoint for registering a user
    const sendEmailEndpoint = '/testSendEmail';
    const currentTimestamp = new Date().getTime();
    const formattedTimestamp = formatTimestamp(currentTimestamp);

    try {
        // Make a POST request to the register endpoint
        const response = await fetch(sendEmailEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formattedTimestamp }),
        });

        console.log('Full response object:', response);
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        console.log('Before going to take response:');

        const data = await response.json();

        console.log('Data:', data);
        // Handle the response data as needed
        console.log('Submission successful, send Email request at:', data.currentTimestamp);
    } catch (error) {
        console.error('Error during submission:', error.message);
    }




}