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

// function handleTableRowClick() {
//     var DSG_ID = $(this).find('td')[1].innerHTML;
//     var DSG_Descr = $(this).find('td')[2].innerHTML;

//     // document.getElementById("DSG_ID").readOnly = true;
//     document.getElementById("DSG_ID").value = DSG_ID;
//     document.getElementById("DSG_Descr").value = DSG_Descr;
// }

// Handle click on table row
function handleTableRowClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const DSG_ID = rowData[1];
    const DSG_Descr = rowData[2];
    $('#DSG_ID').val(DSG_ID);
    $('#DSG_Descr').val(DSG_Descr);
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const DSG_ID = rowData[1];
    console.log('DSG_ID: ', DSG_ID)
    if (confirm("Are you sure you want to delete this designation?")) {
        deleteDesignation(DSG_ID).then(success => {
            if (success) {
                displaySuccessMessage('Designation deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete designation. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    // document.getElementById("DSG_ID").readOnly = false;
    document.getElementById("DSG_ID").value = '';
    document.getElementById("DSG_Descr").value = '';
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllDesignations() {
    try {
        const response = await fetch(`${BASE_URL}/designation/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch designations');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching designations:', error);
        return null;
    }
}

async function getDesignationById(id) {
    try {
        const response = await fetch(`${BASE_URL}/${id}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch designation');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching designation with ID ${id}:`, error);
        return null;
    }
}

async function createDesignation(designationData) {
    try {
        const response = await fetch(`${BASE_URL}/designation/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(designationData),
        });
        if (!response.ok) {
            throw new Error('Failed to create designation');
        }
        //const data = await response.json();
        displaySuccessMessage('Designation created successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating designation:', error);
        displayErrorMessage('Failed to create designation. Please try again.');
        return null;
    }
}

async function updateDesignation(id, designationData) {
    try {
        const response = await fetch(`${BASE_URL}/designation/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(designationData),
        });
        if (!response.ok) {
            throw new Error('Failed to update designation');
        }
        //const data = await response.json();
        displaySuccessMessage('Designation updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating designation:', error);
        displayErrorMessage('Failed to update designation. Please try again.');
        return null;
    }
}

async function deleteDesignation(id) {
    try {
        const response = await fetch(`${BASE_URL}/designation/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        });
        if (!response.ok) {
            throw new Error('Failed to delete designation');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting designation with ID ${id}:`, error);
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
            var row = [counter, data[i].DSG_ID, data[i].DSG_Descr, actionButton.outerHTML];
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
    const DSG_ID = document.getElementById("DSG_ID").value;
    const DSG_Descr = document.getElementById("DSG_Descr").value;

    const designationData = {
        DSG_ID: DSG_ID,
        DSG_Descr: DSG_Descr
    }
    createDesignation(designationData);
    
}

function handleUpdateClick(){
    const DSG_ID = document.getElementById("DSG_ID").value;
    const DSG_Descr = document.getElementById("DSG_Descr").value;

    const designationData = {
        DSG_ID: DSG_ID,
        DSG_Descr: DSG_Descr
    }
    updateDesignation(DSG_ID, designationData);
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

// Example usage:
// getAllDesignations().then(data => console.log(data));
// getDesignationById(1).then(data => console.log(data));
// createDesignation({ name: 'New Designation' }).then(data => console.log(data));
// updateDesignation(1, { name: 'Updated Designation' }).then(data => console.log(data));
// deleteDesignation(1).then(success => console.log(success));

