document.addEventListener("DOMContentLoaded", async function () {
    const tableBody = document.getElementById("logsTableBody");
    const logTable = document.querySelector("#logTable");

    /**
     * Renders the log entries into the HTML table.
     * @param {Array} logs - An array of log objects from the API.
     */
    function renderLogs(logs) {
        // Clear any old or dummy data from the table
        tableBody.innerHTML = "";

        // If there are no logs, display a helpful message
        if (!logs || logs.length === 0) {
            const row = tableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 4; // Span across all columns
            cell.textContent = "No login logs were found in the data file.";
            cell.style.textAlign = 'center';
            return;
        }

        // Loop through each log from the API and create a table row
        for (const log of logs) {
            const row = document.createElement("tr");
            
            // The status ('Success' or 'Failed') comes directly from the backend
            const statusClass = log.status === "Success" ? "text-success" : "text-danger";

            row.innerHTML = `
                <td>${log.timestamp}</td>
                <td><span class="${statusClass}">${log.status}</span></td>
                <td>${log.email}</td>
                <td>${log.ip}</td>
            `;

            tableBody.appendChild(row);
        }
    }

    /**
     * Main function to fetch data and initialize the page.
     */
    async function initializePage() {
        try {
            // Fetch the data from the API endpoint we created
            const response = await fetch('/dashboard/api/data');
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const data = await response.json();

            // Use the 'logs' array from the API response to render the table
            renderLogs(data.logs);

            // Initialize the simple-datatables library AFTER the table is populated
            if (logTable) {
                new simpleDatatables.DataTable(logTable, {
                    searchable: true,
                    perPage: 10,
                    labels: {
                        placeholder: "Search in logs...",
                        noRows: "No logs found",
                        info: "Showing {start} to {end} of {rows} entries",
                    }
                });
            }

        } catch (error) {
            console.error("Failed to fetch or render log data:", error);
            // Display a user-friendly error message in the table
            const row = tableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 4;
            cell.textContent = "Error loading data. Please check the console for details.";
            cell.style.textAlign = 'center';
            cell.style.color = 'red';
        }
    }

    // Run the main function when the page is ready
    initializePage();
});