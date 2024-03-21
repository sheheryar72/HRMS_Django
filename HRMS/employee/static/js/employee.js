const BASE_URL = '/employee/api/';
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
    const col1 = rowData[1];
    document.getElementById("updateFormData").classList.remove("d-none");
    document.getElementById("insertFormData").classList.add("d-none");
    fillFormDataFromDB(col1);
}

// Handle click on delete button in table row
function handleDeleteButtonClick() {
    //alert()
    const rowData = table.row($(this).closest('tr')).data();
    const Dept_ID = rowData[1];
    // console.log('Dept_ID: ', Dept_ID)
    if (confirm("Are you sure you want to delete this department?")) {
        deleteDesignation(Dept_ID).then(success => {
            if (success) {
                displaySuccessMessage('Designation deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete department. Please try again.');
            }
        });
    }
}

function handleCancelClick() {
    document.getElementById("Emp_ID").value = ''
    document.getElementById("Emp_Name").value = ''
    document.getElementById("DateOfBirth").value = ''
    document.getElementById("Gender").selectedIndex = 0
    document.getElementById("Marital_Status").selectedIndex = 0
    document.getElementById("Personal_Cell_No").value = ''
    document.getElementById("HR_Emp_ID").value = ''
    document.getElementById("Father_Name").value = ''
    document.getElementById("CNIC_No").value = ''
    document.getElementById("Religion").value = ''
    document.getElementById("CT_ID").selectedIndex = 0
    document.getElementById("Emergency_Cell_No").value = ''
    document.getElementById("Joining_Date").value = '';
    document.getElementById("Joining_Dsg_ID").selectedIndex = 0
    document.getElementById("Official_Cell_No").value = ''
    document.getElementById("Co_ID").selectedIndex = 0
    document.getElementById("Joining_Dept_ID").selectedIndex = 0
    document.getElementById("Emp_Status").selectedIndex = 0

    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");

}

async function getAllEmployee() {
    try {
        const response = await fetch(`${BASE_URL}getall`);
        if (!response.ok) {
            throw new Error('Failed to fetch departments');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching departments:', error);
        return null;
    }
}

// function handleInsertClick() {
//     const Emp_ID = Number(document.getElementById("Emp_ID").value)
//     const Emp_Name = document.getElementById("Emp_Name").value
//     const DateOfBirth = document.getElementById("DateOfBirth").value
//     const Gender = document.getElementById("Gender").value
//     const Marital_Status = document.getElementById("Marital_Status").value
//     const Personal_Cell_No = document.getElementById("Personal_Cell_No").value
//     const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value)
//     const Father_Name = document.getElementById("Father_Name").value
//     const CNIC_No = document.getElementById("CNIC_No").value
//     const religion = document.getElementById("Religion").value
//     const CT_ID = Number(document.getElementById("CT_ID").value)
//     const Emergency_Cell_No = document.getElementById("Emergency_Cell_No").value
//     const Joining_Date = document.getElementById("Joining_Date").value
//     const Joining_Dsg_ID = Number(document.getElementById("Joining_Dsg_ID").value)
//     const Official_Cell_No = document.getElementById("Official_Cell_No").value
//     const Co_ID = Number(document.getElementById("Co_ID").value)
//     const Joining_Dept_ID = Number(document.getElementById("Joining_Dept_ID").value)
//     const Emp_Status = document.getElementById("Emp_Status").value;

//     let formData = new FormData();
//     formData.append('profileImage', document.getElementById('profileImage').files[0]);

//     console.log('profileImage: ', document.getElementById('profileImage').files[0])

//     const emp_data = {
//         Emp_ID: Emp_ID,
//         Emp_Name: Emp_Name,
//         DateOfBirth: DateOfBirth,
//         Gender: Gender,
//         Marital_Status: Marital_Status,
//         Emp_Status: Emp_Status,
//         Joining_Dept_ID: Joining_Dept_ID,
//         Co_ID: Co_ID,
//         Official_Cell_No: Official_Cell_No,
//         Joining_Dsg_ID: Joining_Dsg_ID,
//         Joining_Date: Joining_Date,
//         CT_ID: CT_ID,
//         Emergency_Cell_No: Emergency_Cell_No,
//         religion: religion,
//         CNIC_No: CNIC_No,
//         Father_Name: Father_Name,
//         HR_Emp_ID: HR_Emp_ID,
//         Personal_Cell_No: Personal_Cell_No,
//         emp_profileimage: '',
//         emp_documents_file: ''
//     }
//     console.log('emp_data: ', emp_data)

//     for (let key in emp_data) {
//         formData.append(key, emp_data[key]);
//     }
    
//     console.log('formData: ', formData)

//     createEmployee(formData);

// }
// async function createEmployee(formData) {
//     try {
//         const response = await fetch(`${BASE_URL}add`, {
//             method: 'POST',
//             // headers: {
//             //     'Content-Type': 'application/json',
//             // },
//             body: formData,
//             // body: JSON.stringify(emp_data),
//         });
//         if (!response.ok) {
//             throw new Error('Failed to create department');
//         }
//         //const data = await response.json();
//         displaySuccessMessage('Designation created successfully!');
//         fillTableGrid();
//         //return data;
//     } catch (error) {
//         console.error('Error creating department:', error);
//         displayErrorMessage('Failed to create department. Please try again.');
//         return null;
//     }
// }

function handleInsertClick() {
    const Emp_ID = Number(document.getElementById("Emp_ID").value);
    const Emp_Name = document.getElementById("Emp_Name").value;
    const DateOfBirth = document.getElementById("DateOfBirth").value;
    const Gender = document.getElementById("Gender").value;
    const Marital_Status = document.getElementById("Marital_Status").value;
    const Personal_Cell_No = document.getElementById("Personal_Cell_No").value;
    const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value);
    const Father_Name = document.getElementById("Father_Name").value;
    const CNIC_No = document.getElementById("CNIC_No").value;
    const religion = document.getElementById("Religion").value;
    const CT_ID = Number(document.getElementById("CT_ID").value);
    const Emergency_Cell_No = document.getElementById("Emergency_Cell_No").value;
    const Joining_Date = document.getElementById("Joining_Date").value;
    const Joining_Dsg_ID = Number(document.getElementById("Joining_Dsg_ID").value);
    const Official_Cell_No = document.getElementById("Official_Cell_No").value;
    const Co_ID = Number(document.getElementById("Co_ID").value);
    const Joining_Dept_ID = Number(document.getElementById("Joining_Dept_ID").value);
    const Emp_Status = document.getElementById("Emp_Status").value;

    console.log('profileImage: ', document.getElementById('profileImage').files[0])

    let formData = new FormData();
    formData.append('profileImage', document.getElementById('profileImage').files[0]);
    formData.append('Emp_ID', Emp_ID);
    formData.append('Emp_Name', Emp_Name);
    formData.append('DateOfBirth', DateOfBirth);
    formData.append('Gender', Gender);
    formData.append('Marital_Status', Marital_Status);
    formData.append('Personal_Cell_No', Personal_Cell_No);
    formData.append('HR_Emp_ID', HR_Emp_ID);
    formData.append('Father_Name', Father_Name);
    formData.append('CNIC_No', CNIC_No);
    formData.append('religion', religion);
    formData.append('CT_ID', CT_ID);
    formData.append('Emergency_Cell_No', Emergency_Cell_No);
    formData.append('Joining_Date', Joining_Date);
    formData.append('Joining_Dsg_ID', Joining_Dsg_ID);
    formData.append('Official_Cell_No', Official_Cell_No);
    formData.append('Co_ID', Co_ID);
    formData.append('Joining_Dept_ID', Joining_Dept_ID);
    formData.append('Emp_Status', Emp_Status);

    createEmployee(formData);
}

async function createEmployee(formData) {
    try {
        const response = await fetch(`${BASE_URL}add`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Failed to create employee');
        }
        displaySuccessMessage('Employee created successfully!');
        fillTableGrid();
    } catch (error) {
        console.error('Error creating employee:', error);
        displayErrorMessage('Failed to create employee. Please try again.');
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
            throw new Error('Failed to update department');
        }
        //const data = await response.json();
        displaySuccessMessage('Designation updated successfully!');
        fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating department:', error);
        displayErrorMessage('Failed to update department. Please try again.');
        return null;
    }
}

async function deleteDesignation(id) {
    try {
        const response = await fetch(`${BASE_URL}delete/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete department');
        }
        return true;
    } catch (error) {
        console.error(`Error deleting department with ID ${id}:`, error);
        return false;
    }
}

function fillTableGrid() {
    getAllEmployee().then((data) => {
        console.log("response: ", data);
        var counter = 1;
        table.clear().draw();

        for (var i = 0; i < data.length; i++) {
            var actionButton = createActionButton(); // Create action button element
            var row = [counter, data[i].Emp_ID, data[i].HR_Emp_ID, data[i].Emp_Name, data[i].DateOfBirth, data[i].Joining_Date, actionButton.outerHTML];
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
    dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleUpdateClick() {
    const Dept_ID = document.getElementById("Dept_ID").value;
    const Dept_Descr = document.getElementById("Dept_Descr").value;

    const departmentData = {
        Dept_ID: Dept_ID,
        Dept_Descr: Dept_Descr
    }
    updateDesignation(Dept_ID, departmentData);
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

async function getAllDataFromDB(url) {
    try {
        const response = await fetch(`/${url}`);
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

function fillFormDataFromDB(id) {
    getAllDataFromDB(`employee/api/getbyid/${id}`).then((data => {
        console.log('emp data: ', data)
        document.getElementById("Emp_ID").value = data.Emp_ID
        document.getElementById("Emp_Name").value = data.Emp_Name
        document.getElementById("DateOfBirth").value = moment(data.DateOfBirth).format("YYYY-MM-DD");
        document.getElementById("Gender").value = data.Gender
        document.getElementById("Marital_Status").value = data.Marital_Status
        document.getElementById("Personal_Cell_No").value = data.Personal_Cell_No
        document.getElementById("HR_Emp_ID").value = data.HR_Emp_ID
        document.getElementById("Father_Name").value = data.Father_Name
        document.getElementById("CNIC_No").value = data.CNIC_No
        document.getElementById("Religion").value = data.Religion
        document.getElementById("CT_ID").value = data.CT_ID
        document.getElementById("Emergency_Cell_No").value = data.Emergency_Cell_No
        document.getElementById("Joining_Date").value = moment(data.Joining_Date).format("YYYY-MM-DD");
        document.getElementById("Joining_Dsg_ID").value = data.Joining_Dsg_ID
        document.getElementById("Official_Cell_No").value = data.Official_Cell_No
        document.getElementById("Co_ID").value = data.Co_ID
        document.getElementById("Joining_Dept_ID").value = data.Joining_Dept_ID
        document.getElementById("Emp_Status").value = data.Emp_Status
        console.log('data.profileimage: ', data.profileimage)
        // document.getElementById("profileImage").value = data.profileimage
        document.getElementById("profileImage").src = "/media/media/profile/salman.jpg";

    }));
}

function fillDropDown(dataName, dropdownId, valueField, displayTextField) {
    getAllDataFromDB(dataName).then((data) => {
        var temp = '';
        // console.log('data: ', data)
        data.forEach(element => {
            temp += `<option value="${element[valueField]}">${element[displayTextField]}</option>`;
        });
        document.getElementById(dropdownId).innerHTML = temp;
    });
}

document.getElementById('profileImage').addEventListener('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('previewImage').setAttribute('src', e.target.result);
    };  
    reader.readAsDataURL(this.files[0]);
});

$(document).ready(function () {
    initializeDataTable();
    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    fillDropDown('department/api/getall', 'Joining_Dept_ID', 'Dept_ID', 'Dept_Descr');
    fillDropDown('designation/api/getall', 'Joining_Dsg_ID', 'DSG_ID', 'DSG_Descr');
    fillDropDown('city/api/getall', 'CT_ID', 'CT_ID', 'CT_Descr');
    fillTableGrid()
});
