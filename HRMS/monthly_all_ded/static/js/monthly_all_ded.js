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
    // const W_deptID = 2;
    const W_deptID = document.getElementById("Current_Department").value;
    const W_Department = document.getElementById("W_Department").value;
    try {
        const response = await fetch(`${BASE_URL}/monthly_all_ded/getall_dept_element/${W_deptID}/${W_Department}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        let temp = '', temp2 = '', counter = 1;

        // console.log("W_Department data: ", data);

        document.getElementById("InserRowHeadID").innerHTML =
            `<th style="width: 12%;">Emp ID</th><th style="width: 40%;">Emp Name</th><th style="width: 15%;">HR Code</th><th style="width: 10%;">Grade</th>`;

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
        let maxRows = data[1]["Element"].reduce((max, element) => Math.max(max, element.rows), 0);

        console.log("new data loop")

        data[0]["Employee"].forEach(emp => {
            let element_columns = '<tr>';
            element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp.Emp_ID}" id="Employee"  readonly /></td>`;
            element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Emp_Name}" readonly /></td>`;
            element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.HR_Emp_ID}"  readonly /></td>`;
            element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Grade_Descr}" readonly /></td>`;

            data[1]["Element"].forEach((element, index) => {
                element_name_col = `${element.Element_Name}_${element.Element_ID}`;
                element_name_col = element_name_col.replace(/ /g, "_");
                table_row_length = document.getElementById("InserRowID").rows.length

                single_emp_data = data[2]['Emp_Element_Status'].filter(x => x.Emp_ID == emp.Emp_ID)

                // console.log('single_emp_data: ', single_emp_data)

                let readonly = '';
                if (!single_emp_data.some(obj => obj.Element_ID === element.Element_ID)) {
                    readonly = 'readonly'
                    console.log('not element.Element_ID: ', element.Element_ID)
                } else {
                    // console.log('not element.Element_ID: ', element.Element_ID)
                }

                // console.log(data[2]['Emp_Element_Status'].filter(x=>x.Emp_ID == emp.Emp_ID))
                // let readonly = 5 >= table_row_length ? '' : 'readonly'; // Check if the current row exceeds the maximum rows for this column
                // debugger

                element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp["Element_Amount"][element_name_col] || ''}"  ${readonly}></td>`;
            });

            element_columns += '</tr>';
            document.getElementById("InserRowID").innerHTML += element_columns;
        });

        // document.getElementById("InserRowID").innerHTML = '';
        // data[0]["Employee"].forEach(emp => {
        //     console.log('emp: ', emp)
        //     let element_columns = '<tr>';
        //     element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp.Emp_ID}" id="Employee" style="width: 100%;" readonly /></td>`;
        //     element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Emp_Name}" style="width: 100%;" readonly /></td>`;
        //     element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.HR_Emp_ID}" style="width: 100%;" readonly /></td>`;
        //     element_columns += `<td><input type="text" class="form-control form-control-sm" value="${emp.Grade_Descr}" style="width: 100%;" readonly /></td>`;
        //     data[1]["Element"].forEach(element => {
        //         element_name_col = `${element.Element_Name}_${element.Element_ID}`;
        //         element_name_col = element_name_col.replace(/ /g, "_");  // Replace all spaces with underscores globally
        //         // console.log('element_name_col: ', element_name_col);
        //         console.log('element.Element_ID: ', element.Element_ID)
        //         element_columns += `<td><input type="number" class="form-control form-control-sm" value="${emp["Element_Amount"][element_name_col] || ''}" style="width: 100%;"></td>`;
        //     });
        //     element_columns += '</tr>';
        //     document.getElementById("InserRowID").innerHTML += element_columns;
        // });


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
    W_deptID = 1;
    current_payrollperiod();
    getAllDepartmentFromAPI();

    w_dept = document.getElementById("W_Department");
    if(w_dept.length == 1){
        alert(w_dept)
    }

    // getAll_Dept_ByID(W_deptID);
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
            if (index != 1 && index != 2 && index != 3) {
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

document.getElementById("exportData").addEventListener('click', async function () {
    exportToExcel()
});

async function getDataFromAPI() {
    try {
        const W_deptID = 2;
        const response = await fetch(`${BASE_URL}/monthly_all_ded/export_template/${W_deptID}`);
        if (!response.ok) {
            throw new Error('Some Error while Exporting Template');
        }
        const data = await response.json();
        console.log("Export Data: ", data);
        return data;
    } catch (error) {
        console.error('Error fetching Grade:', error);
    }
}

async function getAllDepartmentFromAPI() {
    try {
        const W_deptID = 2;
        const response = await fetch(`${BASE_URL}/department/api/getall`);
        if (!response.ok) {
            throw new Error('Some Error while Exporting Template');
        }
        const data = await response.json();
        console.log("getAllDepartmentFromAPI: ", data);
        let depts = ''
        data.forEach(item => {
            depts += `<option value="${item.Dept_ID}">${item.Dept_Descr}</option>`
        });
        document.getElementById("Current_Department").innerHTML = depts
        // return data;
    } catch (error) {
        console.error('Error fetching Grade:', error);
    }
}

document.getElementById("Current_Department").addEventListener('click', function () {
    let W_deptID = this.value
    getAll_Dept_ByID(W_deptID);
})

async function exportToExcel() {
    try {
        // Fetch data from API
        const data = await getDataFromAPI();
        console.log("exportToExcel exportToExcel: ", data)

        // const columns = ['Emp_ID', 'Emp_Name', 'Basic_Salary_01', 'Medical_Allowance_2', 'Conveyance_Allowance_3', 'Overtime_Allowance_4',
        //     'House_Rent_Allowanc_5', 'Utilities_Allowance_6', 'Meal_Allowance_7', 'Arrears_8', 'Bike_Maintainence_9', 'Incentives_10',
        //     'Device_Reimbursment_11', 'Communication_12', 'Bonus_13', 'Other_Allowance_14', 'Loan_15', 'Advance_Salary_16',
        //     'EOBI_17', 'Income_Tax_18', 'Absent_Days_19', 'Device_Deduction_20', 'Over_Utilizaton_Mobile_21', 'Vehicle_or_Fuel_Deduction_22',
        //     'Pandamic_Deduction_23', 'Late_Days_24', 'Other_Deduction_25', 'Mobile_Installment_26', 'Food_Panda_27'];
        const columns = ['Emp_ID', 'Emp_Name']
        data.Element.map(obj => {
            let element_col_name = `${obj.W_All_Ded_Element_ID__Element_Name}_${obj.W_All_Ded_Element_ID__Element_ID}`
            let element_col_name2 = element_col_name.replace(/ /g, "_");
            columns.push(element_col_name2)
        })

        console.log('columns: ', columns)

        // Extract values for each row
        const rows = data.Employee.map(obj => {
            // Fill the first two columns with Emp_ID and Emp_Name values
            const row = [obj['Emp_ID'], obj['Emp_Name']];
            // Fill the rest of the columns with empty strings
            for (let i = 2; i < 27; i++) {
                row.push('');
            }
            return row;
        });

        // Create workbook and worksheet
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.aoa_to_sheet([columns, ...rows]);

        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, 'Monthly_Payroll_Template');

        // Export the workbook as Excel file
        XLSX.writeFile(wb, 'Monthly_Payroll_Template.xlsx');
    } catch (error) {
        console.error('Error exporting data:', error);
    }
}

document.getElementById("importData").addEventListener('click', async function () {
    try {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        Insert_Monthly_PE_By_Excel(file);
    } catch (error) {
        console.error('Error:', error);
    }
});

async function Insert_Monthly_PE_By_Excel(file) {
    try {
        let tableData = await importFromExcel(file);
        let W_Department = document.getElementById("W_Department").value
        console.log("table data: ", tableData)
        console.log("table W_Department: ", W_Department)
        const response = await fetch(`${BASE_URL}/monthly_all_ded/Insert_from_excel/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'table_data': tableData, 'W_Department': W_Department, 'Period': current_period_id }),
        })
        if (!response.ok) {
            displayErrorMessage("Failed While assigning Elements")
        } else {
            displaySuccessMessage("Successfully Assigned Elements")
        }
        const data = await response.json();
    } catch (error) {
        console.error('Error inserting data:', error);
        displayErrorMessage("Failed While assigning Elements")
    }
}

function importFromExcel(file) {
    return new Promise((resolve, reject) => {
        try {
            const reader = new FileReader();
            reader.onload = function (event) {
                const data = new Uint8Array(event.target.result);
                const wb = XLSX.read(data, { type: 'array' });
                const ws = wb.Sheets[wb.SheetNames[0]];
                const jsonData = XLSX.utils.sheet_to_json(ws, { header: 1 });
                const columns = jsonData[0];
                const dictionary = {};
                for (let i = 0; i < columns.length; i++) {
                    const columnName = columns[i];
                    dictionary[columnName] = [];
                    for (let j = 1; j < jsonData.length; j++) {
                        dictionary[columnName].push(jsonData[j][i]);
                    }
                }
                console.log('Dictionary of arrays:', dictionary);
                resolve(dictionary); // Resolve the promise with the processed data
            };
            reader.readAsArrayBuffer(file);
        } catch (error) {
            console.error('Error importing data:', error);
            reject(error); // Reject the promise if an error occurs
        }
    });
}

// async function Insert_Monthly_PE_By_Excel(file) {
//     let tableData = await importFromExcel(file);
//     let W_Department = document.getElementById("W_Department").value
//     console.log("table data: ", tableData)
//     console.log("table W_Department: ", W_Department)
//     const response = await fetch(`${BASE_URL}/monthly_all_ded/Insert_from_excel/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ 'table_data': tableData, 'W_Department': W_Department }),
//     })
//     if (!response.ok) {
//         displayErrorMessage("Failed While assigning Elements")
//     } else {
//         displaySuccessMessage("Successfully Assigned Elements")
//     }
//     const data = await response.json();
// }

// function importFromExcel(file) {
//     try {
//         console.log('file: ', file);
//         const reader = new FileReader(); // Create a new FileReader object
//         reader.onload = function (event) {
//             const data = new Uint8Array(event.target.result); // Convert the file data to Uint8Array
//             const wb = XLSX.read(data, { type: 'array' }); // Read the Excel file using XLSX
//             const ws = wb.Sheets[wb.SheetNames[0]]; // Assume the data is in the first sheet
//             const jsonData = XLSX.utils.sheet_to_json(ws, { header: 1 }); // Parse the data into an array of objects
//             const columns = jsonData[0]; // Extract column headers
//             const dictionary = {}; // Initialize the dictionary of arrays
//             // Iterate over columns
//             for (let i = 0; i < columns.length; i++) {
//                 const columnName = columns[i];
//                 dictionary[columnName] = [];
//                 // Iterate over rows (skip the first row as it contains column headers)
//                 for (let j = 1; j < jsonData.length; j++) {
//                     // Push data into the corresponding array
//                     dictionary[columnName].push(jsonData[j][i]);
//                 }
//             }
//             // Log the dictionary
//             console.log('Dictionary of arrays:', dictionary);
//             return dictionary
//         };
//         reader.readAsArrayBuffer(file); // Read the file as an array buffer
//     } catch (error) {
//         console.error('Error importing data:', error);
//     }
// }

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




