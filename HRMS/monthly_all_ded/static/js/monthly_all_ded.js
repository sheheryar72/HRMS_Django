const BASE_URL = window.location.origin;
var table, current_w_dept_id = 0, current_period_id = 0;
const INSERT_BUTTON_ID = 'insertFormData';
const UPDATE_BUTTON_ID = 'updateFormData';
const CANCEL_BUTTON_ID = 'CancelFormData';

function initializeDataTable() {
    // table = $('#GridID').DataTable({
    //     destroy: true,
    //     duplicate: false,
    //     ordering: false,
    //     scrollY: '330px',
    //     scrollCollapse: true,
    //     pageLength: 5,
    //     lengthMenu: [[5, 10, 20, -1], [5, 10, 20, 'All']]
    // });
}

// document.getElementById("W_Department").addEventListener("change", async function () {
//     // const W_deptID = localStorage.getItem("W_deptID");
//     const W_deptID = 2;
//     const W_Department = document.getElementById("W_Department").value;
//     try {
//         const response = await fetch(`${BASE_URL}getall_dept_element/${W_deptID}/${W_Department}`);
//         if (!response.ok) {
//             throw new Error('Failed to fetch Grade');
//         }
//         const data = await response.json();
//         let temp = '', temp2 = '', counter = 1;

//         console.log("W_Department data: ", data);

//         data[1]["Element"].forEach(element => {
//             temp += `<th style="width: 10%;">${element.Element_Name}</th>`
//         });
//         document.getElementById("InserRowHeadID").innerHTML = temp;

//         data[0]["Employee"].forEach(emp => {
//             let element_column = '';
//             for (let i = 0; i < data[1]["Element"].length; i++) {
//                 element_column += '`<input type="number" class="form-control">`';
//             }
//             table.row.add(counter, emp.Emp_Name, element_column).draw(false);
//             counter++;
//         });

//     } catch (error) {
//         console.error('Error fetching Grade:', error);
//         return null;
//     }
// });

function CancelFormAndGridData() {
    // document.getElementById("Department").value = '';
    // document.getElementById("Period").selectedIndex = 0;
    // document.getElementById("W_Department").selectedIndex = 0;

    document.getElementById("InserRowID").innerHTML = '';
}

document.getElementById("W_Department").addEventListener("click", async function () {
    // const W_deptID = localStorage.getItem("W_deptID");
    const W_deptID = 2;
    const W_Department = document.getElementById("W_Department").value;
    try {
        const response = await fetch(`${BASE_URL}/monthly_all_ded/getall_dept_element/${W_deptID}/${W_Department}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        let temp = '', temp2 = '', counter = 1;

        console.log("W_Department data: ", data);

        document.getElementById("InserRowHeadID").innerHTML = `<th style="width: 12%;">Employee ID</th><th style="width: 20%;">Employee</th>`;

        data[1]["Element"].forEach(element => {
            // element_col_ID = `${element.Element_Name}_${element.Element_ID}`
            let element_col_ID = `${element.Element_Name}_${element.Element_ID}`;
            element_col_ID = element_col_ID.replace(/ /g, '_');
            temp += `<th style="width: 20%;" id="${element_col_ID}">${element.Element_Name}</th>`;
        });

        document.getElementById("InserRowHeadID").innerHTML += temp;

        // document.getElementById("InserRowID").innerHTML = '';
        // data[0]["Employee"].forEach(emp => {
        //     console.log('emp2: ', emp);
        //     let element_columns = '';
        //     element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp.Emp_ID}" id="Employee" style="width: 100%;" readonly /></td>`;
        //     element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Emp_Name}" style="width: 100%;" readonly /></td>`;
        //     data[1]["Element"].forEach(element => {
        //         element_name_col = `${element.Element_Name}_${element.Element_ID}`
        //         element_columns += `<td><input type="number" class="form-control form-control-sm" value="${data[0]["Employee"][0]["Element_Amount"]["${element_name_col}"]}" style="width: 100%;"></td>`;
        //     });
        //     element_columns += '</tr>';
        //     document.getElementById("InserRowID").innerHTML += element_columns;
        //     counter++;
        // });


        document.getElementById("InserRowID").innerHTML = '';
        data[0]["Employee"].forEach(emp => {
            let element_columns = '<tr>';
            element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp.Emp_ID}" id="Employee" style="width: 100%;" readonly /></td>`;
            element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Emp_Name}" style="width: 100%;" readonly /></td>`;
            data[1]["Element"].forEach(element => {
                element_name_col = `${element.Element_Name}_${element.Element_ID}`;
                element_name_col = element_name_col.replace(/ /g, "_");  // Replace all spaces with underscores globally
                console.log('element_name_col: ', element_name_col);
                element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp["Element_Amount"][element_name_col] || ''}" style="width: 100%;"></td>`;
            });
            element_columns += '</tr>';
            document.getElementById("InserRowID").innerHTML += element_columns;
        });


    } catch (error) {
        console.error('Error fetching Grade:', error);
        return null;
    }
});

async function getAll_Dept_ByID(id) {
    try {
        const response = await fetch(`${BASE_URL}/monthly_all_ded/getall_dept/${id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        let temp = '';
        data.forEach(element => {
            temp += `<option value="${element.Dept_ID}">${element.Dept_Descr}</option>`;
        });
        document.getElementById("W_Department").innerHTML = temp;

    } catch (error) {
        console.error('Error fetching Grade:', error);
        return null;
    }
}

//  async function getAllDeptElemet(current_w_dept_id) {
//     const current_w_dept_id = 2;
//     // const current_w_dept_id = localStorage.getItem("Department");
//     try {
//         const response = await fetch(`${BASE_URL}getall_w_dept_element/${current_w_dept_id}`);
//         if (!response.ok) {
//             throw new Error('Failed to fetch Working Departments and Elements');
//         }
//         const data = await response.json();
//         let temp = '', temp2 = '', counter = 1;

//         console.log('data: ', data)

//         current_period_id = data.Period.ID 
//         document.getElementById("Period").value = data.Period.MNTH_NAME;
//         document.getElementById("Department").value = data.Department.Dept_Descr;

//         document.getElementById("InserRowHeadID").innerHTML = `<th style="width: 7%;">S. No</th><th style="width: 20%;">Employee</th>`;

//         data.Element.forEach(element => {
//             temp += `<th style="width: 20%;">${element.Element_Name}</th>`;
//         });

//         document.getElementById("InserRowHeadID").innerHTML += temp;

//         document.getElementById("InserRowID").innerHTML = '';
//         data.Employee.forEach(emp => {
//             let element_columns = '';
//             element_columns += `<tr><td class="text-center">${counter}</td>`;
//             element_columns += `<td>${emp.Emp_Name}</td>`;
//             data.Element.forEach(element => {
//                 element_columns += `<td><input type="number" class="form-control-sm"></td>`;
//             });
//             // console.log('element_columns: ', element_columns)
//             // table.row.add(element_columns).draw(false);
//             element_columns += '</tr>';
//             document.getElementById("InserRowID").innerHTML += element_columns;
//             counter++;
//         });

//     } catch (error) {
//         console.error('Error fetching Grade:', error);
//         return null;
//     }
// };

async function getAllDeptElemet() {
    const current_w_dept_id = 2;
    // const current_w_dept_id = localStorage.getItem("Department");
    try {
        const response = await fetch(`${BASE_URL}/monthly_all_ded/getall_w_dept_element/${current_w_dept_id}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Working Departments and Elements');
        }
        const data = await response.json();
        let temp = '', temp2 = '', counter = 1;

        console.log('data: ', data)

        current_period_id = data.Period.ID
        document.getElementById("Period").value = data.Period.MNTH_NAME;
        document.getElementById("Department").value = data.Department.Dept_Descr;

        document.getElementById("InserRowHeadID").innerHTML = `<th style="width: 13%;">Emp_ID</th><th style="width: 20%;">Employee_Name</th>`;

        data.Element.forEach(element => {
            temp += `<th style="width: 20%;">${element.Element_Name}</th>`;
        });

        document.getElementById("InserRowHeadID").innerHTML += temp;

        document.getElementById("InserRowID").innerHTML = '';
        data.Employee.forEach(emp => {
            console.log('emp: ', emp)
            let element_columns = '';
            element_columns += `<tr><td class="text-center"><input type="number" value="${emp.Element_ID}" class="form-control form-control-sm" style="width: 100%;"></td>`;
            element_columns += `<tr><td class="text-center"><input type="number" value="${emp.Element_Name}" class="form-control form-control-sm" style="width: 100%;"></td>`;
            data.Element.forEach(element => {
                element_columns += `<td><input type="number" class="form-control form-control-sm" style="width: 100%;"></td>`;
            });
            // console.log('element_columns: ', element_columns)
            // table.row.add(element_columns).draw(false);
            element_columns += '</tr>';
            document.getElementById("InserRowID").innerHTML += element_columns;
            counter++;
        });

    } catch (error) {
        console.error('Error fetching Grade:', error);
        return null;
    }
};


$(document).ready(function () {
    initializeDataTable();
    current_w_dept_id = localStorage.getItem("current_w_dept_id");
    current_w_dept_name = localStorage.getItem("current_w_dept_name");
    document.getElementById("Department").value = current_w_dept_name;
    W_deptID = 2;
    current_payrollperiod();
    getAll_Dept_ByID(W_deptID);
    // getAllDeptElemet(W_deptID);
    document.getElementById("CancelFormData").addEventListener('click', CancelFormAndGridData);
})

document.getElementById(INSERT_BUTTON_ID).addEventListener("click", function () {
    Insert_Monthly_PE();
});

// function Insert_Monthly_PE() {

//     let monthly_pe_obj = {}
//     let month_pe_col = []
//     const period = document.getElementById("Period").value;
//     $('#InserRowHeadID').each(function (index) {
//         let col_name = $(this).text()
//         // monthly_pe_obj[`${col_name}`] = "0"
//         month_pe_col.push(col_name)
//     })

//     $("InserRowID").find('tr').each(function () {
//         let monthly_pe_array = []

//         $(this).find('td input').each(function (index) {
//             if (columns.includes(index)) {
//                 let cell_value = $(this).find('input').val()
//                 if (index != 1) {
//                     monthly_pe_obj[`${month_pe_col[index]}`] = cell_value
//                 }
//             }
//         });

//         monthly_pe_array.push(monthly_pe_obj)
//     });

// }

async function current_payrollperiod() {
    const response = await fetch(`${BASE_URL}/monthly_all_ded/current_payrollperiod/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    if (!response.ok) {
        throw new Error("failed to assigned payroll element")
    }
    const data = await response.json();
    console.log("current_payrollperiod: ", data)
    document.getElementById("Period").value = data.MNTH_NAME
    current_period_id = data.PERIOD_ID
}

async function Insert_Monthly_PE() {
    let tableData = GetTableData()
    let W_Department = document.getElementById("W_Department").value
    console.log("table data: ", tableData)
    console.log("table W_Department: ", W_Department)
    const response = await fetch(`${BASE_URL}/monthly_all_ded/insert/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'table_data': tableData, 'W_Department': W_Department }),
    })
    if (!response.ok) {
        displayErrorMessage("Failed While assigning Elements")
    } else {
        displaySuccessMessage("Successfully Assigned Elements")
    }
    const data = await response.json();
}

function GetTableData() {
    let data = [];

    $('#GridID tbody tr').each(function () {
        let rowData = {};
        $(this).find('td').each(function (index) {
            let columnName = $('#GridID thead tr th').eq(index).attr('id');
            let cellValue = $(this).find('input').val();
            // console.log('celvalue: ', cellValue)
            if (cellValue == '') {
                cellValue = 0;
            }
            if (index == 0) {
                columnName = "Employee"
            }
            if (index != 1) {
                if (columnName !== "") {
                    rowData['Period'] = Number(current_period_id);
                    rowData[columnName] = Number(cellValue);
                }
            }
        });
        data.push(rowData);
    });

    return data;
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




