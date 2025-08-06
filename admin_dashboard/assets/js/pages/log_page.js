// assets/js/pages/log_page.js

// Sample logs (you can replace this with dynamic fetch or CSV parsing later)
const rawLogs = `
[2025-06-23 19:13:08] SUCCESS LOGIN: test@gmail.com from IP: 127.0.0.1
[2025-06-23 23:24:04] FAILED LOGIN: test@gmail.com from IP: 127.0.0.1
[2025-06-23 23:25:06] FAILED LOGIN: test@gmail.com from IP: 127.0.0.1
[2025-06-23 23:25:16] SUCCESS LOGIN: test@gmail.com from IP: 127.0.0.1
[2025-06-24 17:48:22] SUCCESS LOGIN: test@gmail.com from IP: 127.0.0.1
[2025-06-26 23:40:08] SUCCESS LOGIN: password@gmail.com from IP: 127.0.0.1
`;

// HTML Table container
const tableBody = document.getElementById("logsTableBody");

// Parse log lines
function parseLogLine(line) {
  const match = line.match(/\[(.*?)\] (SUCCESS|FAILED) LOGIN: (.*?) from IP: (.*)/);
  if (!match) return null;
  return {
    timestamp: match[1],
    status: match[2],
    email: match[3],
    ip: match[4]
  };
}

// Render the log entries
function renderLogs() {
  const logLines = rawLogs.trim().split("\n");
  for (const line of logLines) {
    const log = parseLogLine(line);
    if (!log) continue;

    const row = document.createElement("tr");
    const statusClass = log.status === "SUCCESS" ? "text-success" : "text-danger";

    row.innerHTML = `
      <td>${log.timestamp}</td>
      <td><span class="${statusClass}">${log.status}</span></td>
      <td>${log.email}</td>
      <td>${log.ip}</td>
    `;

    tableBody.appendChild(row);
  }
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", function () {
  renderLogs();

  // Optional: initialize DataTable
  const logTable = document.querySelector("#logTable");
  if (logTable) {
    new simpleDatatables.DataTable(logTable, {
      searchable: true,
      fixedHeight: true,
      perPage: 10,
    });
  }
});
