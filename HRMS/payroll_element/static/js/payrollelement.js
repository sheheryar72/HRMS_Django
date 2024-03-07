const BASE_URL = 'http://127.0.0.1:8000/payrollelement/api/';
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

function handleTableRowClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const Element_ID = rowData[1];
    const Element_Name = rowData[2];
    const Element_Type = rowData[3];
    const Element_Categpry = rowData[4];
    $('#Element_ID').val(Element_ID);
    $('#Element_Name').val(Element_Name);
    $('#Element_Type').val(Element_Type);
    $('#Element_Category').val(Element_Categpry);
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");
}

function handleDeleteButtonClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const Element_ID = rowData[1];
    console.log('Element_ID: ', Element_ID)
    if (confirm("Are you sure you want to delete this Payroll Element?")) {
        deletePayrollElement(Element_ID).then(success => {
            if (success) {
                displaySuccessMessage('Payroll Element deleted successfully!');
                fillTableGrid(); 
            } else {
                displayErrorMessage('Failed to delete Payroll Element. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    document.getElementById("Element_ID").readOnly = false;
    document.getElementById("Element_ID").value = '';
    document.getElementById("Element_Name").value = '';
    document.getElementById("Element_Type").value = '';
    document.getElementById("Element_Category").value = '';
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllPayrollElement() {
    try {
        const response = await fetch(`${BASE_URL}getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch Payroll Element');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Payroll Element:', error);
        return null;
    }
}

async function getPayrollElementById(id) {
    try {
        const response = await fetch(`${BASE_URL}/getbyid/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Payroll Element');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching Payroll Element with ID ${id}:`, error);
        return null;
    }
}

async function createPayrollElement(formData) {
    try {
        console.log('formData: ', formData)
        const response = await fetch(`${BASE_URL}add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        if (!response.ok) {
            throw new Error('Failed to create Payroll Element');
        }
        //const data = await response.json();
        displaySuccessMessage('Payroll Element created successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating Payroll Element:', error);
        displayErrorMessage('Failed to create Payroll Element. Please try again.');
        return null;
    }
}

async function updatePayrollElement(id, formData) {
    try {
        console.log('formData: ', formData)
        const response = await fetch(`${BASE_URL}update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        if (!response.ok) {
            throw new Error('Failed to update Payroll Element');
        }
        //const data = await response.json();
        displaySuccessMessage('Payroll Element updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating Payroll Element:', error);
        displayErrorMessage('Failed to update Payroll Element. Please try again.');
        return null;
    }
}

async function deletePayrollElement(id) {
    try {
        const response = await fetch(`${BASE_URL}delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete Payroll Element');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting Payroll Element with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllPayrollElement().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();
       
        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); 
            var row = [counter, data[i].Element_ID, data[i].Element_Name, data[i].Element_Type, data[i].Element_Category, actionButton.outerHTML];
            table.row.add(row).draw(false);
            counter++;
        }
    });
}

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
    dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleInsertClick(){
    const Element_ID = document.getElementById("Element_ID").value;
    const Element_Name = document.getElementById("Element_Name").value;
    const Element_Type = document.getElementById("Element_Type").value;
    const Element_Category = document.getElementById("Element_Category").value;

    const formData = {
        Element_ID: Element_ID,
        Element_Name: Element_Name,
        Element_Type: Element_Type,
        Element_Category: Element_Category
    }
    createPayrollElement(formData);
    
}

function handleUpdateClick(){
    const Element_ID = document.getElementById("Element_ID").value;
    const Element_Name = document.getElementById("Element_Name").value;
    const Element_Type = document.getElementById("Element_Type").value;
    const Element_Category = document.getElementById("Element_Category").value;

    const formData = {
        Element_ID: Element_ID,
        Element_Name: Element_Name,
        Element_Type: Element_Type,
        Element_Category: Element_Category
    }
    updatePayrollElement(Element_ID, formData);
    fillTableGrid();
}

function displaySuccessMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.classList.add('alert', 'alert-success', 'mt-3');
    alertContainer.textContent = message;
    document.getElementById('alertMessage').appendChild(alertContainer);
    setTimeout(() => {
        alertContainer.remove();
    }, 2000); 
}

function displayErrorMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.classList.add('alert', 'alert-danger', 'mt-3');
    alertContainer.textContent = message;
    document.getElementById('alertMessage').appendChild(alertContainer);
    setTimeout(() => {
        alertContainer.remove();
    }, 2000); 
}

$(document).ready(function () {
    initializeDataTable();
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); 
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    fillTableGrid()
});



