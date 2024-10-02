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

// function getall_payrollperiod() {
//     getAllDataFromDB(`${BASE_URL}/salaryprocess/getall_payrollperiod`, 'Payroll Period').then((data) => {
//         console.log("getall_payrollperiod response: ", data);
//         var temp = '';
//         for (var i = 0; i < data.length; i++) {
//             temp += `<option value="${data[i].PAYROLL_ID}">${data[i].MNTH_NAME}</option>`
//         }
//         document.getElementById("Payroll_ID").innerHTML = temp;
//     });
// }


function get_active_period() {
    getAllDataFromDB(`${BASE_URL}/salaryprocess/get_active_period`, 'Payroll Period').then((data) => {
        console.log("getall_payrollperiod response: ", data);
        var temp = `<option value="${data[0].Payroll_ID}">${data[0].MNTH_SHORT_NAME} - ${data[0].Yr}</option>`
        // var temp = `${data.MNTH_NAME} - ${data.FinYear}`
        document.getElementById("Payroll_ID").innerHTML = temp;
    });
}


// async function transfer_data_to_salary_process(payroll_id, fuel_rate) {
//     try {
//         const response = await fetch(`${BASE_URL}/salaryprocess/execute_salary_process/${payroll_id}/${fuel_rate}/`, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         });

//         // Handle response based on status code
//         if (response.status === 404) {
//             throw new Error('Payroll period not found');
//         }

//         if (response.status === 400) {
//             // Handle specific client errors if you use 400 for payroll not finalized
//             const errorData = await response.json();
//             throw new Error(`Payroll is not finalized: ${errorData.Message}`);
//         }

//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(`Failed to run salary process: ${errorData.Message}`);
//         }

//         // Parse successful response
//         const data = await response.json();
//         console.log("data: ", data);
//         alert("Monthly process completed successfully!");
//     } catch (error) {
//         console.error("Error running salary process:", error.message);
//         alert("Error running salary process: " + error.message);
//     }
// }


async function transfer_data_to_salary_process(payroll_id, fuel_rate) {
    try {
        const response = await fetch(`${BASE_URL}/salaryprocess/execute_salary_process/${payroll_id}/${fuel_rate}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.status == 506) {
            const errorData = await response.json();
            throw new Error(`Payroll is not finalized: ${errorData.error}`);
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Failed to run salary process: ${errorData.error}`);
        }

        const data = await response.json();
        console.log("data: ", data);
        alert("Monthly process completed successfully!");
    } catch (error) {
        console.error("Error running salary process:", error.message);
        alert("Error running salary process: " + error.message);
    }
}


document.getElementById("monthly_process_btn").addEventListener('click', function() {
    var userConfirmation = confirm("Do you want to run the monthly process?");
    const payroll_id = document.getElementById("Payroll_ID").value;
    const fuel_rate = document.getElementById("fuel_rate").value;

    if (userConfirmation) {
        alert("Running the monthly process...");
        transfer_data_to_salary_process(payroll_id, fuel_rate);
    } else {
        alert("Monthly process was cancelled.");
    }
});


$(document).ready(function () {
    get_active_period()
});
