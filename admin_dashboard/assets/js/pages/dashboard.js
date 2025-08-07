document.addEventListener("DOMContentLoaded", async function () {

    // Helper function to get the CSS class for a user's password status badge
    function getRiskBadge(risk) {
        switch (risk) {
            case "Weak": return "bg-danger";
            case "Common": return "bg-warning";
            case "Strong": return "bg-success";
            default: return "bg-secondary";
        }
    }

    /**
     * Populates the four summary cards at the top of the page.
     * @param {object} summaryStats - The summary_stats object from the API.
     */
    function updateTopCards(summaryStats) {
        document.getElementById("balance").textContent = summaryStats.total_users;
        document.getElementById("revenue").textContent = summaryStats.strong_passwords; // Note: Template ID is 'revenue'
        document.getElementById("orders").textContent = summaryStats.weak_passwords;    // Note: Template ID is 'orders'
        document.getElementById("sales").textContent = summaryStats.common_passwords;   // Note: Template ID is 'sales'

        // Add color classes to card bodies
        document.getElementById("card-total-users").classList.add("bg-primary");
        document.getElementById("card-strong").classList.add("bg-success");
        document.getElementById("card-weak").classList.add("bg-danger");
        document.getElementById("card-common").classList.add("bg-warning");
    }

    /**
     * Calculates the overall security score and updates the display.
     * @param {object} summaryStats - The summary_stats object from the API.
     */
    function updateOverallScore(summaryStats) {
        const { total_users, strong_passwords } = summaryStats;
        const score = total_users > 0 ? Math.round((strong_passwords / total_users) * 100) : 0;
        document.getElementById("summaryScore").textContent = score + "%";
    }

    /**
     * Creates the bar chart showing the breakdown of password weaknesses.
     * @param {Array} users - The array of user objects from the API.
     */
    function createWeaknessChart(users) {
        const weaknessCounts = {
            "Missing Uppercase": users.filter(u => !u.has_upper).length,
            "Missing Digit": users.filter(u => !u.has_digit).length,
            "Common Password": users.filter(u => u.common_password).length,
            "Used Personal Info": users.filter(u => u.used_personal_info).length,
        };

        const ctxBar = document.getElementById("bar").getContext("2d");
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: Object.keys(weaknessCounts),
                datasets: [{
                    label: 'Users Affected',
                    data: Object.values(weaknessCounts),
                    backgroundColor: ['#ff9f40', '#ff6384', '#ffcd56', '#4bc0c0']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    /**
     * Creates the radial chart showing the overall risk composition.
     * @param {Array} users - The array of user objects from the API.
     */
    function createRiskRadialChart(users) {
        const totalUsers = users.length;
        if (totalUsers === 0) return;

        const commonPct = Math.round((users.filter(u => u.common_password).length / totalUsers) * 100);
        const personalInfoPct = Math.round((users.filter(u => u.used_personal_info).length / totalUsers) * 100);
        const weakPct = Math.round((users.filter(u => u.password_status === 'Weak').length / totalUsers) * 100);

        const options = {
            series: [commonPct, personalInfoPct, weakPct],
            chart: { height: 350, type: "radialBar" },
            plotOptions: {
                radialBar: {
                    dataLabels: {
                        name: { fontSize: "18px" },
                        value: { fontSize: "22px", formatter: (val) => val + "%" },
                        total: {
                            show: true,
                            label: "Avg Risk %",
                            formatter: () => Math.round((commonPct + personalInfoPct + weakPct) / 3) + "%"
                        },
                    },
                },
            },
            labels: ["Common PWD", "Personal Info", "Weak PWD"],
            colors: ['#ff6384', '#ff9f40', '#ffcd56'],
        };
        new ApexCharts(document.querySelector("#radialBars"), options).render();
    }

    /**
     * Populates the "Recent Login Activity" list.
     * @param {Array} logs - The array of log objects from the API.
     */
    function updateRecentLogins(logs) {
        const list = document.getElementById("recentLoginList");
        list.innerHTML = "";
        const recentLogs = logs.slice(0, 5); // Get the 5 most recent logs

        const statusBadges = { Success: "bg-success", Failed: "bg-danger" };

        recentLogs.forEach(log => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-start";
            li.innerHTML = `
                <div>
                    <div class="fw-bold">${log.email}</div>
                    <small class="text-muted">${log.timestamp}</small>
                </div>
                <span class="badge ${statusBadges[log.status] || 'bg-secondary'}">${log.status}</span>
            `;
            list.appendChild(li);
        });
    }

    /**
     * Sets up the searchable user audit table.
     * @param {Array} allUsers - The full array of user objects from the API.
     */
    function setupUserAuditTable(allUsers) {
        const tbody = document.getElementById("auditTableBody");
        const searchInput = document.getElementById("searchInput");

        function renderTable(usersToRender) {
            tbody.innerHTML = "";
            usersToRender.forEach(user => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${user.fullname}</td>
                    <td>${user.email}</td>
                    <td>${user.phone}</td>
                    <td>${user.department}</td>
                    <td><span class="badge ${getRiskBadge(user.password_status)}">${user.password_status}</span></td>
                `;
                tbody.appendChild(row);
            });
        }

        // Initial render with all users
        renderTable(allUsers);

        // Add search functionality
        searchInput.addEventListener("input", function () {
            const searchTerm = this.value.toLowerCase();
            const filtered = allUsers.filter(user =>
                user.fullname.toLowerCase().includes(searchTerm) ||
                user.email.toLowerCase().includes(searchTerm) ||
                user.department.toLowerCase().includes(searchTerm)
            );
            renderTable(filtered);
        });
    }


    /**
     * Main function to fetch all data and initialize the dashboard.
     */
    async function initializeDashboard() {
        try {
            const response = await fetch('/dashboard/api/data');
            if (!response.ok) throw new Error(`Network error: ${response.statusText}`);
            const data = await response.json();

            // Use the fetched data to update each component of the page
            updateTopCards(data.summary_stats);
            updateOverallScore(data.summary_stats);
            createWeaknessChart(data.users);
            createRiskRadialChart(data.users);
            updateRecentLogins(data.logs);
            setupUserAuditTable(data.users);

        } catch (error) {
            console.error("Failed to initialize dashboard:", error);
            // Optionally, display a global error message on the page
        }
    }

    initializeDashboard();
});