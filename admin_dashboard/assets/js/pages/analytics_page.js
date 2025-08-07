document.addEventListener("DOMContentLoaded", async function () {

    /**
     * Processes the raw user data from the API to group password issues by department.
     * @param {Array} users - The array of user objects from the API.
     * @returns {Object} Data structured for the Chart.js bar chart.
     */
    function processDepartmentData(users) {
        const departmentStats = {};

        // Loop through each user to count their issues and group by department
        for (const user of users) {
            const dept = user.department || 'Unknown';
            if (!departmentStats[dept]) {
                departmentStats[dept] = { weak: 0, common: 0, personal: 0 };
            }

            if (user.password_status === 'Weak') {
                departmentStats[dept].weak++;
            }
            if (user.password_status === 'Common') {
                departmentStats[dept].common++;
            }
            if (user.used_personal_info) {
                departmentStats[dept].personal++;
            }
        }

        const labels = Object.keys(departmentStats);
        return {
            labels: labels,
            datasets: [
                {
                    label: "Weak Passwords",
                    data: labels.map(label => departmentStats[label].weak),
                    backgroundColor: "#f87171"
                },
                {
                    label: "Common Passwords",
                    data: labels.map(label => departmentStats[label].common),
                    backgroundColor: "#fbbf24"
                },
                {
                    label: "Personal Info Used",
                    data: labels.map(label => departmentStats[label].personal),
                    backgroundColor: "#6366f1"
                }
            ]
        };
    }

    /**
     * Processes raw log data to group login attempts by date.
     * @param {Array} logs - The array of log objects from the API.
     * @returns {Object} Data structured for the Chart.js line chart.
     */
    function processLoginData(logs) {
        const dailyActivity = {};
        const sortedLogs = logs.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        for (const log of sortedLogs) {
            const date = new Date(log.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            if (!dailyActivity[date]) {
                dailyActivity[date] = { success: 0, failed: 0 };
            }
            log.status === 'Success' ? dailyActivity[date].success++ : dailyActivity[date].failed++;
        }

        const labels = Object.keys(dailyActivity);
        return {
            labels: labels,
            datasets: [
                {
                    label: "Success Logins",
                    data: labels.map(label => dailyActivity[label].success),
                    borderColor: "#10b981",
                    backgroundColor: "#10b98133",
                    fill: true,
                    tension: 0.4
                },
                {
                    label: "Failed Logins",
                    data: labels.map(label => dailyActivity[label].failed),
                    borderColor: "#ef4444",
                    backgroundColor: "#ef444433",
                    fill: true,
                    tension: 0.4
                }
            ]
        };
    }

    /**
     * Initializes all charts on the page with data from the API.
     */
    async function initializeCharts() {
        try {
            const response = await fetch('/dashboard/api/data');
            if (!response.ok) throw new Error(`Network error: ${response.statusText}`);
            const data = await response.json();

            // --- 1. Password Strength Distribution (Pie Chart) ---
            const pieCtx = document.getElementById("strengthPieChart").getContext("2d");
            new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels: ["Strong", "Weak", "Common"],
                    datasets: [{
                        data: [
                            data.summary_stats.strong_passwords,
                            data.summary_stats.weak_passwords,
                            data.summary_stats.common_passwords
                        ],
                        backgroundColor: ["#34d399", "#f87171", "#fbbf24"],
                    }]
                },
                options: { responsive: true, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
            });

            // --- 2. Department-wise Password Issues (Bar Chart) ---
            const departmentData = processDepartmentData(data.users);
            const departmentBarCtx = document.getElementById("departmentBarChart").getContext("2d");
            new Chart(departmentBarCtx, {
                type: 'bar',
                data: departmentData,
                options: { responsive: true, scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } } }
            });

            // --- 3. Login Activity Over Time (Line Chart) ---
            const loginData = processLoginData(data.logs);
            const loginCtx = document.getElementById("loginLineChart").getContext("2d");
            new Chart(loginCtx, {
                type: 'line',
                data: loginData,
                options: { responsive: true, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: true } } }
            });

        } catch (error) {
            console.error("Failed to fetch or initialize charts:", error);
            // You can add a user-friendly error message on the page here if you want
        }
    }

    initializeCharts();
});