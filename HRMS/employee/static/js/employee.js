const BASE_URL = window.location.origin;
var table, city_array = [], region_array = [];
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
    if (confirm("Are you sure you want to delete this Employee?")) {
        deleteDesignation(Dept_ID).then(success => {
            if (success) {
                displaySuccessMessage('Employee deleted successfully!');
                fillTableGrid(); // Reload table after deletion
            } else {
                displayErrorMessage('Failed to delete Employee. Please try again.');
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
    document.getElementById("Email").value = '';
    document.getElementById("Address").value = '';
    document.getElementById("Confirmation_Date").value = '';
    document.getElementById("CNIC_Issue_Date").value = '';
    document.getElementById("CNIC_Exp_Date").value = '';
    // document.getElementById("previewImage").src = "{% get_media_prefix %}profile/avatar.png"

    document.getElementById("updateFormData").classList.add("d-none");
    document.getElementById("insertFormData").classList.remove("d-none");

}

async function getAllEmployee() {
    try {
        const response = await fetch(`${BASE_URL}/employee/getall`);
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
    const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value);
    const Father_Name = document.getElementById("Father_Name").value;
    const CNIC_No = document.getElementById("CNIC_No").value;
    const Religion = document.getElementById("Religion").value;
    const CT_ID = Number(document.getElementById("CT_ID").value);
    const Personal_Cell_No = document.getElementById("Personal_Cell_No").value;
    const Official_Cell_No = document.getElementById("Official_Cell_No").value;
    const Emergency_Cell_No = document.getElementById("Emergency_Cell_No").value;
    const Joining_Date = document.getElementById("Joining_Date").value;
    const Joining_Dsg_ID = Number(document.getElementById("Joining_Dsg_ID").value);
    const Co_ID = Number(document.getElementById("Co_ID").value);
    const Joining_Dept_ID = Number(document.getElementById("Joining_Dept_ID").value);
    const Emp_Status = document.getElementById("Emp_Status").value;
    const Email = document.getElementById("Email").value;
    const Address = document.getElementById("Address").value;
    const Confirmation_Date = document.getElementById("Confirmation_Date").value;
    const CNIC_Issue_Date = document.getElementById("CNIC_Issue_Date").value;
    const CNIC_Exp_Date = document.getElementById("CNIC_Exp_Date").value;

    // console.log('profileImage: ', document.getElementById('profileImage').files[0])

    let formData = new FormData();
    // formData.append('profileImage', document.getElementById('profileImage').files[0]);
    formData.append('Emp_ID', Emp_ID);
    formData.append('HR_Emp_ID', HR_Emp_ID);
    formData.append('Emp_Name', Emp_Name);
    formData.append('Father_Name', Father_Name);
    formData.append('DateOfBirth', DateOfBirth);
    formData.append('Gender', Gender);
    formData.append('Marital_Status', Marital_Status);
    formData.append('Personal_Cell_No', Personal_Cell_No);
    formData.append('CNIC_No', CNIC_No);
    formData.append('Religion', Religion);
    formData.append('CT_ID', CT_ID);
    formData.append('Emergency_Cell_No', Emergency_Cell_No);
    formData.append('Joining_Date', Joining_Date);
    formData.append('Joining_Dsg_ID', Joining_Dsg_ID);
    formData.append('Official_Cell_No', Official_Cell_No);
    formData.append('Co_ID', Co_ID);
    formData.append('Joining_Dept_ID', Joining_Dept_ID);
    formData.append('Emp_Status', true);
    formData.append('Email', Email);
    formData.append('Address', Address);
    formData.append('Confirmation_Date', Confirmation_Date);
    formData.append('CNIC_Issue_Date', CNIC_Issue_Date);
    formData.append('CNIC_Exp_Date', CNIC_Exp_Date);

    if(HR_Emp_ID != '' && Emp_Name != '' && Joining_Date != '' && CT_ID != '' && DateOfBirth != '' && Joining_Dept_ID != ''
        && Joining_Dsg_ID != '' && CNIC_No != '' && CNIC_Issue_Date != '' && CNIC_Exp_Date != '' && Gender != '' 
    && Marital_Status != '' && Co_ID != '')
    {
        createEmployee(formData);
    }else{
        alert('please fill required field!')
    }
}

async function createEmployee(formData) {
    try {
        const response = await fetch(`${BASE_URL}/employee/add`, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData,
        });
        
        if (!response.ok) {
            const errorData = await response.json();  // Parse the JSON response to get the error message
            throw new Error(errorData.message || 'Failed to create employee');  // Use the server's error message or a default one
        }

        displaySuccessMessage('Employee created successfully!');
        fillTableGrid();
    } catch (error) {
        console.error('Error creating Employee:', error);
        displayErrorMessage('Failed to create Employee. Please try again.');
    }
}

async function updateDesignation(id, formData) {
    try {
        const response = await fetch(`${BASE_URL}/employee/update/${id}`, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData,
        });
        if (!response.ok) {
            const errorData = await response.json();  // Parse the JSON response to get the error message
            throw new Error(errorData.message || 'Failed to create Employee');  // Use the server's error message or a default one
        }
        //const data = await response.json();
        displaySuccessMessage('Employee updated successfully!');
        fillTableGrid();
        // fillTableGrid();
        //return data;
    } catch (error) {
        console.error('Error updating Employee:', error);
        displayErrorMessage('Failed to update Employee. Please try again.');
        return null;
    }
}

async function deleteDesignation(id) {
    try {
        const response = await fetch(`${BASE_URL}/employee/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
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
        // console.log("response: ", data);
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
    // dropdownMenu.appendChild(deleteLink);

    dropdown.appendChild(button);
    dropdown.appendChild(dropdownMenu);

    return dropdown;
}

function handleUpdateClick() {
    // const Dept_ID = document.getElementById("Dept_ID").value;
    // const Dept_Descr = document.getElementById("Dept_Descr").value;

    // const departmentData = {
    //     Dept_ID: Dept_ID,
    //     Dept_Descr: Dept_Descr
    // }

    const Emp_ID = Number(document.getElementById("Emp_ID").value);
    const Emp_Name = document.getElementById("Emp_Name").value;
    const DateOfBirth = document.getElementById("DateOfBirth").value;
    const Gender = document.getElementById("Gender").value;
    const Marital_Status = document.getElementById("Marital_Status").value;
    const HR_Emp_ID = Number(document.getElementById("HR_Emp_ID").value);
    const Father_Name = document.getElementById("Father_Name").value;
    const CNIC_No = document.getElementById("CNIC_No").value;
    const Religion = document.getElementById("Religion").value;
    const CT_ID = Number(document.getElementById("CT_ID").value);
    const REG_ID = Number(document.getElementById("REG_ID").value);
    const Personal_Cell_No = document.getElementById("Personal_Cell_No").value;
    const Official_Cell_No = document.getElementById("Official_Cell_No").value;
    const Emergency_Cell_No = document.getElementById("Emergency_Cell_No").value;
    const Joining_Date = document.getElementById("Joining_Date").value;
    const Joining_Dsg_ID = Number(document.getElementById("Joining_Dsg_ID").value);
    const Co_ID = Number(document.getElementById("Co_ID").value);
    const Joining_Dept_ID = Number(document.getElementById("Joining_Dept_ID").value);
    const Emp_Status = document.getElementById("Emp_Status").value;
    const Email = document.getElementById("Email").value;
    const Address = document.getElementById("Address").value;
    const Confirmation_Date = document.getElementById("Confirmation_Date").value;
    const CNIC_Issue_Date = document.getElementById("CNIC_Issue_Date").value;
    const CNIC_Exp_Date = document.getElementById("CNIC_Exp_Date").value;

    // console.log('profileImage: ', document.getElementById('profileImage').files[0])

    let formData = new FormData();
    // formData.append('profileImage', document.getElementById('profileImage').files[0]);
    formData.append('Emp_ID', Emp_ID);
    formData.append('HR_Emp_ID', HR_Emp_ID);
    formData.append('Emp_Name', Emp_Name);
    formData.append('Father_Name', Father_Name);
    formData.append('DateOfBirth', DateOfBirth);
    formData.append('Gender', Gender);
    formData.append('Marital_Status', Marital_Status);
    formData.append('Personal_Cell_No', Personal_Cell_No);
    formData.append('CNIC_No', CNIC_No);
    formData.append('Religion', Religion);
    formData.append('CT_ID', CT_ID);
    formData.append('REG_ID', REG_ID);
    formData.append('Emergency_Cell_No', Emergency_Cell_No);
    formData.append('Joining_Date', Joining_Date);
    formData.append('Joining_Dsg_ID', Joining_Dsg_ID);
    formData.append('Official_Cell_No', Official_Cell_No);
    formData.append('Co_ID', Co_ID);
    formData.append('Joining_Dept_ID', Joining_Dept_ID);
    formData.append('Emp_Status', true);
    formData.append('Email', Email);
    formData.append('Address', Address);
    formData.append('Confirmation_Date', Confirmation_Date);
    formData.append('CNIC_Issue_Date', CNIC_Issue_Date);
    formData.append('CNIC_Exp_Date', CNIC_Exp_Date);

    if(HR_Emp_ID != '' && Emp_Name != '' && Joining_Date != '' && CT_ID != '' && DateOfBirth != '' && Joining_Dept_ID != ''
        && Joining_Dsg_ID != '' && CNIC_No != '' && CNIC_Issue_Date != '' && CNIC_Exp_Date != '' && Gender != '' 
    && Marital_Status != '' && Co_ID != '')
    {
    updateDesignation(Emp_ID, formData);
    }else{
        alert('please fill required field!')
    }
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
    getAllDataFromDB(`employee/getbyid/${id}`).then((data => {
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
        document.getElementById("CNIC_Issue_Date").value = data.CNIC_Issue_Date 
        document.getElementById("CNIC_Exp_Date").value = data.CNIC_Exp_Date 
        document.getElementById("Religion").value = data.Religion
        document.getElementById("CT_ID").value = data.CT_ID
        document.getElementById("Grade_ID").value = data.Grade_ID
        document.getElementById("Address").value = data.Address
        
        // console.log('region_array region: ', region_array)
        const region = region_array.find(x => x.REG_ID == data.REG_ID);
        // console.log('region: ', region)
        if(region != undefined){
            document.getElementById("REG_ID").innerHTML = `<option value="${region.REG_ID}">${region.REG_Descr}</option>` 
        }
        document.getElementById("Emergency_Cell_No").value = data.Emergency_Cell_No
        document.getElementById("Joining_Date").value = moment(data.Joining_Date).format("YYYY-MM-DD");
        document.getElementById("Joining_Dsg_ID").value = data.Joining_Dsg_ID
        document.getElementById("Official_Cell_No").value = data.Official_Cell_No
        document.getElementById("Co_ID").value = data.Co_ID
        document.getElementById("Joining_Dept_ID").value = data.Joining_Dept_ID
        document.getElementById("Emp_Status").value = data.Emp_Status
        // console.log('data.profileimage: ', data.profileimage)
        // document.getElementById("profileImage").value = data.profileimage
        // document.getElementById("profileImage").src = "/media/media/profile/salman.jpg";

    }));
}

function fillDropDown(dataName, dropdownId, valueField, displayTextField) {
    getAllDataFromDB(dataName).then((data) => {
        var temp = '';
        // console.log('dataName: ', dataName)
        // console.log('dataName data: ', data)
        if (dataName == 'city/getall') {
            city_array = data
        }  if (dataName == 'region/getall') {
                region_array = data
                // console.log('region_array: ', region_array)
            } else{
                data.forEach(element => {
                    temp += `<option value="${element[valueField]}">${element[displayTextField]}</option>`;
                });   
            }
             
        document.getElementById(dropdownId).innerHTML = temp;
    });
}

document.getElementById('CT_ID').addEventListener('change', function (e) {
    console.log('city_array: ', city_array)
    seleted_region = city_array.find(x => x.CT_ID == this.value)
    console.log('seleted_region: ', seleted_region)
    document.getElementById("REG_ID").innerHTML = `<option value="${seleted_region.REG_ID}">${seleted_region.REG_Descr}</option>`
});

// document.getElementById('profileImage').addEventListener('change', function (e) {
//     var reader = new FileReader();
//     reader.onload = function (e) {
//         document.getElementById('previewImage').setAttribute('src', e.target.result);
//     };
//     reader.readAsDataURL(this.files[0]);
// });

// window.onload = function(){
//     document.getElementById('previewImage').setAttribute('src', "{% static 'profile/avatar.png' %}");
// }

$(document).ready(function () {
    initializeDataTable();

    document.getElementById('DateOfBirth').valueAsDate = new Date();
    document.getElementById('CNIC_Issue_Date').valueAsDate = new Date();
    document.getElementById('CNIC_Exp_Date').valueAsDate = new Date();
    document.getElementById('Joining_Date').valueAsDate = new Date();
    document.getElementById('Confirmation_Date').valueAsDate = new Date();
    document.getElementById('Joining_Date').valueAsDate = new Date();


    // $('#GridID tbody').on('click', 'tr', handleTableRowClick);
    $('#GridID tbody').on('click', '.roweditclass', handleTableRowClick);
    $('#GridID tbody').on('click', '.rowdeleteclass', handleDeleteButtonClick); // Attach delete button click handler
    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);
    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);
    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);
    fillDropDown('department/getall', 'Joining_Dept_ID', 'Dept_ID', 'Dept_Descr');
    fillDropDown('designation/getall', 'Joining_Dsg_ID', 'DSG_ID', 'DSG_Descr');
    fillDropDown('city/getall', 'CT_ID', 'CT_ID', 'CT_Descr');
    fillDropDown('grade/getall', 'Grade_ID', 'Grade_ID', 'Grade_Descr');
    fillDropDown('region/getall', 'REG_ID', 'REG_ID', 'REG_Descr');
    fillDropDown('employee/group-of-companies', 'Co_ID', 'CoID', 'CoName');
    fillTableGrid()
});
