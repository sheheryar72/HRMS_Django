const BASE_URL = '/monthly_all_ded/';
var table;
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

document.getElementById("W_Department").addEventListener("change", async function () {
    // const W_deptID = localStorage.getItem("W_deptID");
    const W_deptID = 2;
    const W_Department = document.getElementById("W_Department").value;
    try {
        const response = await fetch(`${BASE_URL}getall_dept_element/${W_deptID}/${W_Department}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Grade');
        }
        const data = await response.json();
        let temp = '', temp2 = '', counter = 1;

        // console.log("W_Department data: ", data);

        document.getElementById("InserRowHeadID").innerHTML = `<th style="width: 5%;">S. No</th><th style="width: 15%;">Employee</th>`;
        
        data[1]["Element"].forEach(element => {
            temp += `<th style="width: 20%;">${element.Element_Name}</th>`;
        });

        document.getElementById("InserRowHeadID").innerHTML += temp;

        document.getElementById("InserRowID").innerHTML = '';
        data[0]["Employee"].forEach(emp => {
            let element_columns = '';
            element_columns += `<tr><td class="text-center">${counter}</td>`;
            element_columns += `<td>${emp.Emp_Name}</td>`;
            data[1]["Element"].forEach(element => {
                element_columns += `<td><input type="number" class="form-control-sm"></td>`;
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
});



async function getAll_Dept_ByID(id) {
    try {
        const response = await fetch(`${BASE_URL}getall_dept/${id}`);
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

$(document).ready(function () {
    initializeDataTable();
    // const W_deptID = localStorage.getItem("W_deptID");
    W_deptID = 2
    getAll_Dept_ByID(W_deptID);
})
