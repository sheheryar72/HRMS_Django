const BASE_URL = window.location.origin;
var table;
const INSERT_BUTTON_ID = 'insertFormData';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';

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
    const REG_ID = rowData[1];
    const REG_Descr = rowData[2];
    $('#REG_ID').val(REG_ID);
    $('#REG_Descr').val(REG_Descr);
    document.getElementById("insertFormData").classList.add("d-none");
    document.getElementById("updateFormData").classList.remove("d-none");
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const REG_ID = rowData[1];
    console.log('REG_ID: ', REG_ID)
    if (confirm("Are you sure you want to delete this region?")) {
        deleteregion(REG_ID).then(success => {
            if (success) {
                displaySuccessMessage('region deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete region. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    // document.getElementById("REG_ID").readOnly = false;
    document.getElementById("REG_ID").value = '';
    document.getElementById("REG_Descr").value = '';
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllregion() {
    try {
        const response = await fetch(`${BASE_URL}/region/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch region');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching region:', error);
        return null;
    }
}

async function getregionById(id) {
    try {
        const response = await fetch(`${BASE_URL}/region/${id}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch region');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching region with ID ${id}:`, error);
        return null;
    }
}

async function createregion(departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/region/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assume getCookie is a function to retrieve the CSRF token
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to create region');
        }
        //const data = await response.json();
        displaySuccessMessage('region created successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating region:', error);
        displayErrorMessage('Failed to create region. Please try again.');
        return null;
    }
}

async function updateregion(id, departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/region/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to update region');
        }
        //const data = await response.json();
        displaySuccessMessage('region updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating region:', error);
        displayErrorMessage('Failed to update region. Please try again.');
        return null;
    }
}

async function deleteregion(id) {
    try {
        const response = await fetch(`${BASE_URL}/region/delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete region');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting region with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllregion().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();
       
        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].REG_ID, data[i].REG_Descr, actionButton.outerHTML];
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
    const REG_ID = document.getElementById("REG_ID").value;
    const REG_Descr = document.getElementById("REG_Descr").value;

    const departmentData = {
        REG_ID: REG_ID,
        REG_Descr: REG_Descr
    }
    createregion(departmentData);
    
}

function handleUpdateClick(){
    const REG_ID = document.getElementById("REG_ID").value;
    const REG_Descr = document.getElementById("REG_Descr").value;

    const departmentData = {
        REG_ID: REG_ID,
        REG_Descr: REG_Descr
    }
    updateregion(REG_ID, departmentData);
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
    fillTableGrid()
});
