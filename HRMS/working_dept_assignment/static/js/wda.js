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


$(document).ready(function () {
    // initializeDataTable();

    // $('#GridID1 tbody').on('click', 'tr', handleTableRowClick);

    // document.getElementById(INSERT_BUTTON_ID).addEventListener('click', handleInsertClick);

    // document.getElementById(UPDATE_BUTTON_ID).addEventListener('click', handleUpdateClick);

    // document.getElementById(CANCEL_BUTTON_ID).addEventListener('click', handleCancelClick);

    // $(document).on('click', function () {
    //     if (event.srcElement.className != 'submit-btn')
    //         document.getElementById("alertId").innerHTML = "";
    // });

});

window.addEventListener('load', function() {
    alert('Page fully loaded');
});

// window.onload = function () {
//     getAllDepartment();
//     getAllElement();
//     // Uncomment if needed
//     // GetAllWDAByID(2);
// };






