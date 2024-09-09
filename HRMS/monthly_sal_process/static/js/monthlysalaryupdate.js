const BASE_URL = window.location.origin;
var table, tabl2;
// const INSERT_BUTTON_ID = 'insertFormData';
// const SAVE_NEW_BUTTON_ID = 'saveNewBtnId';
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
                "className": "text-right",
            }
        ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']],
        paging: false, // Hide pagination
        searching: false, // Hide search
        lengthChange: false, // Hide page length options
        info: false, // Hide table info (e.g., "Showing 1 to 5 of 10 entries")
        dom: '<"top"i>rt<"bottom"flp><"clear">' // Position controls above the table
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
                "className": "text-right",
            }
        ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']],
        paging: false, // Hide pagination
        searching: false, // Hide search
        lengthChange: false, // Hide page length options
        info: false, // Hide table info (e.g., "Showing 1 to 5 of 10 entries")
        dom: '<"top"i>rt<"bottom"flp><"clear">' // Position controls above the table
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
    // document.getElementById("insertFormData").classList.add("d-none");
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
    document.getElementById("Emp_ID_").value = '';
    document.getElementById("Emp_Up_Date").value = '';
    document.getElementById("No_of_Children").value = '';
    document.getElementById("GrossSalary").value = '';
    document.getElementById("Remarks").value = '';
    document.getElementById("HR_Emp_ID").value = '';
    document.getElementById("Emp_ID").selectedIndex = 0;
    document.getElementById("DSG_ID").selectedIndex = 0;
    document.getElementById("Dept_ID").selectedIndex = 0;
    document.getElementById("Grade_ID").selectedIndex = 0;
    document.getElementById("Emp_Category").selectedIndex = 0;
    document.getElementById("Marital_Status").selectedIndex = 0;
    document.getElementById("updateFormData").classList.add("d-none");
    // document.getElementById("saveNewBtnId").classList.add("d-none");
    // document.getElementById("insertFormData").classList.remove("d-none");

    document.getElementById("InserRowID1").innerHTML = "";
    document.getElementById("InserRowID2").innerHTML = "";

    document.getElementById('totalAllowance_fixed_gross').innerText = `Total Allowance Fixed Gross: 0.00`
    document.getElementById('totalAllowance_fixed_additional').innerText = `Total Allowance Fixed Additional: 0.00`
    document.getElementById('totalAllowance').innerText = `Total Allowance: 0.00`
    document.getElementById('totalDeduction').innerText = `Total Deduction: 0.00`

    document.getElementById("Transfer_Type").selectedIndex = 0;
    document.getElementById("Account_No").value = '';
    document.getElementById("Bank_Name").value = '';
    document.getElementById("Stop_Salary").selectedIndex = 0;

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

// async function updateDesignation(id, departmentData) {
//     try {
//         const response = await fetch(`${BASE_URL}update/${id}`, {
//             method: 'PUT',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(departmentData),
//         });
//         if (!response.ok) {
//             throw new Error('Failed to update Grade');
//         }
//         //const data = await response.json();
//         displaySuccessMessage('Grade updated successfully!');
//         fillTableGrid();
//         //return data;
//     } catch (error) {
//         console.error('Error updating Grade:', error);
//         displayErrorMessage('Failed to update Grade. Please try again.');
//         return null;
//     }
// }

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
    // dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

// function handleInsertClick() {
//     const Grade_ID = document.getElementById("Grade_ID").value;
//     const Grade_Descr = document.getElementById("Grade_Descr").value;

//     const departmentData = {
//         Grade_ID: Grade_ID,
//         Grade_Descr: Grade_Descr
//     }
//     createDesignation(departmentData);

// }


function handleInsertClick() {

    const Emp_Up_ID = Number(document.getElementById("Emp_Up_ID").value);
    const Emp_Up_Date = document.getElementById("Emp_Up_Date").value;
    const Emp_ID = Number(document.getElementById("Emp_ID").value);
    const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value);
    const Emp_Category = document.getElementById("Emp_Category").value;
    const Dsg_ID = Number(document.getElementById("DSG_ID").value);
    const Dept_ID = Number(document.getElementById("Dept_ID").value);
    const Grade_ID = Number(document.getElementById("Grade_ID").value);
    const Marital_Status = document.getElementById("Marital_Status").value;
    const No_of_Children = Number(document.getElementById("No_of_Children").value);
    const Remarks = document.getElementById("Remarks").value;
    const Element_Descr = document.getElementById("Element_Descr").value;
    const grossSalary = Number(document.getElementById("GrossSalary").value);

    const Transfer_Type = document.getElementById("Transfer_Type").value;
    const Account_No = document.getElementById("Account_No").value;
    const Bank_Name = document.getElementById("Bank_Name").value;
    const Stop_Salary = document.getElementById("Stop_Salary").value;
    const CO_ID = document.getElementById("CO_ID").value;

    let dataArray = [];

    $("#bmGridID1 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(0) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(1) input").val();
        rowData.Amount = Number($(this).find("td:eq(2) input").val());
        rowData.Element_Type = "Allowance";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    $("#bmGridID2 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(0) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(1) input").val();
        rowData.Amount = Number($(this).find("td:eq(2) input").val());
        rowData.Element_Type = "Deduction";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    let masterData = {
        Emp_Up_ID: Emp_Up_ID,
        Emp_Up_Date: Emp_Up_Date,
        Emp_ID: Emp_ID,
        HR_Emp_ID: HR_Emp_ID,
        Emp_Category: Emp_Category,
        Dsg_ID: Dsg_ID,
        Dept_ID: Dept_ID,
        Grade_ID: Grade_ID,
        Marital_Status: Marital_Status,
        No_of_Children: No_of_Children,
        Remarks: Remarks,
        GrossSalary: grossSalary,
        Co_ID: CO_ID,
        Transfer_Type: Transfer_Type,
        Account_No: Account_No,
        Bank_Name: Bank_Name,
        Stop_Salary: Stop_Salary,
    }

    console.log("addsalarymaster masterData: ", masterData)
    console.log("addsalarymaster dataArray: ", dataArray)

    //debugger
    if (Emp_ID != 0 && Dsg_ID != 0 && Dept_ID != 0 && Grade_ID != 0 && dataArray.length != 0, Emp_Up_Date != "") {

        $.post({
            url: BASE_URL + '/salaryprocess/addsalarymaster/',
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
                'X-CSRFToken': getCookie('csrftoken')
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

    const Emp_Up_ID = Number(document.getElementById("Emp_Up_ID").value);
    const Emp_Up_Date = document.getElementById("Emp_Up_Date").value;
    const Emp_ID = Number(document.getElementById("Emp_ID").value);
    const Emp_ID_ = Number(document.getElementById("Emp_ID_").value);
    const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value);
    const Emp_Category = document.getElementById("Emp_Category").value;
    const Dsg_ID = Number(document.getElementById("DSG_ID").value);
    const Dept_ID = Number(document.getElementById("Dept_ID").value);
    const Grade_ID = Number(document.getElementById("Grade_ID").value);
    const Marital_Status = document.getElementById("Marital_Status").value;
    const No_of_Children = Number(document.getElementById("No_of_Children").value);
    const Remarks = document.getElementById("Remarks").value;
    const Element_Descr = document.getElementById("Element_Descr").value;
    const grossSalary = Number(document.getElementById("GrossSalary").value);

    const Transfer_Type = document.getElementById("Transfer_Type").value;
    const Account_No = document.getElementById("Account_No").value;
    const Bank_Name = document.getElementById("Bank_Name").value;
    const Stop_Salary = document.getElementById("Stop_Salary").value;
    const CO_ID = document.getElementById("CO_ID").value;

    let dataArray = [];

    $("#bmGridID1 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(0) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(1) input").val();
        rowData.Amount = Number($(this).find("td:eq(2) input").val());
        rowData.Element_Type = "Allowance";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    $("#bmGridID2 tbody tr").each(function () {
        var rowData = {};
        rowData.Element_ID = Number($(this).find("td:eq(0) input").attr("id"));
        rowData.Element_Category = $(this).find("td:eq(1) input").val();
        rowData.Amount = Number($(this).find("td:eq(2) input").val());
        rowData.Element_Type = "Deduction";
        if (rowData.Amount != 0)
            dataArray.push(rowData);
    });

    let masterData = {
        Emp_Up_ID: Emp_Up_ID,
        Emp_Up_Date: Emp_Up_Date,
        Emp_ID: Emp_ID,
        HR_Emp_ID: HR_Emp_ID,
        Emp_Category: Emp_Category,
        Dsg_ID: Dsg_ID,
        Dept_ID: Dept_ID,
        Grade_ID: Grade_ID,
        Marital_Status: Marital_Status,
        No_of_Children: No_of_Children,
        Remarks: Remarks,
        GrossSalary: grossSalary,
        Co_ID: CO_ID,
        Transfer_Type: Transfer_Type,
        Account_No: Account_No,
        Bank_Name: Bank_Name,
        Stop_Salary: Boolean(Stop_Salary)
    }
    // alert('update salary')
    // alert(Emp_Up_ID)
    // debugger
    if (Emp_Up_ID != 0 && Emp_ID != 0 && Dsg_ID != 0 && Dept_ID != 0 && Grade_ID != 0 && dataArray.length != 0) {

        $.post({
            // url: BASE_URL + `salaryupdate/updatesalary/${Emp_Up_ID}/`,
            url: BASE_URL + `/salaryprocess/updatesalary/${Emp_Up_ID}`,
            contentType: 'application/json',
            data: JSON.stringify({
                masterData: masterData,
                detailList: dataArray
            }),
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
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

document.getElementById("Emp_ID").addEventListener("change", function () {
    mapEmployeeDate(this.value);
})

// function mapEmployeeDate(empID) {

//     console.log('listofEmployeeNotInSalUpdate: ', listofEmployeeNotInSalUpdate);
//     const singleEmpData = listofEmployeeNotInSalUpdate.find(item => item.Emp_ID == empID);
//     console.log('singleEmpData: ', singleEmpData);
//     //debugger
//     if (singleEmpData != null && singleEmpData != 0) {
//         document.getElementById("Emp_ID").value = singleEmpData.Emp_ID;
//         document.getElementById("HR_Emp_ID").value = singleEmpData.HR_Emp_ID;
//         document.getElementById("Emp_Category").value = '';
//         document.getElementById("DSG_ID").value = singleEmpData.Joining_Dsg_ID;
//         document.getElementById("Dept_ID").value = singleEmpData.Joining_Dept_ID;
//         document.getElementById("Grade_ID").value = singleEmpData.Grade_ID;
//         document.getElementById("Marital_Status").value = singleEmpData.Marital_Status;
//     }

//     getAllDataFromDB(`${BASE_URL}payroll_element/getall/`, "Payroll Element").then((data) => {
//         console.log("Data: ", data)
//         listofPayrollElement = data;

//         let counter = 0;
//         document.getElementById("InserRowID1").innerHTML = '';
//         document.getElementById("InserRowID2").innerHTML = '';

//         for (var i = 0; i < listofPayrollElement.length; i++) {
//             if (listofPayrollElement[i].Element_Category == "Fixed") {
//                 if (listofPayrollElement[i].Element_Type == "Allowance") {
//                     document.getElementById("InserRowID1").innerHTML +=
//                         `<tr>
//                                 <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
//                                 <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
//                                 <td><input type="number" value=""  /></td></tr>`;

//                 }

//                 if (listofPayrollElement[i].Element_Type == "Deduction") {
//                     document.getElementById("InserRowID2").innerHTML +=
//                         `<tr>
//                                 <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
//                                 <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
//                                 <td><input type="number" value="" /></td></tr>`;
//                 }
//             }
//         }
//     })
//         .catch((error) => {
//             console.log("Error")
//         })
// }

function mapEmployeeDate(empID) {
    console.log('listofEmployeeNotInSalUpdate: ', listofEmployeeNotInSalUpdate);
    const singleEmpData = listofEmployeeNotInSalUpdate.find(item => item.Emp_ID == empID);
    console.log('singleEmpData: ', singleEmpData);
    //debugger
    if (singleEmpData != null && singleEmpData != 0) {
        document.getElementById("Emp_ID").value = singleEmpData.Emp_ID;
        document.getElementById("Emp_ID_").value = singleEmpData.Emp_ID;
        document.getElementById("HR_Emp_ID").value = singleEmpData.HR_Emp_ID;
        document.getElementById("Emp_Category").value = '';
        document.getElementById("DSG_ID").value = singleEmpData.Joining_Dsg_ID;
        document.getElementById("Dept_ID").value = singleEmpData.Joining_Dept_ID;
        document.getElementById("Grade_ID").value = singleEmpData.Grade_ID;
        document.getElementById("Marital_Status").value = singleEmpData.Marital_Status;
    }

    getAllDataFromDB(`${BASE_URL}/payroll_element/getall/`, "Payroll Element").then((data) => {
        console.log("Data: ", data)
        listofPayrollElement = data;

        let counter = 0;
        document.getElementById("InserRowID1").innerHTML = '';
        document.getElementById("InserRowID2").innerHTML = '';

        let totalAllowance = 0;
        let totalDeduction = 0;

        for (var i = 0; i < listofPayrollElement.length; i++) {
            if (listofPayrollElement[i].Element_Category == "Fixed") {
                if (listofPayrollElement[i].Element_Type == "Allowance") {
                    let allowanceAmount = document.createElement('input');
                    allowanceAmount.setAttribute('type', 'number');
                    allowanceAmount.setAttribute('value', '');
                    allowanceAmount.setAttribute('class', 'allowanceInput');

                    document.getElementById("InserRowID1").innerHTML +=
                        `<tr>
                                <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
                                <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
                                <td><input type="number" value="" class="allowanceInput" /></td></tr>`;
                }

                if (listofPayrollElement[i].Element_Type == "Deduction") {
                    let deductionAmount = document.createElement('input');
                    deductionAmount.setAttribute('type', 'number');
                    deductionAmount.setAttribute('value', '');
                    deductionAmount.setAttribute('class', 'deductionInput');

                    document.getElementById("InserRowID2").innerHTML +=
                        `<tr>
                                <td><input type="text" id="${listofPayrollElement[i].Element_ID}" value="${listofPayrollElement[i].Element_Name}" readonly /></td>
                                <td><input type="text" value="${listofPayrollElement[i].Element_Category}" readonly /></td>
                                <td><input type="number" value="" class="deductionInput" /></td></tr>`;
                }
            }
        }
        // Calculate total after elements are added
        calculateTotal();
    })
        .catch((error) => {
            console.log("Error")
        })
}

// Event delegation for dynamic elements
document.addEventListener('focusout', function (e) {
    if (e.target.classList.contains('allowanceInput') || e.target.classList.contains('deductionInput')) {
        calculateTotal();
    }
});

function calculateTotal() {
    // alert()
    let allowanceInputs = document.querySelectorAll('.allowanceInput');
    let deductionInputs = document.querySelectorAll('.deductionInput');
    let allowanceTotal = 0;
    let deductionTotal = 0;
    let totalAllowance_fixed_gross = 0, totalAllowance_fixed_additional = 0;

    allowanceInputs.forEach(input => {
        allowanceTotal += parseFloat(input.value) || 0;
    });

    deductionInputs.forEach(input => {
        deductionTotal += parseFloat(input.value) || 0;
    });

    $("#bmGridID1 tbody tr").each(function () {
        const Element_Allowance = $(this).find("td:eq(0) input").val();
        const Element_Category = $(this).find("td:eq(1) input").val();
        const Element_Amount = $(this).find("td:eq(2) input").val();

        console.log('Element_Category: ', Element_Category)

        if (Element_Category == 'Fixed Gross') {
            totalAllowance_fixed_gross += Number(Element_Amount);
        }
        if (Element_Category == 'Fixed Additional') {
            totalAllowance_fixed_additional += Number(Element_Amount);
        }
    })

    document.getElementById("totalAllowance_fixed_gross").innerHTML = `Total Allowance Fixed Gross: ${totalAllowance_fixed_gross.toFixed(2)}`
    document.getElementById("totalAllowance_fixed_additional").innerHTML = `Total Allowance Fixed Additional: ${totalAllowance_fixed_additional.toFixed(2)}`


    // document.getElementById("totalAllowance_fixed_gross").innerHTML = `Total Allowance Fixed Gross: ${totalAllowance_fixed_gross}`
    // document.getElementById("totalAllowance_fixed_additional").innerHTML = `Total Allowance Fixed Additional: ${totalAllowance_fixed_additional}`

    document.getElementById('totalAllowance').innerText = `Total Allowance: ${allowanceTotal.toFixed(2)}`
    document.getElementById('totalDeduction').innerText = `Total Deduction: ${deductionTotal.toFixed(2)}`
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
    getAllDataFromDB(`${BASE_URL}/grade/getall`, 'Grade').then((data) => {
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

document.getElementById("calculateGrossSalary").addEventListener('click', function () {

    const grossSalary = Number(document.getElementById("GrossSalary").value);
    // debugger
    var totalRows = Number($('#InserRowID1 tr').length);

    // alert('totalRows: ', totalRows)
    if (grossSalary != 0 && totalRows != 0) {
        $("#bmGridID1 tbody tr").each(function () {
            const elementID = Number($(this).find("td:eq(0) input").attr("id"));
            if (elementID == 1) {
                const amount = (grossSalary / 100) * 58.5;
                $(this).find("td:eq(2) input").val(amount.toFixed(2));
            }
            if (elementID == 2) {
                const amount = (grossSalary / 100) * 6.5;

                $(this).find("td:eq(2) input").val(amount.toFixed(2));
            }
            if (elementID == 5) {
                const amount = (grossSalary / 100) * 29;

                $(this).find("td:eq(2) input").val(amount.toFixed(2));
            }
            if (elementID == 6) {
                const amount = (grossSalary / 100) * 6;

                $(this).find("td:eq(2) input").val(amount.toFixed(2));
            }
        });

        $("#bmGridID2 tbody tr").each(function () {
            const elementID = Number($(this).find("td:eq(0) input").attr("id"));
            if (elementID == 17) {
                $(this).find("td:eq(2) input").val(130);
            }
        });
    }

    calculateTotal();

});

// async function fillPayrollElementTableGrid(empID, empUpID) {
//     try {
//         const response = await fetch(`${BASE_URL}/salaryprocess/payrollelement/${empUpID}/${empID}/`, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         });
//         if (!response.ok) {  
//             throw new Error(`Failed to fetch Payroll Element`);
//         }
//         const data = await response.json();
//         console.log("data: ", data)
//         listofPayrollElement = data;
//         table4.clear().draw();
//         allowance_grid = document.querySelectorAll('.bmGridID1')
//         deduction_grid = document.querySelectorAll('.bmGridID2')
//         for (var i = 0; i < data.length; i++) {
//             for (var j = 0; j < allowance_grid.length; j++) {
//                 if (allowance_grid) {
//                     if (data[i].ElemenT_NAME != allowance_grid[0].value) {
//                         table4.row.add([data[i].Element_ID, data[i].Element_Name, data[i].Element_Type, data[i].Element_Category]).draw(false);
//                     }
//                 } if (deduction_grid) {
//                     if (data[i].ElemenT_NAME != deduction_grid[0].value) {
//                         table4.row.add([data[i].Element_ID, data[i].Element_Name, data[i].Element_Type, data[i].Element_Category]).draw(false);
//                     }
//                 } else {
//                     table4.row.add([data[i].Element_ID, data[i].Element_Name, data[i].Element_Type, data[i].Element_Category]).draw(false);
//                 }
//             }
//         }
//         // document.getElementById("Element_Descr").innerHTML = temp;
//     } catch (error) {
//         console.error(`Error fetching Payroll Element:`, error);
//         return null;
//     }
// }


async function fillPayrollElementTableGrid(empID, empUpID) {
    try {
        const response = await fetch(`${BASE_URL}/salaryprocess/payrollelement/${empUpID}/${empID}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`Failed to fetch Payroll Element`);
        }

        const data = await response.json();
        console.log("data: ", data);
        listofPayrollElement = data;

        // Clear the table before adding new rows
        table4.clear().draw();

        // Get the current allowance and deduction values from the first column of input fields
        const allowance_grid = document.querySelectorAll('#InserRowID1 tr td:first-child input[type="text"]');
        const deduction_grid = document.querySelectorAll('#InserRowID2 tr td:first-child input[type="text"]');

        // Use sets to store existing allowance and deduction values for fast lookup
        const existingAllowances = new Set();
        const existingDeductions = new Set();

        // Collect values from the first column input fields
        allowance_grid.forEach(function(input) {
            console.log('allowance_grid input value: ', input.id)
            existingAllowances.add(Number(input.id));
        });

        deduction_grid.forEach(function(input) {
            console.log('deduction_grid input value: ', input.id)
            existingDeductions.add(Number(input.id));
        });

        // Loop through fetched data
        data.forEach(function(item) {
            const elementID = item.Element_ID;

            console.log('elementID: ', elementID)
            console.log('existingAllowances: ', existingAllowances)
            console.log('existingDeductions: ', existingDeductions)

            // Add the row to table4 only if it doesn't exist in either allowance or deduction grids
            if (!existingAllowances.has(elementID) && !existingDeductions.has(elementID)) {
                table4.row.add([
                    item.Element_ID,
                    item.Element_Name,
                    item.Element_Type,
                    item.Element_Category
                ]).draw(false);
            }
        });

    } catch (error) {
        console.error(`Error fetching Payroll Element:`, error);
        return null;
    }
}


function fillCompaniestTableGrid() {
    getAllDataFromDB(`${BASE_URL}/employee/group-of-companies`, 'Companies').then((data) => {
        console.log("companies: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].CoID}">${data[i].CoName}</option>`
        }
        document.getElementById("CO_ID").innerHTML = temp;
    });
}

function fillDepartmentTableGrid() {
    getAllDataFromDB(`${BASE_URL}/department/getall`, 'Department').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].Dept_ID}">${data[i].Dept_Descr}</option>`
        }
        document.getElementById("Dept_ID").innerHTML = temp;
    });
}

function fillDesignationTableGrid() {
    getAllDataFromDB(`${BASE_URL}/designation/getall`, 'Designation').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].DSG_ID}">${data[i].DSG_Descr}</option>`
        }
        document.getElementById("DSG_ID").innerHTML = temp;
    });
}

// function fillSalaryMasterTableGrid() {
    
//     const payroll_id = document.getElementById("Search_Payroll_ID").value;

//     if(payroll_id != '' || payroll_id != undefined){
//         getAllDataFromDB(`${BASE_URL}/salaryprocess/getllmaster/${payroll_id}`, 'Monthly Salary Update Master').then((data) => {
//             console.log("fillSalaryMasterTableGrid response: ", data);
//             var temp = '';
//             table5.clear().draw();
//             for (var i = 0; i < data.length; i++) {
//                 // temp += `<option value="${data[i].Emp_ID}">${data[i].Emp_Name}</option>`;
//                 table5.row.add([data[i].Emp_Up_ID, data[i].Emp_ID, data[i].HR_Emp_ID, data[i].Emp_Name
//                     , data[i].Dsg_Descr, data[i].Dept_Descr, data[i].Emp_Up_Date]).draw(false);
//             }
//             // document.getElementById("Emp_Up_ID2").innerHTML = temp;
//         });
//     }
//     else{
//         alert("Kindly Select payroll period first!")
//     }
// }

function fillSalaryMasterTableGrid() {
    const payroll_id = Number(document.getElementById("Search_Payroll_ID").value);

    console.log('payroll_id: ', payroll_id)

    if (payroll_id && payroll_id !== '') {
        getAllDataFromDB(`${BASE_URL}/salaryprocess/getallmaster/${payroll_id}/`, 'Monthly Salary Update Master')
            .then((data) => {
                console.log("fillSalaryMasterTableGrid response: ", data);
                table5.clear().draw();
                for (let i = 0; i < data.length; i++) {
                    table5.row.add([
                        data[i].Emp_Up_ID,
                        data[i].Emp_ID,
                        data[i].HR_Emp_ID,
                        data[i].Emp_Name,
                        data[i].Dsg_Descr,
                        data[i].Dept_Descr,
                        data[i].Emp_Up_Date
                    ]).draw(false);
                }
            })
            .catch((error) => {
                console.error("Error fetching data: ", error);
                alert("Failed to fetch data. Please try again later.");
            });
    } else {
        alert("Kindly Select payroll period first!");
    }
}

function fillEmployeeTableGrid() {
    getAllDataFromDB(`${BASE_URL}/employee/getall`, 'Employee').then((data) => {
        // console.log("response: ", data);
        var temp = '';
        listofEmployeeNotInSalUpdate = data;
        // Sort the list of objects by name in ascending order
        listofEmployeeNotInSalUpdate.sort((a, b) => {
            if (a.Emp_Name < b.Emp_Name) {  
                return -1;
            }
            if (a.name > b.name) {
                return 1;
            }
            return 0;
        });
        for (var i = 0; i < data.length; i++) {
            temp += `<option value="${data[i].Emp_ID}">${data[i].Emp_Name}</option>`
            // temp += `<option value="${data[i].Emp_ID}">${data[i].Emp_Name} - ${data[i].HR_Emp_ID}</option>`
        }
        document.getElementById("Emp_ID").innerHTML = temp;
    });
}

function handleTableRowClick3() {

    const Emp_Up_ID = Number($(this).find('td')[0].innerHTML);
    const Emp_ID = Number($(this).find('td')[1].innerHTML);

    const payroll_id = Number(document.getElementById("Search_Payroll_ID").value);
    console.log('payroll_id: ', payroll_id)

    GetAll_Salary_update_BYID(Emp_Up_ID, Emp_ID, payroll_id);

    $("#orangeModalSubscription4").modal('hide');

    // document.getElementById("insertFormData").classList.add("d-none");
    // document.getElementById("saveNewBtnId").classList.remove("d-none");
    document.getElementById("updateFormData").classList.remove("d-none");
}

function GetAll_Salary_update_BYID(emp_up_Id, empId, payroll_id) {
    console.log("emp_up_Id: ", emp_up_Id)
    console.log("empId: ", empId)
    console.log("payroll_id: ", payroll_id)
    getAllDataFromDB(`${BASE_URL}/salaryprocess/getallmasterbyid/${emp_up_Id}/${empId}/${payroll_id}`, 'Salary Master').then((data) => {
        console.log("GetAll_Salary_update_BYID response: ", data);

        document.getElementById("Emp_Up_ID").value = data[0].Emp_Up_ID;
        // document.getElementById("Emp_Up_ID2").value = data[0].Emp_Up_ID;
        document.getElementById("Emp_Up_Date").value = moment(data[0].Emp_Up_Date).format("YYYY-MM-DD");
        document.getElementById("Emp_ID_").value = data[0].Emp_ID;
        document.getElementById("Emp_ID").value = data[0].Emp_ID;
        document.getElementById("HR_Emp_ID").value = data[0].HR_Emp_ID;
        // document.getElementById("Emp_Name").value = data[0].Emp_Name;
        // document.getElementById("Emp_Category").value = "";
        document.getElementById("DSG_ID").value = data[0].Dsg_ID;
        document.getElementById("Dept_ID").value = data[0].Dept_ID;
        document.getElementById("Grade_ID").value = data[0].Grade_ID;
        document.getElementById("Marital_Status").value = data[0].Marital_Status;
        document.getElementById("No_of_Children").value = data[0].No_of_Children;
        document.getElementById("Remarks").value = data[0].Remarks;
        document.getElementById("GrossSalary").value = data[0].GrossSalary;

        document.getElementById("Transfer_Type").value = data[0].Transfer_Type;
        document.getElementById("Account_No").value = data[0].Account_No;
        document.getElementById("Bank_Name").value = data[0].Bank_Name;
        document.getElementById("Stop_Salary").value = data[0].Stop_Salary ? 1 : 0;
        document.getElementById("CO_ID").value = data[0].Co_ID;
        // document.getElementById("Payroll_ID").value = data[0].Payroll_Name;

        document.getElementById("InserRowID1").innerHTML = '';
        document.getElementById("InserRowID2").innerHTML = '';

        let allowanceRow = '', deductionRow = '';
        let counter = 1, totalAllowance = 0, totalDeduction = 0, totalAllowance_fixed_gross = 0, totalAllowance_fixed_additional = 0;

        for (var i = 0; i < data.length; i++) {

            if (data[i].Element_Type == 'Allowance' && data[i].Element_Category == 'Fixed Gross') {
                totalAllowance_fixed_gross += data[i].Amount;
            }
            if (data[i].Element_Type == 'Allowance' && data[i].Element_Category == 'Fixed Additional') {
                totalAllowance_fixed_additional += data[i].Amount;
            }
            if (data[i].Element_Type == 'Allowance') {
                allowanceRow += `<tr>
                        <td><input type="text" id="${data[i].Element_ID}" value="${data[i].Element_Name}" readonly /></td>
                        <td><input type="text" value="${data[i].Element_Category}" readonly /></td>
                        <td><input type="text" style="text-align: right;" class="allowanceInput" value="${data[i].Amount.toFixed(2)}" /></td></tr>`;
                totalAllowance += data[i].Amount;
            }
            if (data[i].Element_Type == 'Deduction') {
                deductionRow += `<tr>
                        <td><input type="text" id="${data[i].Element_ID}" value="${data[i].Element_Name}" readonly /></td>
                        <td><input type="text" value="${data[i].Element_Category}" readonly /></td>
                        <td><input type="text" style="text-align: right;" class="deductionInput" value="${data[i].Amount.toFixed(2)}" /></td></tr>`;
                totalDeduction += data[i].Amount;
            }
            counter++;
        }
        // console.log("allowanceRow: ", allowanceRow)
        // console.log("deductionRow: ", deductionRow)
        document.getElementById("InserRowID1").innerHTML = allowanceRow;
        document.getElementById("InserRowID2").innerHTML = deductionRow;

        document.getElementById("totalAllowance").innerHTML = `Total Allowance: ${totalAllowance.toFixed(2)}`
        document.getElementById("totalDeduction").innerHTML = `Total Deduction: ${totalDeduction.toFixed(2)}`

        document.getElementById("totalAllowance_fixed_gross").innerHTML = `Total Allowance Fixed Gross: ${totalAllowance_fixed_gross.toFixed(2)}`
        document.getElementById("totalAllowance_fixed_additional").innerHTML = `Total Allowance Fixed Additional: ${totalAllowance_fixed_additional.toFixed(2)}`


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
        var temp =
            `<tr>
                <td><input type="text" id="${ElemenT_ID}" value="${ElemenT_NAME}" readonly /></td>
                <td><input type="text" value="${ElemenT_CATEGORY}" readonly /></td>
                <td><input type="text" style="text-align: right" value="" /></td></tr>`;
        $("#InserRowID1").append(temp);
    }
    if (ElemenT_TYPE == "Deduction") {
        var temp =
            `<tr>
                <td><input type="text" id="${ElemenT_ID}" value="${ElemenT_NAME}" readonly /></td>
                <td><input type="text" value="${ElemenT_CATEGORY}" readonly /></td>
                <td><input type="text" style="text-align: right" value="" /></td></tr>`;
        $("#InserRowID2").append(temp);
    }

    $("#orangeModalSubscription3").modal('hide');
}

function get_active_period() {
    getAllDataFromDB(`${BASE_URL}/salaryprocess/get_active_period`, 'Payroll Period').then((data) => {
        console.log("getall_payrollperiod response: ", data);
        var temp = `<option value="${data.PAYROLL_ID}">${data.MNTH_NAME} - ${data.FinYear}</option>`
        // var temp = `${data.MNTH_NAME} - ${data.FinYear}`
        document.getElementById("Search_Payroll_ID").innerHTML = temp;
    });
}

$(document).ready(function () {
    initializeDataTable();

    document.getElementById('Emp_Up_Date').valueAsDate = new Date();

    get_active_period()
    fillCompaniestTableGrid()
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
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick);
    // document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    // document.getElementById(SAVE_NEW_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    // fillTableGrid()
})
