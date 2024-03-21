const BASE_URL = '/';
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
        deleteUserPrivileges(Grade_ID).then(success => {
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
    document.getElementById("Search_User").selectedIndex = 0;
    document.getElementById("User_ID").value = 0;
    document.getElementById("User_Emp_Code").value = '';
    document.getElementById("User_Name").value = '';
    document.getElementById("User_Password").value = '';
    document.getElementById("User_Designation").selectedIndex = 0;
    document.getElementById("User_NICNo").value = '';
    document.getElementById("User_Email").value = '';
    document.getElementById("Confirm_Password").value = '';
    document.getElementById("PTCL_No").value = '';
    document.getElementById("Cell_No").value = '';
    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");
}

async function getAllUserPrivileges(userid) {
    try {
        console.log('userid: ', userid)
        const response = await fetch(`${BASE_URL}administration/api/userprivileges/getall/${userid}`);
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

async function getAllCompanies() {
    try {
        const response = await fetch(`${BASE_URL}administration/api/company/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch Companies');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching Companies:', error);
        return null;
    }
}

async function getAllFormDescription() {
    try {
        const response = await fetch(`${BASE_URL}administration/api/formdescription/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch formdescription');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching formdescription:', error);
        return null;
    }
}

async function getAllDesignation() {
    try {
        const response = await fetch(`${BASE_URL}designation/api/getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch designation');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching designation:', error);
        return null;
    }
}

async function getAllUserFromDB() {
    try {
        const response = await fetch(`${BASE_URL}login/api/getalluser`);
        if (!response.ok) {
            throw new Error('Failed to fetch designation');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching designation:', error);
        return null;
    }
}

function fillUserDropDown() {
    let temp = '';
    getAllUserFromDB().then((data) => {
        data.forEach(element => {
            temp += `<option value="${element.User_ID}">${element.User_Name}</option>`;
        });
        document.getElementById("Search_User").innerHTML = temp;
    })
}

async function getUserPrivilegesById(id) {
    try {
        const response = await fetch(`${BASE_URL}${id}`);
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

async function createUserPrivileges(formData) {
    try {
        const response = await fetch(`${BASE_URL}administration/api/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
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

async function updateUserPrivileges(id, departmentData) {
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

async function deleteUserPrivileges(id) {
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



document.getElementById("addFormDescription").addEventListener('click', function () {
    getAllFormDescription().then((data) => {
        console.log('form description: ', data);
        let companiesSelect = '<select class="form-control form-control-sm" id="companies"><option value="1">iTecknologi Tracking</option></select>';
        let formStatusCodeSelect = `<select class="form-control form-control-sm" id="formStatusCode">
                <option value="3">Add And Update</option>
                <option value="1">Add</option>
                <option value="2">Update</option>
                <option value="0">View</option>
                </select>`;
        let formStatusCheckBox = `<input type="checkbox" class="FormCheckBox1" name="FormCheckBox" checked id="formId1">`;
        var counter = 1;
        if (data && data.length > 0) { // Check if data is not null and not empty
            table.clear().draw();
            for (var i = 0; i < data.length; i++) {
                var row = [
                    counter,
                    data[i].FormID,
                    data[i].FormDescr,
                    data[i].ModuleDescr,
                    data[i].MnuDescr,
                    data[i].MnuSubDescr,
                    data[i].FormType,
                    formStatusCodeSelect,
                    formStatusCheckBox,
                    companiesSelect
                ];
                table.row.add(row).draw(false);
                counter++;
            }
        } else {
            console.log('No data found');
        }
    });
});

document.getElementById("Search_User").addEventListener('change', function () {
    -getAllUserPrivileges(this.value).then((data) => {
        console.log('getAllUserPrivileges: ', data);
        // let formStatusCodeSelect = `<select class="form-control form-control-sm" id="formStatusCode">
        //                             <option value="3">Add And Update</option>
        //                             <option value="1">Add</option>
        //                             <option value="2">Update</option>
        //                             <option value="0">View</option>
        //                             </select>`;
        let formStatusCheckBox = `<input type="checkbox" class="FormCheckBox1" name="FormCheckBox" checked id="formId1">`;
        let companiesSelect = '<select class="form-control form-control-sm" id="companies"><option value="1">iTecknologi Tracking</option></select>';
        var counter = 1;
        if (data && data.length > 0) {
            document.getElementById("Search_User").selectedIndex = 0;
            document.getElementById("User_ID").value = data[0].UserDetail.User_ID;
            document.getElementById("User_Emp_Code").value = data[0].UserDetail.User_Emp_Code;
            document.getElementById("User_Name").value = data[0].UserDetail.User_Name;
            document.getElementById("User_Password").value = data[0].UserDetail.User_Password;
            document.getElementById("User_Designation").selectedIndex = data[0].UserDetail.User_Designation;
            document.getElementById("User_NICNo").value = data[0].UserDetail.User_NICNo;
            document.getElementById("User_Email").value = data[0].UserDetail.User_Email;
            document.getElementById("Confirm_Password").value = data[0].UserDetail.User_ID;
            document.getElementById("PTCL_No").value = data[0].UserDetail.User_ID;
            document.getElementById("Cell_No").value = data[0].UserDetail.Cell_No;
            document.getElementById("updateFormData").classList.remove("d-none");
            document.getElementById("insertFormData").classList.add("d-none");

            table.clear().draw();
            for (var i = 0; i < data.length; i++) {

                var formStatusCodeSelect = `<select class="form-control form-control-sm" id="formStatusCode${i}">
                                <option value="3" ${data[i].FormStatusID == 3 ? 'selected' : ''}>Add And Update</option>
                                <option value="1" ${data[i].FormStatusID == 1 ? 'selected' : ''}>Add</option>
                                <option value="2" ${data[i].FormStatusID == 2 ? 'selected' : ''}>Update</option>
                                <option value="0" ${data[i].FormStatusID == 0 ? 'selected' : ''}>View</option>
                                </select>`;

                var row = [
                    counter,
                    data[i].FormDescription.FormID,
                    data[i].FormDescription.FormDescr,
                    data[i].FormDescription.ModuleDescr,
                    data[i].FormDescription.MnuDescr,
                    data[i].FormDescription.MnuSubDescr,
                    data[i].FormDescription.FormType,
                    formStatusCodeSelect,
                    formStatusCheckBox,
                    companiesSelect
                ];
                table.row.add(row).draw(false);
                counter++;
            }
        } else {
            console.log('No data found');
        }
    });
});



function fillTableGrid() {
    // getAllCompanies().then((companiesData) => {
    // console.log("Companies response: ", companiesData);
    // let companiesSelect = '<select class="form-control form-control-sm" id="companies">';
    // for (let i = 0; i < companiesData.length; i++) {
    //     companiesSelect += `<option value="${companiesData[i].CoID}">${companiesData[i].CoName}</option>`;
    // }
    // companiesSelect += '</select>';

    let companiesSelect = '<select class="form-control form-control-sm" id="companies"><option value="1">iTecknologi Tracking</option></select>';

    getAllUserPrivileges(1).then((userPrivilegesData) => {
        console.log("User privileges response: ", userPrivilegesData);
        let formStatusCodeSelect = `<select class="form-control form-control-sm" id="formStatusCode">
                <option value="3">Add And Update</option>
                <option value="1">Add</option>
                <option value="2">Update</option>
                <option value="0">View</option>
                </select>`;

        console.log('userPrivilegesData: ', userPrivilegesData)
        var counter = 1;
        table.clear().draw();
        for (var i = 0; i < userPrivilegesData.length; i++) {
            // var row = [
            //     counter,
            //     userPrivilegesData[i].Form_ID,
            //     userPrivilegesData[i].Form_Descr,
            //     userPrivilegesData[i].Module,
            //     userPrivilegesData[i].Menu,
            //     userPrivilegesData[i].Sub_Menu,
            //     userPrivilegesData[i].Form_Type,
            //     formStatusCodeSelect,
            //     userPrivilegesData[i].Status,
            //     companiesSelect
            // ];
            var row = [1, 1, 'form 1', 1, 1, 1, 'test type', formStatusCodeSelect, 1, companiesSelect];
            table.row.add(row).draw(false);
            counter++;
        }
    }).catch((error) => {
        console.error("Error fetching user privileges: ", error);
    });
}

// function handleInsertClick() {
//     let tablerowarrayobject = [];
//     const User_ID = document.getElementById("User_ID").value = 0;
//     const User_Emp_Code = document.getElementById("User_Emp_Code").value = '';  
//     const User_Name = document.getElementById("User_Name").value = '';  
//     const User_Password = document.getElementById("User_Password").value = '';  
//     const User_Designation = document.getElementById("User_Designation").selectedIndex = 0; 
//     const User_NICNo = document.getElementById("User_NICNo").value = '';  
//     const User_Email = document.getElementById("User_Email").value = '';  
//     const Confirm_Password = document.getElementById("Confirm_Password").value = '';  
//     const PTCL_No = document.getElementById("PTCL_No").value = '';  
//     const Cell_No = document.getElementById("Cell_No").value = '';  

//     const formData = {
//         User_ID: User_ID,
//         User_Emp_Code: User_Emp_Code,
//         User_Name: User_Name,
//         User_Password: User_Password,
//         User_Designation: User_Designation,
//         User_NICNo: User_NICNo,
//         User_Email: User_Email,
//         Confirm_Password: Confirm_Password,
//         PTCL_No: PTCL_No,
//         Cell_No: Cell_No,
//     }

//     formprivileges = document.getElementsByName("FormCheckBox");
//     debugger
//     if ($("#InserRowID tr").length > 1) {
//         $("#InserRowID tr").each(function () {

//             var currentRow = $(this);

//             var col1_value = currentRow.find("td:eq(1)").text();
//             var col7_value = currentRow.find("td:eq(7) :selected").map(function (i, el) {
//                 return $(el).val();
//             }).get();;
//             var col8_value = currentRow.find("td:eq(8) checked").val();

//             //var ff = currentRow.find("td:eq(8)").html();
//             /*var colval7 = currentRow.find("td:eq(7)").html();
//             var colval8 = currentRow.find("td:eq(8)").html();*/

//             //debugger

//             console.log('col8_value: ', col8_value)

//             var obj = {};
//             obj.FormID = col7_value;
//             obj.Status = true;
//             if (col7_value == 1) {
//                 obj.FormStatus = 'A';
//             } if (col7_value == 2) {
//                 obj.FormStatus = 'U';
//             } if (col7_value == 3) {
//                 obj.FormStatus = 'AU';
//             }

//             if(col8_value){
//                 tablerowarrayobject.push(obj);
//             }

//         });
//     }

//     createUserPrivileges(formData);

// }

function handleInsertClick() {
    let tablerowarrayobject = [];

    table.rows().every(function () {
        let currentRow = this.node();

        let col1_value = $(currentRow).find("td:eq(1)").text();
        let col7_value = $(currentRow).find("td:eq(7) select").val();
        let col8_checked = $(currentRow).find("td:eq(8) input[type='checkbox']").is(":checked");

        if (col8_checked) {
            let obj = {};
            obj.FormID = col1_value;
            if (col7_value == 0) {
                obj.FormStatusID = 0;
                obj.FormStatus = 'V';
            } else if (col7_value == 1) {
                obj.FormStatusID = 1;
                obj.FormStatus = 'A';
            } else if (col7_value == 2) {
                obj.FormStatusID = 2;
                obj.FormStatus = 'U';
            } else if (col7_value == 3) {
                obj.FormStatusID = 3;
                obj.FormStatus = 'AU';
            }
            tablerowarrayobject.push(obj);
        }
    });

    console.log(tablerowarrayobject);

    const User_ID = document.getElementById("User_ID").value;
    const User_Emp_Code = document.getElementById("User_Emp_Code").value;
    const User_Name = document.getElementById("User_Name").value;
    const User_Password = document.getElementById("User_Password").value;
    const User_Designation = document.getElementById("User_Designation").selectedIndex;
    const User_NICNo = document.getElementById("User_NICNo").value;
    const User_Email = document.getElementById("User_Email").value;
    const Confirm_Password = document.getElementById("Confirm_Password").value;
    const PTCL_No = document.getElementById("PTCL_No").value;
    const Cell_No = document.getElementById("Cell_No").value;

    const formData = {
        User_ID: User_ID,
        User_Emp_Code: User_Emp_Code,
        User_Name: User_Name,
        User_Password: User_Password,
        User_Designation: User_Designation,
        User_NICNo: User_NICNo,
        User_Email: User_Email,
        Confirm_Password: Confirm_Password,
        PTCL_No: PTCL_No,
        Cell_No: Cell_No,
        tableFormIDs: tablerowarrayobject
    }

    console.log('formData: ', formData)

    createUserPrivileges(formData);
}

function handleUpdateClick() {
    const Grade_ID = document.getElementById("Grade_ID").value;
    const Grade_Descr = document.getElementById("Grade_Descr").value;

    const departmentData = {
        Grade_ID: Grade_ID,
        Grade_Descr: Grade_Descr
    }
    updateUserPrivileges(Grade_ID, departmentData);
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

function fillDesignationDropDown() {
    getAllDesignation().then((data) => {
        let temp = '';
        data.forEach(element => {
            temp += `<option value="${element.DSG_ID}">${element.DSG_Descr}</option>`;
        });
        document.getElementById("User_Designation").innerHTML = temp;
    });
}

$(document).ready(function () {
    initializeDataTable();
    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    fillDesignationDropDown()
    fillUserDropDown()
    //fillTableGrid()
});
