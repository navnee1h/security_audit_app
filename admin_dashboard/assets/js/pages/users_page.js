document.addEventListener("DOMContentLoaded", function () {
  const tableBody = document.getElementById("usersTableBody");
  const departments = ["HR", "Sales", "Tech", "Support", "Finance"];

  const getRandomItem = arr => arr[Math.floor(Math.random() * arr.length)];
  const getRandomBool = (prob = 0.5) => Math.random() < prob;

  function generateDummyUsers(count = 100) {
    const dummyUsers = [];
    for (let i = 0; i < count; i++) {
      const firstName = `User${i + 1}`;
      const email = `user${i + 1}@example.com`;
      const phone = `9${Math.floor(100000000 + Math.random() * 900000000)}`;
      const department = getRandomItem(departments);
      const user = {
        fullname: firstName,
        email: email,
        phone: phone,
        department: department,
        length_ok: getRandomBool(0.8),
        has_upper: getRandomBool(0.6),
        has_lower: true,
        has_digit: getRandomBool(0.7),
        has_special: getRandomBool(0.5),
        common_password: getRandomBool(0.2),
        used_personal_info: getRandomBool(0.3)
      };
      dummyUsers.push(user);
    }
    return dummyUsers;
  }

  function getPasswordStatus(user) {
    if (user.common_password) return "Common";
    if (!user.length_ok || !user.has_upper || !user.has_digit) return "Weak";
    return "Strong";
  }

  function getPasswordReason(user) {
    const reasons = [];
    if (!user.length_ok) reasons.push("Too short");
    if (!user.has_upper) reasons.push("No uppercase");
    if (!user.has_digit) reasons.push("No digit");
    if (!user.has_special) reasons.push("No special char");
    if (user.common_password) reasons.push("Common password");
    if (user.used_personal_info) reasons.push("Used personal info");
    return reasons.join(", ");
  }

  function getBadgeClass(status) {
    switch (status) {
      case "Weak": return "bg-danger";
      case "Common": return "bg-warning";
      case "Strong": return "bg-success";
      default: return "bg-secondary";
    }
  }

  // 1. Generate and inject dummy users into HTML table
  const users = generateDummyUsers(100);
  for (const user of users) {
    const status = getPasswordStatus(user);
    const reason = getPasswordReason(user);
    const badgeClass = getBadgeClass(status);

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${user.fullname}</td>
      <td>${user.email}</td>
      <td>${user.phone}</td>
      <td>${user.department}</td>
      <td><span class="badge ${badgeClass}">${status}</span></td>
      <td><small>${reason}</small></td>
      <td><button class="btn btn-sm btn-outline-primary">Notify</button></td>
    `;
    tableBody.appendChild(row);
  }

  // 2. Initialize simple-datatables AFTER injecting data
  const userTable = document.querySelector("#userTable");
  if (userTable) {
    new simpleDatatables.DataTable(userTable, {
      searchable: true,
      fixedHeight: true,
      perPage: 10,
    });
  }
});