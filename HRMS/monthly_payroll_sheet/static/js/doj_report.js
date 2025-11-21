const BASE_URL = window.location.origin;

// -----------------------------
// Populate Table (DataTable)
// -----------------------------
function populateTable(data) {
    const tableBody = document.getElementById("table-body");
    tableBody.innerHTML = "";

    data.forEach(item => {
        const row = `
            <tr>
                <td>${item.TYPE || "N/A"}</td>
                <td>${item.Emp_Name || "N/A"}</td>
                <td>${item.HR_Emp_ID || "N/A"}</td>
                <td>${item.Joining_Date || "N/A"}</td>
                <td>${item.Emp_Status ? "Active" : "In-Active"}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML("beforeend", row);
    });

    // Destroy old DataTable if exists
    if ($.fn.DataTable.isDataTable("#dojTable")) {
        $("#dojTable").DataTable().clear().destroy();
    }

    // Initialize DataTable
    $("#dojTable").DataTable({
        pageLength: 10,
        lengthMenu: [10, 20, 50, 100],
        responsive: true,
        autoWidth: false,
        searching: true,
        ordering: true,
        language: {
            search: "Search Employee:",
            lengthMenu: "Show _MENU_ entries",
            paginate: {
                previous: "Prev",
                next: "Next"
            }
        }
    });
}

// -----------------------------
// Fetch DOJ Report (POST)
// -----------------------------
async function get_DOJ_report() {
    const from_date = document.getElementById("from_date").value;
    const to_date = document.getElementById("to_date").value;

    try {
        const response = await fetch(`${BASE_URL}/payrollsheet/get_doj_report/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                from_date: from_date || null,
                to_date: to_date || null
            })
        });

        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }

        const json = await response.json();
        // debugger
        if (json.status === "success") {
            populateTable(json.data);
        } else {
            alert(json.message || "Error fetching report");
        }

    } catch (error) {
        console.error("Error fetching report:", error);
        alert(error.message);
    }
}

// -----------------------------
// Button Click Handler
// -----------------------------
document.getElementById("monthly_paysheet_btn").addEventListener("click", get_DOJ_report);
