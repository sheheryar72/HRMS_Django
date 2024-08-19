const BASE_URL = window.location.origin;
var table;
const INSERT_BUTTON_ID = 'insertFormData';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';
var region_array = [] 

function initializeDataTable() {
    table = $('#GridID').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
        scrollY: '330px',
        scrollCollapse: true,
        pageLength: 5,
        'columnDefs': [
            {
                "targets": 1,
                "className": "text-left",
            },
            {
                "targets": 2,
                "className": "text-left",
            }
        ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    });
}

// Handle click on table row
function handleTableRowClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const CT_ID = rowData[1];
    const CT_Descr = rowData[2];
    const REG_ID = rowData[3];

    $('#CT_ID').val(CT_ID);
    $('#CT_Descr').val(CT_Descr);   
    // $('#REG_ID').val(REG_ID);

    // Set the REG_ID dropdown based on the visible text
    setDropdownText("REG_ID", REG_ID);

    document.getElementById("insertFormData").classList.add("d-none");
    document.getElementById("updateFormData").classList.remove("d-none");
}

function setDropdownText(dropdownId, text) {
    var dropdown = document.getElementById(dropdownId);
    var options = dropdown.options;

    for (var i = 0; i < options.length; i++) {
        if (options[i].text === text) {
            dropdown.selectedIndex = i;
            break;
        }
    }
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const CT_ID = rowData[1];
    console.log('CT_ID: ', CT_ID)
    if (confirm("Are you sure you want to delete this City?")) {
        deleteCity(CT_ID).then(success => {
            if (success) {
                displaySuccessMessage('City deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete City. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    // document.getElementById("CT_ID").readOnly = false;
    document.getElementById("CT_ID").value = '';
    document.getElementById("CT_Descr").value = '';
    document.getElementById("REG_ID").selectedIndex = 0;
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllCity() {
    try {
        const response = await fetch(`${BASE_URL}/city/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch City');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching City:', error);
        return null;
    }
}

async function getAllRegion() {
    try {
        const response = await fetch(`${BASE_URL}/region/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch City');
        }
        const data = await response.json();

        var temp = ''
        data.forEach(element => {
            temp += `<option value='${element.REG_ID}'>${element.REG_Descr}</option>`
        });
        document.getElementById("REG_ID").innerHTML = temp
    } catch (error) {
        console.error('Error fetching City:', error);
        return null;
    }
}


async function getCityById(id) {
    try {
        const response = await fetch(`${BASE_URL}/city/${id}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch City');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching City with ID ${id}:`, error);
        return null;
    }
}

async function createCity(departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/city/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assume getCookie is a function to retrieve the CSRF token
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to create City');
        }
        //const data = await response.json();
        displaySuccessMessage('City created successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating City:', error);
        displayErrorMessage('Failed to create City. Please try again.');
        return null;
    }
}

async function updateCity(id, departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/city/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to update City');
        }
        //const data = await response.json();
        displaySuccessMessage('City updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating City:', error);
        displayErrorMessage('Failed to update City. Please try again.');
        return null;
    }
}

async function deleteCity(id) {
    try {
        const response = await fetch(`${BASE_URL}/city/delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete City');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting City with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllCity().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();
       
        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].CT_ID, data[i].CT_Descr, data[i].REG_Descr, actionButton.outerHTML];
            table.row.add(row).draw(false);
            counter++;
        }
    });
}

// Function to create action button element
function createActionButton() {
    var dropdown = document.createElement("div");
    dropdown.classList.add("dropdown");

    var button = document.createElement("button");
    button.classList.add("btn", "btn-dark", "dropdown-toggle");
    button.setAttribute("type", "button");
    button.setAttribute("id", "dropdownMenuButton1");
    button.setAttribute("data-toggle", "dropdown");
    button.setAttribute("aria-haspopup", "true");
    button.setAttribute("aria-expanded", "false");
    button.innerHTML = '<i class="fas fa-ellipsis-v"></i>';

    var dropdownMenu = document.createElement("div");
    dropdownMenu.classList.add("dropdown-menu");
    dropdownMenu.setAttribute("aria-labelledby", "dropdownMenuButton1");

    var editLink = document.createElement("a");
    editLink.classList.add("dropdown-item");
    editLink.classList.add("roweditclass");
    editLink.href = "#";
    editLink.innerText = "Edit";

    var deleteLink = document.createElement("a");
    deleteLink.classList.add("dropdown-item");
    deleteLink.classList.add("rowdeleteclass");
    deleteLink.href = "#";
    deleteLink.innerText = "Delete";

    dropdownMenu.appendChild(editLink);
    // dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleInsertClick(){
    const CT_ID = document.getElementById("CT_ID").value;
    const CT_Descr = document.getElementById("CT_Descr").value;
    const REG_ID = document.getElementById("REG_ID").value;

    const departmentData = {
        CT_ID: CT_ID,
        CT_Descr: CT_Descr,
        REG_ID: REG_ID
    }

    createCity(departmentData);
    
}

function handleUpdateClick(){
    const CT_ID = document.getElementById("CT_ID").value;
    const CT_Descr = document.getElementById("CT_Descr").value;
    const REG_ID = document.getElementById("REG_ID").value;

    const departmentData = {
        CT_ID: CT_ID,
        CT_Descr: CT_Descr,
        REG_ID: REG_ID
    }
    updateCity(CT_ID, departmentData);
    fillTableGrid();
}

// Function to retrieve CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Extract CSRF token from the cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function displaySuccessMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.classList.add('alert', 'alert-success', 'mt-3');
    alertContainer.textContent = message;
    document.getElementById('alertMessage').appendChild(alertContainer);
    setTimeout(() => {
        alertContainer.remove();
    }, 2000); // Remove the message after 3 seconds
}

function displayErrorMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.classList.add('alert', 'alert-danger', 'mt-3');
    alertContainer.textContent = message;
    document.getElementById('alertMessage').appendChild(alertContainer);
    setTimeout(() => {
        alertContainer.remove();
    }, 2000); // Remove the message after 3 seconds
}

$(document).ready(function () {
    initializeDataTable();
    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    getAllRegion()
    fillTableGrid()
});
