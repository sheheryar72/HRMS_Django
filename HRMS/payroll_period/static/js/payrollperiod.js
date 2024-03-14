const BASE_URL = 'http://localhost:8000/payrollperiod/api/';
var table, table2, current_finyear = {};
const INSERT_BUTTON_ID = 'insertFormData';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';

function initializeDataTable() {
    table = $('#GridID').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
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
    table2 = $('#GridID2').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
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
    const FYID = rowData[1];
    const FINYear = rowData[2];
    const FYStatus = rowData[3];
    $('#FYID').val(FYID);
    $('#FINYear').val(FINYear);
    $('#FYStatus').val(FYStatus == 'Active' ? 1 : 0);
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");
}

function handleDeleteButtonClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const FYID = rowData[1];
    console.log('FYID: ', FYID)
    alert("Sorry you can not delete Finantial Year time Time!")
    // if (confirm("Are you sure you want to delete this Financial Year?")) {
    //     deleteFinancialYear(FYID).then(success => {
    //         if (success) {
    //             displaySuccessMessage('Financial Year deleted successfully!');
    //             fillTableGrid(); 
    //         } else {
    //             displayErrorMessage('Failed to delete Financial Year. Please try again.');
    //         }
    //     });
    // }
}

function handleFinPeriodMonthTableRowClick() {
    const rowData = table.row($(this).closest('tr')).data();
    const FYID = rowData[1];
    console.log('FYID: ', FYID)
    fillTable2Grid(FYID)
}

function handlePeriodMonthTableRowClick() {
    const rowData = table2.row($(this).closest('tr')).data();
    console.log('rowData: ', rowData);
    const PERIOD_ID = rowData[1];
    const FINID = rowData[2];
    console.log('PERIOD_ID: ', PERIOD_ID);
    // alert("Sorry you can not delete Finantial year this time!")
    if (confirm("Are you sure you want to Active this Period Month?")) {
        updatePeriodMonth(PERIOD_ID).then(success => {
            if (success) {
                displaySuccessMessage('Period Month activated successfully!');
                fillTable2Grid(FINID); 
            } else {
                displayErrorMessage('Failed to activate Period Month. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    document.getElementById("FYID").readOnly = true;
    document.getElementById("FYID").value = '';
    document.getElementById("FINYear").value = '';
    document.getElementById("FYStatus").selectedIndex = 0;
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

function createActionButton() {``
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

    var periodDetailLink = document.createElement("a");
    periodDetailLink.classList.add("dropdown-item");
    periodDetailLink.classList.add("rowfinperiodmonthclass");
    periodDetailLink.href = "#";
    periodDetailLink.innerText = "Period Details";

    dropdownMenu.appendChild(editLink);
    dropdownMenu.appendChild(deleteLink);
    // dropdownMenu.appendChild(periodDetailLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleInsertClick(){
    const FYID = document.getElementById("FYID").value;
    const FINYear = document.getElementById("FINYear").value;
    const FYStatus = document.getElementById("FYStatus").value;

    const formData = {
        FYID: FYID,
        FinYear: FINYear,
        FYStatus: FYStatus
    }

    if (Number(FINYear.substring(2, 4)) + 1 != Number(FINYear.substring(7))) {
        displayErrorMessage('Please Add correct financial year')
        return;
    }

    let checkFinYearExist = false;
    $("#InserRowID tr").each(function(){
        grid_finyear = $(this).find("td:eq(2)").text();
        
        if (FINYear == grid_finyear){
            checkFinYearExist = true
        }
    })

    if (checkFinYearExist){
        displayErrorMessage('financial year alreay Exist')
        return
    }  
    createFinancialYear(formData);
}

function handleUpdateClick(){
    const FYID = document.getElementById("FYID").value;
    const FinYear = document.getElementById("FINYear").value;
    const FYStatus = document.getElementById("FYStatus").value;

    const departmentData = {
        FYID: FYID,
        FinYear: FinYear,
        FYStatus: FYStatus
    }
    updateFinancialYear(FYID, departmentData);
    fillTableGrid();
    if (FYStatus == 1){
        fillTable2Grid(FYID);
    }
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
    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); 
    $('#GridID tbody').on('click', '.rowfinperiodmonthclass', handleFinPeriodMonthTableRowClick); 
    $('#GridID2 tbody').on('click', '.rowperiodmonthclass', handlePeriodMonthTableRowClick);
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    current_finyear =  {};
    fillTableGrid()
    console.log('current_finyear current_finyear: ', current_finyear)
    // fillTable2Grid(current_finyear.FYID)
});

async function getAllFinancialYears() {
    try {
        const response = await fetch(`${BASE_URL}getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch Financial Year');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Financial Year:', error);
        return null;
    }
}

async function getAllPayrollPeriod(id) {
    try {
        const response = await fetch(`${BASE_URL}getallpayrollperiod/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Financial Year');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Financial Year:', error);
        return null;
    }
}

async function getFinancialYearById(id) {
    try {
        const response = await fetch(`${BASE_URL}${id}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch Financial Year');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching Financial Year with ID ${id}:`, error);
        return null;
    }
}

async function createFinancialYear(formData) {
    console.log('formData: ', formData)
    try {
        const response = await fetch(`${BASE_URL}add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        if (!response.ok) {
            throw new Error('Failed to create Financial Year');
        }
        const obj = await response.json();
        displaySuccessMessage('Financial Year created successfully!');
        console.log('created data: ', obj)
        fillTableGrid();
        debugger
        if (obj.data.FYStatus){
            current_finyear = obj.data;
            fillTable2Grid(obj.data.FYID)
        }

        // console.log('obj.data.FYID: ', obj.data.FYID)
        // if (obj.data.FYID != '' || obj.data.FYID != undefined){
        //     fillTable2Grid(obj.data.FYID)
        // }
        //return data;
    } catch (error) {
        console.error('Error creating Financial Year:', error);
        displayErrorMessage('Failed to create Financial Year. Please try again.');
        return null;
    }
}

async function updateFinancialYear(id, departmentData) {
    try {
        const response = await fetch(`${BASE_URL}update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(departmentData),
        });
        const obj = await response.json();
        debugger
        current_finyear = obj.data;
        if (!response.ok) {
            throw new Error('Failed to update Financial Year');
        }
        //const data = await response.json();
        displaySuccessMessage('Financial Year updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating Financial Year:', error);
        displayErrorMessage('Failed to update Financial Year. Please try again.');
        return null;
    }
}

async function deleteFinancialYear(id) {
    try {
        const response = await fetch(`${BASE_URL}delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete Financial Year');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting Financial Year with ID ${id}:`, error);
        return false;
    }
}

async function updatePeriodMonth(id) {
    try {
        const response = await fetch(`${BASE_URL}updatemonth/${id}`, {
            method: 'PUT',
        });
        if (!response.ok) {
            throw new Error('Failed to Update Period Month');
        }
        return true;
    } catch (error) {
        console.error(`Error Which Activating Period Month with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllFinancialYears().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();
        current_finyear = data.find(x=>x.FYStatus == true);
       console.log('current_finyear: ', current_finyear)
        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); 
            var row = [counter, data[i].FYID, data[i].FinYear, data[i].FYStatus ? 'Active' : 'In-Active', actionButton.outerHTML];
            table.row.add(row).draw(false);
            counter++;
        }
        debugger
        if(current_finyear != undefined){
            fillTable2Grid(current_finyear.FYID);
        }
    });
}

function fillTable2Grid(id = current_finyear.FYID) {
    console.log('fillTable2Grid: ' ,id)
    getAllPayrollPeriod(id).then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table2.clear().draw();
        for (var i = 0; i < data.length; i++) {
            var actionButton = '<button class="action-btn btn-success rowperiodmonthclass">Active</button>';
        //     var row = [counter, data[i].ID, data[i].FYID, data[i].FinYear, data[i].MNTH_ID,
        //     data[i].MNTH_NO, data[i].MNTH_NAME, data[i].MNTH_SHORT_NAME, data[i].PERIOD_STATUS ? 'Active' : 'In-Active',
        //     // data[i].FianYear.FYID == current_finyear.FYID ? actionButton : ''
        // actionButton];

            var row = [counter, data[i].ID, data[i].FYID, data[i].FinYear, data[i].MNTH_ID,
            data[i].MNTH_NO, data[i].MNTH_NAME, data[i].MNTH_SHORT_NAME, data[i].PERIOD_STATUS ? 'Active' : 'In-Active',
        actionButton];

            table2.row.add(row).draw(false);
            counter++;
        }
    });
}