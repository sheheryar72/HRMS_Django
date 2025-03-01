const BASE_URL = window.location.origin;
var table, table5;
const INSERT_BUTTON_ID = 'insertFormData';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';

function initializeDataTable() {
    table = $('#GridID').DataTable({
        destroy: true,
        ordering: false,
        scrollY: '330px',
        scrollCollapse: true,
        pageLength: 5,
        columnDefs: [
            {
                targets: 1,
                className: "text-left",
            },
            {
                targets: 2,
                className: "text-left",
            },
            {
                targets: [8, 9, 10, 11, 12, 13],
                className: 'text-right' // Align numeric columns to the right
            }
        ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    });

    table5 = $('#GridID5').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
        pageLength: 5,
        // 'columnDefs': [
        //     {
        //         "targets": 1,
        //         "className": "text-left",
        //     }
        // ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    });

}

// Handle click on table row
async function handleTableRowClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const Leave_ID = rowData[1];
    const FYID = rowData[2];
    const Emp_ID = rowData[4];
    const EL_OP = rowData[8];
    const CL = rowData[9];
    const SL = rowData[10];
    const EL = rowData[11];
    const EGL = rowData[12];
    const Joining_Date = rowData[7];
    $('#Leave_ID').val(Leave_ID);
    $('#FYID').val(FYID);
    $('#Emp_ID').val(Emp_ID);
    $('#EL_OP').val(EL_OP);
    $('#EL').val(EL);
    $('#TOTAL_EL').val(EL_OP + EL);
    $('#CL').val(CL);
    $('#SL').val(SL);
    $('#EGL').val(EGL);
    document.getElementById('Joining_Date').value = moment(Joining_Date).format("YYYY-MM-DD");
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");

    data = await getLeaveById(Leave_ID);

    let TOTAL_EL = data.EL_OP + data.EL

    $('#EL').val(data.EL);
    $('#EL_OP').val(data.EL_OP);
    $('#TOTAL_EL').val(TOTAL_EL);
    $('#CL').val(data.CL);
    $('#SL').val(data.SL);
    $('#EGL').val(data.EGL);
    
    let LA_EL = data.LA_EL

    $('#LA_EL').val(LA_EL);
    // $('#LA_EL').val(data.LA_EL);
    $('#LA_CL').val(data.LA_CL);
    $('#LA_SL').val(data.LA_SL);
    $('#LA_EGL').val(data.LA_EGL);

    let BALANCE_EL = TOTAL_EL - LA_EL

    $('#Balance_EL').val(BALANCE_EL);
    $('#R_CL').val(data.CL - data.LA_CL);
    $('#R_SL').val(data.SL - data.LA_SL);
    $('#R_EGL').val(data.EGL - data.LA_EGL);
}


// Attach event listener to all elements with the 'leave_balance_class' class
Array.from(document.getElementsByClassName('leave_balance_class')).forEach(element => {
    element.addEventListener('focusout', function() {
        // Get input values and convert them to numbers
        const EL = parseFloat(document.getElementById("EL").value) || 0;
        const EL_OP = parseFloat(document.getElementById("EL_OP").value) || 0;
        const CL = parseFloat(document.getElementById("CL").value) || 0;
        const SL = parseFloat(document.getElementById("SL").value) || 0;
        const EGL = parseFloat(document.getElementById("EGL").value) || 0;

        const LA_EL = parseFloat(document.getElementById("LA_EL").value) || 0;
        const LA_CL = parseFloat(document.getElementById("LA_CL").value) || 0;
        const LA_SL = parseFloat(document.getElementById("LA_SL").value) || 0;
        const LA_EGL = parseFloat(document.getElementById("LA_EGL").value) || 0;

        // Calculate totals and balances
        const TOTAL_EL = EL + EL_OP;
        const Balance_EL = TOTAL_EL - LA_EL;
        const R_CL = CL - LA_CL;
        const R_SL = SL - LA_SL;
        const R_EGL = EGL - LA_EGL;

        // Set calculated values back to the respective fields
        document.getElementById("TOTAL_EL").value = TOTAL_EL;
        document.getElementById("Balance_EL").value = Balance_EL;
        document.getElementById("R_CL").value = R_CL;
        document.getElementById("R_SL").value = R_SL;
        document.getElementById("R_EGL").value = R_EGL;
    });
});



// document.getElementsByClassName('leave_balance_class').addEventListener('focusout', function(){
    
//     const EL = document.getElementById("EL").value;
//     const EL_OP = document.getElementById("EL_OP").value;
//     // const TOTAL_EL = document.getElementById("TOTAL_EL").value;
//     const CL = document.getElementById("CL").value;
//     const SL = document.getElementById("SL").value;
//     const EGL = document.getElementById("EGL").value;

//     const LA_EL = document.getElementById("LA_EL").value;
//     const LA_CL = document.getElementById("LA_CL").value;
//     const LA_SL = document.getElementById("LA_SL").value;
//     const LA_EGL = document.getElementById("LA_EGL").value;

//     // const Balance_EL = document.getElementById("Balance_EL").value;
//     // const R_CL = document.getElementById("R_CL").value;
//     // const R_SL = document.getElementById("R_SL").value;
//     // const R_EGL = document.getElementById("R_EGL").value;

//     let TOTAL_EL = EL + EL_OP

//     // $('#EL').val(EL);
//     // $('#EL_OP').val(EL_OP);
//     $('#TOTAL_EL').val(TOTAL_EL);
//     // $('#CL').val(CL);
//     // $('#SL').val(SL);
//     // $('#EGL').val(EGL);
    
//     $('#LA_EL').val(LA_EL);
//     // $('#LA_CL').val(LA_CL);
//     // $('#LA_SL').val(LA_SL);
//     // $('#LA_EL').val(LA_EL);
//     // $('#LA_EGL').val(LA_EGL);

//     $('#Balance_EL').val(TOTAL_EL - LA_EL);
//     $('#R_CL').val(CL - LA_CL);
//     $('#R_SL').val(SL - LA_SL);
//     $('#R_EGL').val(EGL - LA_EGL);

// })


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
    document.getElementById("Leave_ID").value = '';
    document.getElementById("FYID").selectedIndex = 0;
    document.getElementById("Emp_ID").selectedIndex = 0;
    document.getElementById("EL_OP").value = 0;
    document.getElementById("CL").value = 0;
    document.getElementById("SL").value = 0;
    document.getElementById("EL").value = 0;
    document.getElementById("EGL").value = 0;
    document.getElementById("EGL").value = 0;

    // document.getElementById("LA_EL_OP").value = 0;
    document.getElementById("LA_CL").value = 0;
    document.getElementById("LA_SL").value = 0;
    document.getElementById("LA_EL").value = 0;
    document.getElementById("TOTAL_EL").value = 0;

    document.getElementById("Balance_EL").value = 0;
    document.getElementById("R_SL").value = 0;
    document.getElementById("R_CL").value = 0;
    document.getElementById("R_EGL").value = 0;

    document.getElementById("Joining_Date").value = '';
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
        console.log('fillEmployeeDropDown: ', data)
        data.forEach(element => {
            temp += `<option value="${element.FYID}">${element.FinYear}</option>`;
        });
        document.getElementById("FYID").innerHTML = temp;
    });
}

async function getLeaveById(id) {
    try {
        const response = await fetch(`${BASE_URL}/leaves/getbyid/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Leave');
        }
        const data = await response.json();
        return data; 4
    } catch (error) {
        console.error(`Error fetching Leave with ID ${id}:`, error);
        return null;
    }
}

async function createLeave(data) {
    try {
        const response = await fetch(`${BASE_URL}/leaves/add`, {
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
        const response = await fetch(`${BASE_URL}/leaves/update/${id}`, {
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
        const response = await fetch(`${BASE_URL}/leaves/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
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
    getAll(`${BASE_URL}/leaves/getall`).then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();

        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].Leaves_ID, data[i].FYID, data[i].FinYear, data[i].Emp_ID, data[i].HR_Emp_ID
                , data[i].Emp_Name, moment(data[i].Emp_ID.Joining_Date).format("YYYY-MM-DD"), data[i].EL_OP, data[i].CL, data[i].SL, data[i].EL, data[i].EGL
                , data[i].EL_OP + data[i].CL + data[i].SL + data[i].EL + data[i].EGL, actionButton.outerHTML];
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
    const Leave_ID = document.getElementById("Leave_ID").value;
    const FYID = document.getElementById("FYID").value;
    const Emp_ID = document.getElementById("Emp_ID").value;

    const EL_OP = document.getElementById("EL_OP").value;
    const CL = document.getElementById("CL").value;
    const SL = document.getElementById("SL").value;
    const EL = document.getElementById("EL").value;
    const EGL = document.getElementById("EGL").value;

    // const LA_EL_OP = document.getElementById("LA_EL_OP").value;
    const LA_EL = document.getElementById("LA_EL").value;
    const LA_CL = document.getElementById("LA_CL").value;
    const LA_SL = document.getElementById("LA_SL").value;
    const LA_EGL = document.getElementById("LA_EGL").value;
    // const LA_EL = document.getElementById("LA_EL").value;

    let Total_Avail = Number(LA_EL) + Number(LA_CL) + Number(LA_SL) + Number(LA_EGL)

    const data = {
        Leaves_ID: Number(Leave_ID),
        FYID: Number(FYID),
        Emp_ID: Number(Emp_ID),
        EL_OP: Number(EL_OP),
        CL: Number(CL),
        SL: Number(SL),
        EL: Number(EL),
        EGL: Number(EGL),
        LA_CL: Number(LA_CL),
        LA_SL: Number(LA_SL),
        LA_EL: Number(LA_E),
        LA_EGL: Number(LA_EGL),
        Tot_LA: Number(Total_Avail)
    }
    createLeave(data);
}

function handleUpdateClick() {
    const Leave_ID = document.getElementById("Leave_ID").value;
    const FYID = document.getElementById("FYID").value;
    const Emp_ID = document.getElementById("Emp_ID").value;
    const EL_OP = document.getElementById("EL_OP").value;
    const CL = document.getElementById("CL").value;
    const SL = document.getElementById("SL").value;
    const EL = document.getElementById("EL").value;
    const EGL = document.getElementById("EGL").value;

    const LA_EL = document.getElementById("LA_EL").value;
    const LA_CL = document.getElementById("LA_CL").value;
    const LA_SL = document.getElementById("LA_SL").value;
    const LA_EGL = document.getElementById("LA_EGL").value;

    let Total_Avail = Number(LA_EL) + Number(LA_CL) + Number(LA_SL) + Number(LA_EGL)

    const data = {
        Leaves_ID: Number(Leave_ID),
        FYID: Number(FYID),
        Emp_ID: Number(Emp_ID),
        EL_OP: Number(EL_OP),
        CL: Number(CL),
        SL: Number(SL),
        EL: Number(EL),
        EGL: Number(EGL),
        LA_CL: Number(LA_CL),
        LA_SL: Number(LA_SL),
        LA_EL: Number(LA_EL),
        LA_EGL: Number(LA_EGL),
        Tot_LA: Number(Total_Avail)
    }
    updateLeave(Leave_ID, data);
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



// document.getElementById("leaveGridIconId").addEventListener("click", async function () {
//     const Leave_ID = Number(document.getElementById("Leave_ID").value);
//     console.log('Leave ID: ', Leave_ID);

//     let data = null; // Declare `data` outside the `if` block

//     if (Leave_ID !== 0) {
//         try {
//             data = await getLeaveById(Leave_ID);
//         } catch (error) {
//             console.error("Error fetching leave data:", error);
//             alert("An error occurred while fetching leave data. Please try again.");
//             $("#orangeModalSubscription4").modal('hide');
//             return;
//         }
//     } else {
//         alert("Please select leave first!");
//         $("#orangeModalSubscription4").modal('hide');
//         return;
//     }

//     console.log('Leave By ID Data: ', data);

//     if (data) {
//         try {
//             // Validate the required fields in the data object
//             if (
//                 typeof data.CL === "number" &&
//                 typeof data.SL === "number" &&
//                 typeof data.EL_OP === "number" &&
//                 typeof data.EL === "number" &&
//                 typeof data.EGL === "number"
//             ) {
//                 table5.clear().draw();
//                 table5.row.add([
//                     data.Emp_Name,
//                     data.LA_CL,
//                     data.LA_SL,
//                     data.LA_EL_OP,
//                     data.LA_EL,
//                     data.LA_EGL,
//                     data.CL - data.LA_CL,
//                     data.SL - data.LA_SL,
//                     data.EL_OP - data.LA_EL_OP,
//                     data.EL - data.LA_EL,
//                     data.EGL - data.LA_EGL,
//                     data.Tot_LA
//                 ]).draw(false);
//             } else {
//                 throw new Error("Incomplete leave data received.");
//             }
//         } catch (error) {
//             console.error("Error processing leave data:", error);
//             alert("Failed to process leave data. Please verify the input and try again.");
//             $("#orangeModalSubscription4").modal('hide');
//         }
//     } else {
//         console.error("No data returned for Leave ID:", Leave_ID);
//         alert("Failed to fetch leave data!");
//         $("#orangeModalSubscription4").modal('hide');
//     }
// });



$(document).ready(function () {
    initializeDataTable();

    document.getElementById('Joining_Date').valueAsDate = new Date();

    // $('#GridID5 tbody').on('click', 'tr', handleTableRowClick3);

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
