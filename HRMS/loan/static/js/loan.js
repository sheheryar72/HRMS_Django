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
    const Loan_ID = rowData[1];

    getLeaveById(Loan_ID).then((singleLoanData) => {
        console.log("singleLoanData: ", singleLoanData)
        document.getElementById("FYID").value = singleLoanData.FYID;
        document.getElementById("Loan_ID").value = singleLoanData.Loan_ID;
        document.getElementById("Emp_ID").value = singleLoanData.Emp_ID;
        document.getElementById("Loan_Date").value = moment(singleLoanData.Loan_Date).format("YYYY-MM-DD");
        document.getElementById("Loan_Type").value = singleLoanData.Loan_Type;
        document.getElementById("Previous_Ded_Amount").value = Number(singleLoanData.Previous_Ded_Amount);
        document.getElementById("Loan_Amount").value = Number(singleLoanData.Loan_Amount);
        document.getElementById("Deducted_Amt").value = 0;
        document.getElementById("Loan_Bal_Amt").value = (Number(singleLoanData.Loan_Amount) - Number(singleLoanData.Previous_Ded_Amount));
        document.getElementById("Remarks").value = singleLoanData.Remarks;
        document.getElementById("Loan_Ded_NoofMnth").value = Number(singleLoanData.Loan_Ded_NoofMnth);
        document.getElementById("Loan_Ded_Amt").value = Number(singleLoanData.Loan_Ded_Amt);
        document.getElementById("loanStatus").value = singleLoanData.Loan_Status ? 1 : 0;

        document.getElementById("updateFormData").classList.remove("d-none");
        document.getElementById("insertFormData").classList.add("d-none");
    });
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const Leave_ID = rowData[1];
    console.log('Leave_ID: ', Leave_ID)
    if (confirm("Are you sure you want to delete this Leave?")) {
        deleteLeave(Leave_ID).then(success => {
            if (success) {
                displaySuccessMessage('Leave deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete Leave. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    document.getElementById("Loan_ID").value = '';
    document.getElementById("Loan_Date").value = '';
    document.getElementById("FYID").selectedIndex = 0;
    document.getElementById("Emp_ID").selectedIndex = 0;
    document.getElementById("Loan_Type").selectedIndex = 0;
    document.getElementById("loanStatus").selectedIndex = 0;
    document.getElementById("Remarks").value = "";
    document.getElementById("Previous_Ded_Amount").value = 0;
    document.getElementById("Loan_Amount").value = 0;
    document.getElementById("Loan_Ded_NoofMnth").value = 0;
    document.getElementById("Deducted_Amt").value = 0;
    document.getElementById("Loan_Ded_Amt").value = 0;
    document.getElementById("Loan_Bal_Amt").value = 0;

    document.getElementById(INSERT_BUTTON_ID).classList.remove('d-none');
    document.getElementById(UPDATE_BUTTON_ID).classList.add('d-none');
}

async function getAll(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to fetch Leave');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Leave:', error);
        return null;
    }
}

function fillEmployeeDropDown() {
    getAll(`/employee/getall`).then((data) => {
        let temp = '';
        console.log('fillEmployeeDropDown: ', data)
        data.forEach(element => {
            temp += `<option value="${element.Emp_ID}">${element.Emp_Name} - ${element.HR_Emp_ID}</option>`;
        });
        document.getElementById("Emp_ID").innerHTML = temp;
    });
}

function fillFinYearDropDown() {
    getAll(`/payroll_period/getall`).then((data) => {
        let temp = '';
        console.log('Fill payroll period dropdown: ', data)
        data.forEach(element => {
            temp += `<option value="${element.FYID}">${element.FinYear}</option>`;
        });
        document.getElementById("FYID").innerHTML = temp;
    });
}

async function getLeaveById(id) {
    try {
        const response = await fetch(`${BASE_URL}/loan/getbyid/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Leave');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching Leave with ID ${id}:`, error);
        return null;
    }
}

async function createLeave(data) {
    try {
        const response = await fetch(`${BASE_URL}/loan/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error('Failed to create Leave');
        }
        //const data = await response.json();
        displaySuccessMessage('Leave Added successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error creating Leave:', error);
        displayErrorMessage('Failed to create Leave. Please try again.');
        return null;
    }
}

async function updateLeave(id, data) {
    try {
        const response = await fetch(`${BASE_URL}/loan/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error('Failed to update Leave');
        }
        //const data = await response.json();
        displaySuccessMessage('Leave updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating Leave:', error);
        displayErrorMessage('Failed to update Leave. Please try again.');
        return null;
    }
}

async function deleteLeave(id) {
    try {
        const response = await fetch(`${BASE_URL}/loan/delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete Leave');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting Leave with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAll(`${BASE_URL}/loan/getall`).then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();

        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].Loan_ID, data[i].Loan_Type, data[i].Emp_Name, data[i].Loan_Amount,
                data[i].Loan_Status ? 'Active' : 'In-Active', actionButton.outerHTML];
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

function handleInsertClick() {
    const Loan_ID = document.getElementById("Loan_ID").value;
    const Loan_Date = document.getElementById("Loan_Date").value;
    const Loan_Type = document.getElementById("Loan_Type").value;
    const Previous_Ded_Amount = document.getElementById("Previous_Ded_Amount").value;
    const Loan_Amount = document.getElementById("Loan_Amount").value;
    const Loan_Ded_NoofMnth = document.getElementById("Loan_Ded_NoofMnth").value;
    const Loan_Ded_Amt = document.getElementById("Loan_Ded_Amt").value;
    // const Deducted_Amt = document.getElementById("Deducted_Amt").value;
    // const Loan_Bal_Amt = document.getElementById("Loan_Bal_Amt").value;
    const FYID = document.getElementById("FYID").value;
    const Emp_ID = document.getElementById("Emp_ID").value;
    const loanStatus = document.getElementById("loanStatus").value;
    const Remarks = document.getElementById("Remarks").value;

    const data = {
        Loan_ID: Number(Loan_ID),
        Loan_Date: Loan_Date,
        Loan_Type: Loan_Type,
        Previous_Ded_Amount: Number(Previous_Ded_Amount),
        Loan_Amount: Number(Loan_Amount),
        Loan_Ded_NoofMnth: Number(Loan_Ded_NoofMnth),
        Loan_Ded_Amt: Number(Loan_Ded_Amt),
        Emp_ID: Number(Emp_ID),
        FYID: Number(FYID),
        Loan_Status: (loanStatus),
        Remarks: Remarks
    }
    createLeave(data);
}

function handleUpdateClick() {
    const Loan_ID = document.getElementById("Loan_ID").value;
    const Loan_Date = document.getElementById("Loan_Date").value;
    const Loan_Type = document.getElementById("Loan_Type").value;
    const Previous_Ded_Amount = document.getElementById("Previous_Ded_Amount").value;
    const Loan_Amount = document.getElementById("Loan_Amount").value;
    const Loan_Ded_NoofMnth = document.getElementById("Loan_Ded_NoofMnth").value;
    const Loan_Ded_Amt = document.getElementById("Loan_Ded_Amt").value;
    // const Deducted_Amt = document.getElementById("Deducted_Amt").value;
    // const Loan_Bal_Amt = document.getElementById("Loan_Bal_Amt").value;
    const FYID = document.getElementById("FYID").value;
    const Emp_ID = document.getElementById("Emp_ID").value;
    const loanStatus = document.getElementById("loanStatus").value;
    const Remarks = document.getElementById("Remarks").value;

    const data = {
        Loan_ID: Number(Loan_ID),
        Loan_Date: Loan_Date,
        Loan_Type: Loan_Type,
        Previous_Ded_Amount: Number(Previous_Ded_Amount),
        Loan_Amount: Number(Loan_Amount),
        Loan_Ded_NoofMnth: Number(Loan_Ded_NoofMnth),
        Loan_Ded_Amt: Number(Loan_Ded_Amt),
        Emp_ID: Number(Emp_ID),
        FYID: Number(FYID),
        Loan_Status: Number(loanStatus),
        Remarks: Remarks
    }
    updateLeave(Loan_ID, data);
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

    document.getElementById('Loan_Date').valueAsDate = new Date();

    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    fillEmployeeDropDown()
    fillFinYearDropDown()
    fillTableGrid()
});

document.getElementById("Loan_Ded_NoofMnth").addEventListener("input", function () {
    const txtLoan_Amount = Number(document.getElementById("Loan_Amount").value);
    const deductedAmount = txtLoan_Amount / Number(this.value);
    document.getElementById("Loan_Ded_Amt").value = 0;
    document.getElementById("Deducted_Amt").value = deductedAmount;
    document.getElementById("Loan_Bal_Amt").value = txtLoan_Amount;
});