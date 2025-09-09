const BASE_URL = window.location.origin;

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

function get_active_period() {
    getAllDataFromDB(`${BASE_URL}/salaryprocess/get_active_period`, 'Payroll Period').then((data) => {
        console.log("getall_payrollperiod response: ", data);
        var temp = `<option value="${data[0].Payroll_ID}">${data[0].MNTH_SHORT_NAME} - ${data[0].Yr}</option>`
        // var temp = `<option value="${data[0].Payroll_ID}">${data[0].MNTH_SHORT_NAME} - ${data[0].Yr}</option>`
        // var temp = `<option value="${data.PAYROLL_ID}">${data.MNTH_NAME} - ${data.FinYear}</option>`
        // var temp = `${data.MNTH_NAME} - ${data.FinYear}`
        document.getElementById("Payroll_ID").innerHTML = temp;
    });
}


async function transfer_data_to_salary_process(payroll_id) {
    try {
        const response = await fetch(`${BASE_URL}/payrollsheet/execute_monthly_pay_sheet/${payroll_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to run Payroll Sheet: ${errorData.error}`);
        }

        const data = await response.json();
        console.log("data: ", data);

        // Populate table with data
        // populateTable(data.data);

        alert("Monthly payroll sheet successfully!");
    } catch (error) {
        console.error("Error running Payroll Sheet:", error.message);
        alert("Error running Payroll Sheet: " + error.message);
    }
}



function populateTable(data) {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; // Clear existing rows`

    console.log('populateTable data: ', data)

    data.forEach(record => {
        const row = document.createElement('tr');

        // Add cells for each field
        Object.values(record).forEach(value => {
            const cell = document.createElement('td');
            cell.style.textAlign = "right"
            cell.textContent = value !== null ? value : 'N/A'; // Display 'N/A' for null values
            row.appendChild(cell);
        });

        tableBody.appendChild(row);
    });
}


// async function transfer_data_to_salary_process(payroll_id) {
//     try {
//         const response = await fetch(`${BASE_URL}/payrollsheet/execute_monthly_pay_sheet/${payroll_id}/`, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         });

//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(`Failed to run Payroll Sheet: ${errorData.error}`);
//         }

//         const data = await response.json();
//         console.log("data: ", data);
//         alert("Monthly process completed successfully!");
//     } catch (error) {
//         console.error("Error running Payroll Sheet:", error.message);
//         alert("Error running Payroll Sheet: " + error.message);
//     }
// }


document.getElementById("monthly_paysheet_btn").addEventListener('click', function() {
    // var userConfirmation = confirm("Do you want to run the monthly process?");
    const payroll_id = document.getElementById("Payroll_ID").value;
    transfer_data_to_salary_process(payroll_id);

    // if (userConfirmation) {
    //     // alert("Running the monthly process...");
    // } else {
    //     alert("Monthly process was cancelled.");
    // }
});


// Modify exportToExcel to be an async function
async function exportToExcel() {
    try {
        const payrollId = document.getElementById('Payroll_ID').value; // Assuming you select payroll ID from a dropdown
        const data = await get_payrollsheet_data(payrollId); // Await the data from the async function

        console.log('export to excel data: ', data)

        if (!data || !data.data || data.data.length === 0) {
            alert("No data available to export.");
            return;
        }

        // Convert JSON data to worksheet
        const worksheet = XLSX.utils.json_to_sheet(data.data);

        // Create a workbook and add the worksheet
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Payroll Data');

        // Generate Excel file and prompt download
        XLSX.writeFile(workbook, 'Payroll_Sheet.xlsx');
    } catch (error) {
        console.error("Error exporting to Excel:", error.message);
        alert("Error exporting to Excel: " + error.message);
    }
}

// Modify get_payrollsheet_data to accept a payroll_id parameter and call it correctly
async function get_payrollsheet_data(payroll_id) {
    try {
        const response = await fetch(`${BASE_URL}/payrollsheet/monthly-pay-sheet/${payroll_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to run Payroll Sheet: ${errorData.error}`);
        }

        const data = await response.json();
        console.log('get_payrollsheet_data data: ', data)
        return data;
    } catch (error) {
        console.error("Error running Payroll Sheet:", error.message);
        alert("Error running Payroll Sheet: " + error.message);
    }
}

// Add event listener to the export button
// document.getElementById('export_paysheet_btn').addEventListener('click', exportToExcel);


$(document).ready(function () {
    get_active_period()
});
