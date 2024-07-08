// import { BASE_URL, authorization, companyID, FormStatusID, MenuId, FormId } from './Common.js';

let table, table2, listofDepartments = [], listofElements = [];
const BASE_URL = window.location.origin;
const INSERT_BUTTON_ID = 'insertBtnId';
const UPDATE_BUTTON_ID = 'updateBtnId';
const CANCEL_BUTTON_ID = 'cancelBtnId';

function initializeDataTable() {
    // table = $('#GridID1').DataTable({
    //     destroy: true,
    //     duplicate: false,
    //     ordering: false,
    //     pageLength: 5,
    //     'columnDefs': [
    //         {
    //             "targets": 1,
    //             "className": "text-left custom-input",
    //         },
    //         {
    //             "targets": 2,
    //             "className": "text-left custom-input",
    //         }
    //     ],
    //     lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    // });
    table2 = $('#GridID2').DataTable({
        destroy: true,
        duplicate: false,
        ordering: false,
        pageLength: 5,
        'columnDefs': [
            {
                "targets": 1,
                "className": "text-left custom-input",
            },
            {
                "targets": 2,
                "className": "text-left custom-input",
            }
        ],
        lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    });
}

function handleTableRowClick() {

    const deptId = $(this).find('td')[1].innerHTML;

    document.getElementById("Working_Dept_ID").readOnly = true;
    document.getElementById("singleSelection").value = deptId;

    $("#orangeModalSubscription").modal('hide');

    getWDAByID(deptId);

    // if (FormStatusID == 2 || FormStatusID == 3) {
    //     document.getElementById(UPDATE_BUTTON_ID).style.removeProperty('display');
    // } if (FormStatusID == 1 || FormStatusID == 3) {
    //     document.getElementById(INSERT_BUTTON_ID).style.display = 'none';
    // }
}

function handleCancelClick() {

    document.getElementById("Working_Dept_ID").selectedIndex = 0;
    document.getElementById("singleSelection").selectedIndex = 0;
    document.getElementById("InserRowID").innerHTML = '';
    table2.clear().draw();
    document.getElementById('singleSelection').disabled = false; 
    // document.getElementById('singleSelection').style.backgroundColor = '##343a40'; 
    document.getElementById('singleSelection').style.backgroundColor = '#fff'; 
    document.getElementById('singleSelection').style.color = '#343a40'; 

    // if (FormStatusID == 2 || FormStatusID == 3) {
    //     document.getElementById(UPDATE_BUTTON_ID).style.display = 'none';
    // }
    // if (FormStatusID == 1 || FormStatusID == 3) {
    //     document.getElementById(INSERT_BUTTON_ID).style.removeProperty('display');
    // }

    // document.getElementById("alertId").innerHTML = '';
}

function getCategoryItemDataFromAPI() {
    // if (FormStatusID == 0) {
    //     document.getElementById(INSERT_BUTTON_ID).style.display = 'none';
    //     document.getElementById(UPDATE_BUTTON_ID).style.display = 'none';
    // } if (FormStatusID == 1) {
    //     document.getElementById(UPDATE_BUTTON_ID).style.display = 'none';
    // } if (FormStatusID == 2) {
    //     document.getElementById(INSERT_BUTTON_ID).style.display = 'none';
    // }
    //debugger
    if (authorization != null) {
        $.ajax({
            type: 'GET',
            url: BASE_URL + '/wda/GetAll',
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                'X-CSRFToken': getCookie('csrftoken')
                // "authorization": authorization,
                // "companyID": companyID,
                // "MenuId": MenuId,
                // "FormId": FormId
            },
            success: function (response) {
                console.log("response: ", response);
                listofOrganization = response;
                var counter = 1;
                var gridData = '';
                /*table.clear().draw();
                for (var i = 0; i < response.length; i++) {
                    table.row.add([counter, response[i].grade_ID, response[i].grade_Descr]).draw(false);
                    counter++;
                }*/
            },
            error: function (error) {
                document.getElementById("errormsgid").innerHTML = error;
                $("#myModal").modal('show');
                console.log("Error: ", error);
            }
        });
    } else {
        window.location.href = "/Login/Index2/";
    }
}

function handleInsertClick() {
    const W_Dept_ID_ = document.getElementById("singleSelection").value;
    insertWorkingData(0, W_Dept_ID_, 0);
    getWDAByID(W_Dept_ID_);
    GetAllWDAByID(W_Dept_ID_);
}

function insertWorkingData(W_ID, W_Dept_ID, Mode) {
    let workingDeptData = [];

    $('#dataTable tbody tr').each(function (index, row) {
        let obj0 = {};
        obj0.W_ID = W_ID;
        obj0.W_Dept_ID = W_Dept_ID;
        obj0.Mode = Mode;
        var departmentValues = $(row).find('.multi-department').val();
        obj0.Departments = departmentValues;
        var elementValues = $(row).find('.multi-element').val();
        obj0.Elements = elementValues;

        workingDeptData.push(obj0);
    });

    console.log('workingDeptData: ', workingDeptData);

    //debugger
    if (workingDeptData.length != 0) {

        $.ajax({
            type: 'POST',
            url: BASE_URL + '/wda/add',
            contentType: 'application/json',
            data: JSON.stringify(workingDeptData),
            // data: {
            //     WDAData: workingDeptData
            // },
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
                // "authorization": authorization,
                // "companyID": companyID,
                // "MenuId": MenuId,
                // "FormId": FormId
            },
            success: function (response) {
                //debugger
                displaySuccessMessage("Working Departmenet Successfully Assigned");
            },
            error: function (error) {
                displayErrorMessage("Getting Error while Assigning Working Department");
                console.log(error);
            }
        });
    } else {
        displayErrorMessage("Kindly select working department");
    }
}

function handleUpdateClick() {
    // let Working_Dept_ID = document.getElementById("Working_Dept_ID").value;
    // let W_Dept_ID = document.getElementById("singleSelection").value;
    // insertWorkingData(Working_Dept_ID, W_Dept_ID, 1);
    // getWDAByID(W_Dept_ID);
    // GetAllWDAByID(W_Dept_ID);

    let Working_Dept_ID = document.getElementById("Working_Dept_ID").value;
    const W_Dept_ID_ = document.getElementById("singleSelection").value;
    insertWorkingData(Working_Dept_ID, W_Dept_ID_, 1);
    getWDAByID(W_Dept_ID_);
    GetAllWDAByID(W_Dept_ID_);
}

function getWDAByID(W_ID) {
    $.ajax({
        type: 'GET',
        url: `${BASE_URL}/wda/getall/${W_ID}`,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': getCookie('csrftoken')
            // "authorization": authorization,
            // "companyID": companyID,
            // "MenuId": MenuId,
            // "FormId": FormId
        },
        success: function (response) {
            console.log('response: ', response);

            if (response.length > 0 || response != '') {

                let deptList = response.map(item => item.Dept_ID);
                let elementList = response.map(item => item.W_All_Ded_Element_ID);

                let uniqueValuesSet = new Set(elementList);
                let uniqueArray = Array.from(uniqueValuesSet);

                // document.getElementById("Working_Dept_ID").value = response[0].W_All_Ded_ID;
                //document.getElementById("singleSelection").selectedIndex = response[0].w_All_Ded_Dept_ID;

                console.log('elementList: ', elementList)
                console.log('uniqueValuesSet: ', uniqueValuesSet)
                console.log('uniqueArray: ', uniqueArray)
                
                document.getElementById("InserRowID").innerHTML = "";

                for (var i = 0; i < uniqueArray.length; i++) {
                    addNewRow(); // Add a new row for each unique value

                    let data2 = response.filter(item => item.W_All_Ded_Element_ID == uniqueArray[i]).map(item => item.Dept_ID);
                    console.log('data2: ', data2);

                    // Assuming you have a way to identify the new row in the table, for example, using a class
                    let newRow = $(`#dataTable tbody tr:last`);

                    // Populate multi-selection checkboxes in the new row
                    newRow.find('.multi-department').multiselect('select', data2);
                    newRow.find('.multi-element').multiselect('select', uniqueArray[i]);
                }
            } else {
                displayErrorMessage("No Record Found");
            }

            // Assuming response is an array of objects with properties w_All_Ded_ID and w_All_Ded_Element_ID
            /*$('#dataTable tbody tr').each(function (index, row) {
                if (index < response.length) {
                    // Set values in the multi-select dropdowns for each row
                    $(row).find('.multi-department').multiselect('select', response[index].w_All_Ded_ID);
                    $(row).find('.multi-element').multiselect('select', response[index].w_All_Ded_Element_ID);
                }
            });*/

        },
        error: function (error) {
            console.log('error while fetching designation: ', error)
        }
    })
}

function getAllDepartment() {
    $.ajax({
        type: 'GET',
        url: `/department/getall`,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            // "authorization": authorization,
            // "companyID": companyID,
            // "MenuId": MenuId,
            // "FormId": FormId
        },
        success: function (response) {
            listofDepartments = response;
            console.log('response: ', response);
            let temp = '', temp2 = '';
            for (var i = 0; i < response.length; i++) {
                temp2 += `<option value="${response[i].Dept_ID}">${response[i].Dept_Descr}</option>`;
            }
            document.getElementById("singleSelection").innerHTML = temp2;
            document.getElementById("Working_Dept_ID").innerHTML = temp2;
            // document.getElementById("searchDeptID").innerHTML = temp2;
        },
        error: function (error) {
            console.log('error while fetching designation: ', error)
        }
    })
}

document.getElementById("addBtnId").addEventListener('click', function () {
    addNewRow();
});

function addNewRow() {
    var newRow = $('<tr><td><select class="form-control multi-select multi-department" multiple></select></td><td><select class="form-control multi-select multi-element" multiple></select></td></tr>');

    $('#dataTable tbody').append(newRow);

    populateDropdownDepartmentOptions(newRow.find('.multi-department'));
    populateDropdownElementOptions(newRow.find('.multi-element'));

    newRow.find('.multi-select').multiselect({
        enableFiltering: true,
        includeSelectAllOption: true,
        maxHeight: 300,
        buttonWidth: '100%', // Set the width of the button to 100%
        enableCaseInsensitiveFiltering: true,
        filterPlaceholder: 'Search...',
        nonSelectedText: 'Select Options',
        nSelectedText: ' selected',
        allSelectedText: 'All selected',
        selectAllText: 'Select All'
    });

    // Apply CSS styles
    newRow.find('.form-control').css('color', 'red'); // Change font color to red
    newRow.find('.form-control').css('background-color', 'lightblue'); // Change background color to light blue
}

function populateDropdownDepartmentOptions(dropdown) {
    var optionList = '';

    for (var i = 0; i < listofDepartments.length; i++) {
        optionList += `<option value="${listofDepartments[i].Dept_ID}">${listofDepartments[i].Dept_Descr}</option>`;
    }
    dropdown.html(optionList);
}

function populateDropdownElementOptions(dropdown) {
    var optionList = '';
    for (var i = 0; i < listofElements.length; i++) {
        optionList += `<option value="${listofElements[i].Element_ID}">${listofElements[i].Element_Name}</option>`;
    }
    dropdown.html(optionList);
}

function getAllElement() {
    $.ajax({
        type: 'GET',
        url: `/payroll_element/getall`,
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            // "authorization": authorization,
            // "companyID": companyID,
            // "MenuId": MenuId,
            // "FormId": FormId
        },
        success: function (response) {
            console.log('response: ', response);
            listofElements = response.filter(item => item.Element_Category != 'Fixed');
        },
        error: function (error) {
            console.log('error while fetching designation: ', error)
        }
    })
}

// document.getElementById("searchDeptID").addEventListener("change", function () {
//     GetAllWDAByID(this.value);
// });

function GetAllWDAByID(W_Dept_ID) {
    //debugger
    if (1 == 1) {
        $.ajax({
            type: 'GET',
            url: `${BASE_URL}/wda/getall/${W_Dept_ID}`,
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                'X-CSRFToken': getCookie('csrftoken')
                // "authorization": authorization,
                // "companyID": companyID,
                // "MenuId": MenuId,
                // "FormId": FormId
            },
            success: function (response) {
                console.log("response: ", response);
                //listofOrganization = response;
                var counter = 1;
                var gridData = '';
                table2.clear().draw();
                for (var i = 0; i < response.length; i++) {
                    table2.row.add([counter, response[i].W_All_Ded_Dept_Name, response[i].Dept_Name, response[i].Element_Name, response[i].Element_Type, response[i].Element_Category]).draw(false);
                    counter++;
                }
            },
            error: function (error) {
                // document.getElementById("errormsgid").innerHTML = error;
                $("#myModal").modal('show');
                console.log("Error: ", error);
            }
        });
    } else {
        window.location.href = "/Login/Index2/";
    }
}

document.getElementById("Working_Dept_ID").addEventListener("click", function () {
    // alert('this: ', this.value)
    console.log('this.value: ', this.value);
    document.getElementById("singleSelection").value = this.value;
    document.getElementById('singleSelection').disabled = true;     
    document.getElementById("singleSelection").style.backgroundColor = "#343a40";
    document.getElementById('singleSelection').style.color = '#fff'; 

    document.getElementById("insertBtnId").classList.add("d-none")
    document.getElementById("updateBtnId").classList.remove("d-none")
    
    getWDAByID(this.value);
    GetAllWDAByID(this.value);
});

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

    // $('#GridID1 tbody').on('click', 'tr', handleTableRowClick);

    document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);

    document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);

    document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);

    // $(document).on('click', function () {
    //     if (event.srcElement.className != 'submit-btn')
    //         document.getElementById("alertId").innerHTML = "";
    // });

});

window.onload = function () {
    $(document).ready(function () {
        // alert()
        getAllDepartment();
        getAllElement();
        //GetAllWDAByID(2);-
    });
};

