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
    const Grade_ID = rowData[1];
    const Grade_Descr = rowData[2];
    $('#Grade_ID').val(Grade_ID);
    $('#Grade_Descr').val(Grade_Descr);
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const Grade_ID = rowData[1];
    console.log('Grade_ID: ', Grade_ID)
    if (confirm("Are you sure you want to delete this Grade?")) {
        deleteDesignation(Grade_ID).then(success => {
            if (success) {
                displaySuccessMessage('Grade deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete Grade. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    // document.getElementById("Grade_ID").readOnly = false;
    document.getElementById("Grade_ID").value = '';
    document.getElementById("Grade_Descr").value = '';
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllDesignations() {
    try {
        const response = await fetch(`${BASE_URL}/grade/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Grade:', error);
        return null;
    }
}

async function getDesignationById(id) {
    try {
        const response = await fetch(`${BASE_URL}/grade/${id}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching Grade with ID ${id}:`, error);
        return null;
    }
}

async function createDesignation(departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/grade/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to create Grade');
        }
        //const data = await response.json();
        displaySuccessMessage('Grade created successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating Grade:', error);
        displayErrorMessage('Failed to create Grade. Please try again.');
        return null;
    }
}

async function updateDesignation(id, departmentData) {
    try {
        const response = await fetch(`${BASE_URL}/grade/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(departmentData),
        });
        if (!response.ok) {
            throw new Error('Failed to update Grade');
        }
        //const data = await response.json();
        displaySuccessMessage('Grade updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating Grade:', error);
        displayErrorMessage('Failed to update Grade. Please try again.');
        return null;
    }
}

async function deleteDesignation(id) {
    try {
        const response = await fetch(`${BASE_URL}/grade/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        });
        if (!response.ok) {
            throw new Error('Failed to delete Grade');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting Grade with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllDesignations().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();
       
        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].Grade_ID, data[i].Grade_Descr, actionButton.outerHTML];
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
    const Grade_ID = document.getElementById("Grade_ID").value;
    const Grade_Descr = document.getElementById("Grade_Descr").value;

    const departmentData = {
        Grade_ID: Grade_ID,
        Grade_Descr: Grade_Descr
    }
    createDesignation(departmentData);
    
}

function handleUpdateClick(){
    const Grade_ID = document.getElementById("Grade_ID").value;
    const Grade_Descr = document.getElementById("Grade_Descr").value;

    const departmentData = {
        Grade_ID: Grade_ID,
        Grade_Descr: Grade_Descr
    }
    updateDesignation(Grade_ID, departmentData);
    fillTableGrid();
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
