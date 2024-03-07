const API_URL = 'http://localhost:8000/';
var table, tabl2;
const INSERT_BUTTON_ID = 'insertFormData';
const SAVE_NEW_BUTTON_ID = 'saveNewBtnId';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';

function initializeDataTable() {
    table = $('#bmGridID1').DataTable({
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
    table2 = $('#bmGridID2').DataTable({
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

    table4 = $('#GridID4').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
        pageLength: 5,
        'columnDefs': [
            {
                "targets": 1,
                "className": "text-left",
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
    document.getElementById("Emp_Up_ID").value = '';
    document.getElementById("Emp_Up_Date").value = '';
    document.getElementById("No_of_Children").value = '';
    document.getElementById("GrossSalary").value = '';
    document.getElementById("Remarks").value = '';
    document.getElementById("Emp_ID").selectedIndex = 0;
    document.getElementById("DSG_ID").selectedIndex = 0;
    document.getElementById("Dept_ID").selectedIndex = 0;
    document.getElementById("Grade_ID").selectedIndex = 0;
    document.getElementById("Emp_Category").selectedIndex = 0;
    document.getElementById("Marital_Status").selectedIndex = 0;
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");

    document.getElementById("InserRowID1").innerHTML = "";
    document.getElementById("InserRowID2").innerHTML = "";
}

async function getDesignationById(id) {
    try {
        const response = await fetch(`${BASE_URL}${id}/`);
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
        const response = await fetch(`${BASE_URL}add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
        const response = await fetch(`${BASE_URL}update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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
        const response = await fetch(`${BASE_URL}delete/${id}`, {
            method: 'DELETE',
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
    dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleInsertClick() {
    const Grade_ID = document.getElementById("Grade_ID").value;
    const Grade_Descr = document.getElementById("Grade_Descr").value;

    const departmentData = {
        Grade_ID: Grade_ID,
        Grade_Descr: Grade_Descr
    }
    createDesignation(departmentData);

}


function handleInsertClick() {

    const Emp_Up_ID = Number(document.getElementById("Emp_Up_ID").value);
    const Emp_Up_Date = document.getElementById("Emp_Up_Date").value;
    const Emp_ID = Number(document.getElementById("Emp_ID").value);
    const Emp_Category = document.getElementById("Emp_Category").value;
    const Dsg_ID = Number(document.getElementById("DSG_ID").value);
    const Dept_ID = Number(document.getElementById("Dept_ID").value);
    const Grade_ID = Number(document.getElementById("Grade_ID").value);
    const Marital_Status = document.getElementById("Marital_Status").value;
    const No_of_Children = Number(document.getElementById("No_of_Children").value);
    const Remarks = document.getElementById("Remarks").value;
    const Element_Descr = document.getElementById("Element_Descr").value;
    const grossSalary = Number(document.getElementById("GrossSalary").value);

    let dataArray = [];

    $("#bmGridID1 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(1) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(2) input").val();
        rowData.Amount = Number($(this).find("td:eq(3) input").val());
        rowData.Element_Type = "Allowance";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    $("#bmGridID2 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(1) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(2) input").val();
        rowData.Amount = Number($(this).find("td:eq(3) input").val());
        rowData.Element_Type = "Deduction";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    let masterData = {
        Emp_Up_ID: Emp_Up_ID,
        Emp_Up_Date: Emp_Up_Date,
        Emp_ID: Emp_ID,
        Emp_Category: Emp_Category,
        Dsg_ID: Dsg_ID,
        Dept_ID: Dept_ID,
        Grade_ID: Grade_ID,
        Marital_Status: Marital_Status,
        No_of_Children: No_of_Children,
        Remarks: Remarks,
        GrossSalary: grossSalary,
    }

    //debugger
    if (Emp_ID != 0 && Dsg_ID != 0 && Dept_ID != 0 && Grade_ID != 0 && dataArray.length != 0 && grossSalary != 0) {

        $.post({
            url: API_URL + 'salaryupdate/addsalarymaster/',
            contentType: 'application/json',
            data: JSON.stringify({
                masterData: masterData,
                detailList: dataArray
            }),
            dataType: 'json',
            headers: {
                // "authorization": authorization,
                // "companyID": companyID,
                // "MenuId": MenuId,
                // "FormId": FormId
            },
            success: function (response) {
                displaySuccessMessage("Salary Successfully Updated")
            },
            error: function (error) {
                displayErrorMessage("Fail to Update Salary")
                console.log(error);
            }
        });
    } else {
        displayErrorMessage("Please Fill Correct Data")
    }
}

function handleUpdateClick() {
    const Grade_ID = document.getElementById("Grade_ID").value;
    const Grade_Descr = document.getElementById("Grade_Descr").value;

    const departmentData = {
        Grade_ID: Grade_ID,
        Grade_Descr: Grade_Descr
    }
    updateDesignation(Grade_ID, departmentData);
    // fillTableGrid();
}

document.getElementById("Emp_ID").addEventListener("change", function () {
    mapEmployeeDate(this.value);
})

function mapEmployeeDate(empID) {
    
    console.log('listofEmployeeNotInSalUpdate: ', listofEmployeeNotInSalUpdate);
    const singleEmpData = listofEmployeeNotInSalUpdate.find(item => item.Emp_ID == empID);
    console.log('singleEmpData: ', singleEmpData);
    //debugger
    if (singleEmpData != null && singleEmpData != 0) {
        document.getElementById("Emp_ID").value = singleEmpData.Emp_ID;
        document.getElementById("Emp_Category").value = '';
        document.getElementById("DSG_ID").value = singleEmpData.Joining_Dsg_ID;
        document.getElementById("Dept_ID").value = singleEmpData.Joining_Dept_ID;
        document.getElementById("Grade_ID").value = singleEmpData.Grade_ID;
        document.getElementById("Marital_Status").value = singleEmpData.Marital_Status;
    }

    getAllDataFromDB(`${API_URL}payrollelement/api/getall/`, "Payroll Element").then((data) => {
        console.log("Data: ", data)
        listofPayrollElement = data;

        let counter = 0;
        document.getElementById("InserRowID1").innerHTML = '';
        document.getElementById("InserRowID2").innerHTML = '';

        for (var i = 0; i < listofPayrollElement.length; i++) {
            if (listofPayrollElement[i].Element_Category == "Fixed") {
                if (listofPayrollElement[i].Element_Type == "Allowance") {
                    document.getElementById("InserRowID1").innerHTML +=
                        `<tr><td>${counter++}</td>
                                <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
                                <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
                                <td><input type="number" value=""  /></td></tr>`;
                }
                if (listofPayrollElement[i].Element_Type == "Deduction") {
                    document.getElementById("InserRowID2").innerHTML +=
                        `<tr><td>${counter++}</td>
                                <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
                                <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
                                <td><input type="number" value="" /></td></tr>`;
                }
            }
        }

    })
    .catch((error) => {
        console.log("Error")
    })

    

}

async function getAllDataFromDB(url, name) {
    try {
        const response = await fetch(`${url}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${name}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching ${name}:`, error);
        return null;
    }
}

function fillGradeTableGrid() {
    getAllDataFromDB(`${API_URL}grade/api/getall`, 'Grade').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].Grade_ID}">${data[i].Grade_Descr}</option>`
        }
        document.getElementById("Grade_ID").innerHTML = temp;
    });
}

document.getElementById("elementGridIconId").addEventListener("click", function () {
    let Emp_Up_ID_ = Number(document.getElementById("Emp_Up_ID").value);
    let Emp_ID_ = Number(document.getElementById("Emp_ID").value);
    fillPayrollElementTableGrid(Emp_ID_, Emp_Up_ID_);
});

async function fillPayrollElementTableGrid(empID, empUpID) {
    try {
        const response = await fetch(`${API_URL}salaryupdate/payrollelement/${empID}/${empUpID}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch Payroll Element`);
        }
        const data = await response.json();
        console.log("data: ", data)
        listofPayrollElement = data;
        table4.clear().draw();
        for (var i = 0; i < data.length; i++) {
            table4.row.add([data[i].Element_ID, data[i].Element_Name, data[i].Element_Type, data[i].Element_Category]).draw(false);
        }
        // document.getElementById("Element_Descr").innerHTML = temp;
    } catch (error) {
        console.error(`Error fetching Payroll Element:`, error);
        return null;
    }
}

function fillDepartmentTableGrid() {
    getAllDataFromDB(`${API_URL}department/api/getall`, 'Department').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].Dept_ID}">${data[i].Dept_Descr}</option>`
        }
        document.getElementById("Dept_ID").innerHTML = temp;
    });
}


function fillDesignationTableGrid() {
    getAllDataFromDB(`${API_URL}designation/api/getall`, 'Designation').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].DSG_ID}">${data[i].DSG_Descr}</option>`
        }
        document.getElementById("DSG_ID").innerHTML = temp;
    });
}

function fillSalaryMasterTableGrid() {
    getAllDataFromDB(`${API_URL}salaryupdate/getllmaster/`, 'Salary Update Master').then((data) => {
        console.log("response: ", data);
        var temp = '';
        table5.clear().draw();
        for (var i = 0; i < data.length; i++) {
            // temp += `<option value="${data[i].Emp_ID}">${data[i].Emp_Name}</option>`;
            table5.row.add([data[i].Emp_Up_ID, data[i].Emp_ID, data[i].HR_Emp_ID, data[i].Emp_Name
                , data[i].Dsg_Descr, data[i].Dept_Descr, data[i].Emp_Up_Date]).draw(false);
        }
        // document.getElementById("Emp_Up_ID2").innerHTML = temp;
    });
}

function fillEmployeeTableGrid() {
    getAllDataFromDB(`${API_URL}employee/api/getall`, 'Employee').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        listofEmployeeNotInSalUpdate = data;
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].Emp_ID}">${data[i].Emp_Name} - ${data[i].HR_Emp_ID}</option>`
        }
        document.getElementById("Emp_ID").innerHTML = temp;
    });
}

function handleTableRowClick3() {

    const Emp_Up_ID = $(this).find('td')[0].innerHTML;
    const Emp_ID = $(this).find('td')[1].innerHTML;

    GetAll_Salary_update_BYID(Emp_Up_ID, Emp_ID);

    $("#orangeModalSubscription4").modal('hide');
}

function GetAll_Salary_update_BYID(emp_up_Id, empId) {

    getAllDataFromDB(`${API_URL}salaryupdate/getallmasterbyid/${emp_up_Id}/${empId}/`, 'Salary Master').then((data) => {
        console.log("response: ", data);

        document.getElementById("Emp_Up_ID").value = data[0].Emp_Up_ID;
        document.getElementById("Emp_Up_Date").value = moment(data[0].Emp_Up_Date).format("YYYY-MM-DD");
        document.getElementById("Emp_ID").value = data[0].Emp_ID;
        // document.getElementById("Emp_Name").value = data[0].Emp_Name;
        // document.getElementById("Emp_Category").value = "";
        document.getElementById("DSG_ID").value = data[0].Dsg_ID;
        document.getElementById("Dept_ID").value = data[0].Dept_ID;
        document.getElementById("Grade_ID").value = data[0].Grade_ID;
        document.getElementById("Marital_Status").value = data[0].Marital_Status;
        document.getElementById("No_of_Children").value = data[0].No_of_Children;
        document.getElementById("Remarks").value = data[0].Remarks;

        let allowanceRow = '', deductionRow = '';
        let counter = 1, totalAllowance = 0, totalDeduction = 0;

        for (var i = 0; i < data.length; i++) {
            if (data[i].Element_Type == 'Allowance') {

                allowanceRow += `<tr><td>${counter}</td>
                        <td><input type="text" id="${data[i].Element_ID}" value="${data[i].Element_Name}" readonly /></td>
                        <td><input type="text" value="${data[i].Element_Category}" readonly /></td>
                        <td><input type="text" value="${data[i].Amount}" /></td></tr>`;
                totalAllowance += data[i].Amount;
            }
            if (data[i].Element_Type == 'Deduction') {
                deductionRow += `<tr><td>${counter}</td>
                        <td><input type="text" id="${data[i].Element_ID}" value="${data[i].Element_Name}" readonly /></td>
                        <td><input type="text" value="${data[i].Element_Category}" readonly /></td>
                        <td><input type="text" value="${data[i].Amount}" /></td></tr>`;
                totalDeduction += data[i].Amount;
            }
            counter++;
        }
        console.log("allowanceRow: ", allowanceRow)
        console.log("deductionRow: ", deductionRow)
        document.getElementById("InserRowID1").innerHTML = allowanceRow;
        document.getElementById("InserRowID2").innerHTML = deductionRow;

    });

}


document.getElementById("empupdateGridIconId").addEventListener("click", function () {
    fillSalaryMasterTableGrid();
});

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


function handleTableRowClick2() {

    const ElemenT_ID = $(this).find('td')[0].innerHTML;
    const ElemenT_NAME = $(this).find('td')[1].innerHTML;
    const ElemenT_TYPE = $(this).find('td')[2].innerHTML;
    const ElemenT_CATEGORY = $(this).find('td')[3].innerHTML;

    document.getElementById("Element_Descr").value = ElemenT_NAME;

    if (ElemenT_TYPE == "Allowance") {
        document.getElementById("InserRowID1").innerHTML +=
            `<tr><td></td>
                            <td><input type="text" id="${ElemenT_ID}" value="${ElemenT_NAME}" readonly /></td>
                            <td><input type="text" value="${ElemenT_CATEGORY}" readonly /></td>
                            <td><input type="text" value="" /></td></tr>`;
    }
    if (ElemenT_TYPE == "Deduction") {
        document.getElementById("InserRowID2").innerHTML +=
            `<tr><td></td>
                            <td><input type="text" id="${ElemenT_ID}" value="${ElemenT_NAME}" readonly /></td>
                            <td><input type="text" value="${ElemenT_CATEGORY}" readonly /></td>
                            <td><input type="text" value="" /></td></tr>`;
    }

    $("#orangeModalSubscription3").modal('hide');
}



$(document).ready(function () {
    initializeDataTable();

    fillDepartmentTableGrid()
    fillDesignationTableGrid()
    fillEmployeeTableGrid()
    fillGradeTableGrid()
    // fillPayrollElementTableGrid()
    document.getElementById("InserRowID1").innerHTML = "";
    document.getElementById("InserRowID2").innerHTML = "";

    $('#GridID4 tbody').on('click', 'tr', handleTableRowClick2);
    $('#GridID5 tbody').on('click', 'tr', handleTableRowClick3);

    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    // fillTableGrid()
});
