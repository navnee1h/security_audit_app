document.addEventListener("DOMContentLoaded", async function () {
    const tableBody = document.getElementById("usersTableBody");
    const userTable = document.querySelector("#userTable");

    /**
     * Gets the correct CSS class for the status badge based on the status string.
     * @param {string} status - The password status ('Strong', 'Weak', 'Common').
     * @returns {string} A CSS class name.
     */
    function getBadgeClass(status) {
        switch (status) {
            case "Weak": return "bg-danger";
            case "Common": return "bg-warning";
            case "Strong": return "bg-success";
            default: return "bg-secondary";
        }
    }

    /**
     * Generates a human-readable string of reasons for a password's status.
     * @param {object} user - The user object from the API.
     * @returns {string} A comma-separated list of reasons.
     */
    function getPasswordReason(user) {
        const reasons = [];
        if (user.common_password) reasons.push("Common password");
        if (user.used_personal_info) reasons.push("Uses personal info");
        if (!user.length_ok) reasons.push("Too short");
        if (!user.has_upper) reasons.push("No uppercase letter");
        if (!user.has_digit) reasons.push("No digit");
        if (!user.has_special) reasons.push("No special character");

        // If the password is 'Strong', the reasons array will be empty.
        return reasons.length > 0 ? reasons.join(", ") : "N/A";
    }

    /**
     * Renders the user data into the HTML table.
     * @param {Array} users - An array of user objects from the API.
     */
    function renderUsersTable(users) {
        tableBody.innerHTML = ""; // Clear any dummy data

        if (!users || users.length === 0) {
            const row = tableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 7; // Span all 7 columns of the table
            cell.textContent = "No user data found.";
            cell.style.textAlign = 'center';
            return;
        }

        for (const user of users) {
            const status = user.password_status; // Get status directly from the API data
            const reason = getPasswordReason(user); // Calculate the reason string
            const badgeClass = getBadgeClass(status); // Get the badge color

            const row = document.createElement("tr");

            // [UPDATED] The button now has a 'btn-notify' class, data attributes to hold
            // the email and reason, and is disabled if the password is 'Strong'.
            row.innerHTML = `
                <td>${user.fullname}</td>
                <td>${user.email}</td>
                <td>${user.phone}</td>
                <td>${user.department}</td>
                <td><span class="badge ${badgeClass}">${status}</span></td>
                <td><small>${reason}</small></td>
                <td>
                    <button
                        class="btn btn-sm btn-outline-primary btn-notify"
                        data-email="${user.email}"
                        data-reason="${reason}"
                        ${status === 'Strong' ? 'disabled' : ''}>
                        Notify
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        }
    }

    // ---------------------- [NEW] EVENT LISTENER FOR NOTIFY BUTTONS ----------------------
    // We use event delegation on the table body to handle clicks on buttons that are
    // added dynamically.
    tableBody.addEventListener('click', async function(event) {
        // Check if a notify button was clicked
        if (event.target.classList.contains('btn-notify')) {
            const button = event.target;
            const email = button.dataset.email;
            const reason = button.dataset.reason;

            // Give visual feedback that something is happening
            button.textContent = 'Notifying...';
            button.disabled = true;

            try {
                // Send the notification data to the backend
                const response = await fetch('/admin/notify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: email, reason: reason }),
                });

                const result = await response.json();

                if (response.ok && result.status === 'success') {
                    // Success! Update the button to show it's done.
                    button.textContent = 'Notified';
                    button.classList.remove('btn-outline-primary');
                    button.classList.add('btn-success');
                } else {
                    // Handle failure from the server
                    console.error('Failed to send notification:', result.message);
                    button.textContent = 'Failed';
                    button.classList.remove('btn-outline-primary');
                    button.classList.add('btn-danger');
                }

            } catch (error) {
                // Handle network or other errors
                console.error('Error sending notification:', error);
                button.textContent = 'Error ❌';
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-danger');
            }
        }
    });

    /**
     * Main function to initialize the page.
     */
    async function initializePage() {
        try {
            const response = await fetch('/dashboard/api/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Render the table using the 'users' array from the API response
            renderUsersTable(data.users);

            // Initialize the simple-datatables library AFTER the table is populated
            if (userTable) {
                new simpleDatatables.DataTable(userTable, {
                    searchable: true,
                    perPage: 10,
                    labels: {
                        placeholder: "Search users...",
                        noRows: "No users found",
                        info: "Showing {start} to {end} of {rows} entries",
                    }
                });
            }

        } catch (error) {
            console.error("Failed to fetch user data:", error);
            const row = tableBody.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 7;
            cell.textContent = "Error loading user data.";
            cell.style.textAlign = 'center';
            cell.style.color = 'red';
        }
    }

    initializePage();
});