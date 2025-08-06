var chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  info: '#41B1F9',
  blue: '#3245D1',
  purple: 'rgb(153, 102, 255)',
  grey: '#EBEFF6'
};

// 🔢 Generate 1000 dummy users with random traits
const generateFakeUsers = (count = 1000) => {
  const data = [];
  for (let i = 0; i < count; i++) {
    data.push({
      email: `user${i}@example.com`,
      length_ok: Math.random() > 0.2,
      has_upper: Math.random() > 0.4,
      has_lower: true, // assume always has lowercase
      has_digit: Math.random() > 0.3,
      has_special: Math.random() > 0.5,
      common_password: Math.random() > 0.85,
      used_personal_info: Math.random() > 0.75,
    });
  }
  return data;
};

const securityData = generateFakeUsers(1000);

// 📊 Dashboard Metrics
const dashboardData = {
  balance: securityData.length,
  revenue: securityData.filter(u => u.common_password).length,
  orders: securityData.filter(u => u.used_personal_info).length,
  sales: securityData.filter(u =>
    u.length_ok && u.has_upper && u.has_digit && u.has_special
  ).length,
};

// 🎨 Color themes for each card
const cardColors = {
  "card-total-users": "bg-primary text-white",
  "card-strong": "bg-success text-white",
  "card-weak": "bg-danger text-white",
  "card-common": "bg-warning text-dark"
};

// 📤 Inject values and styles into dashboard cards
document.addEventListener("DOMContentLoaded", function () {
  // Inject dashboard data
  document.getElementById("balance").textContent = dashboardData.balance;
  document.getElementById("revenue").textContent = dashboardData.sales;
  document.getElementById("orders").textContent = dashboardData.orders;
  document.getElementById("sales").textContent = dashboardData.revenue;

  // Add color classes to card bodies
  document.getElementById("card-total-users").classList.add("bg-primary");
  document.getElementById("card-strong").classList.add("bg-success");
  document.getElementById("card-weak").classList.add("bg-danger");
  document.getElementById("card-common").classList.add("bg-warning");
});


// Simulated audit results (Replace with actual audit logic)
  const passwordAuditResults = [
    { risk: "Weak" },
    { risk: "Common" },
    { risk: "Weak" },
    { risk: "Strong" },
    { risk: "Strong" }
  ];

  // Function to calculate the percentage of strong passwords
  function calculateOverallScore(data) {
    const total = data.length;
    const strongCount = data.filter(d => d.risk === "Strong").length;
    return Math.round((strongCount / total) * 100);
  }

  // JS will inject the calculated score into the #summaryScore element
  document.addEventListener("DOMContentLoaded", function () {
    const score = calculateOverallScore(passwordAuditResults);
    document.getElementById("summaryScore").textContent = score + "%";
  });


// 📈 Bar Chart: Password Weakness Breakdown
const passwordMetricCounts = {
  "Missing Uppercase": securityData.filter(u => !u.has_upper).length,
  "Missing Digit": securityData.filter(u => !u.has_digit).length,
  "Common Password": dashboardData.revenue,
  "Used Personal Info": dashboardData.orders,
};

const ctxBar = document.getElementById("bar").getContext("2d");
const barChart = new Chart(ctxBar, {
  type: 'bar',
  data: {
    labels: Object.keys(passwordMetricCounts),
    datasets: [{
      label: 'Users Affected',
      data: Object.values(passwordMetricCounts),
      backgroundColor: [
        chartColors.orange,   // Missing Uppercase
        chartColors.red,      // Missing Digit
        chartColors.yellow,   // Common Password
        chartColors.purple    // Used Personal Info
      ]
    }]
  },
  options: {
    responsive: true,
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          suggestedMax: 500,
          padding: 10,
        },
        gridLines: { drawBorder: false }
      }],
      xAxes: [{
        gridLines: { display: false, drawBorder: false }
      }]
    },
    legend: { display: false },
    title: {
      display: true,
      text: 'Password Weakness Breakdown (1000 Users)',
    }
  }
});


// 🌀 Radial Chart: Risk Composition
// Total users
const totalUsers = securityData.length;

// Count issues independently
const countCommon = securityData.filter(u => u.common_password).length;
const countPersonalInfo = securityData.filter(u => u.used_personal_info).length;
const countWeak = securityData.filter(u =>
  !(u.length_ok && u.has_upper && u.has_digit && u.has_special)
).length;

// Convert to percentages for radial chart
const radialChartData = [
  Math.round((countCommon / totalUsers) * 100),
  Math.round((countPersonalInfo / totalUsers) * 100),
  Math.round((countWeak / totalUsers) * 100),
];

const radialBarsOptions = {
  series: radialChartData,
  chart: {
    height: 350,
    type: "radialBar",
  },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { fontSize: "18px" },
        value: {
          fontSize: "22px",
          formatter: function (val) {
            return val + "%";
          },
        },
        total: {
          show: true,
          label: "Avg Risk %",
          formatter: function () {
            const avg = radialChartData.reduce((a, b) => a + b, 0) / 3;
            return Math.round(avg) + "%";
          },
        },
      },
    },
  },
  labels: ["Common PWD", "Personal Info", "Weak PWD"],
  colors: [chartColors.red, chartColors.orange, chartColors.yellow],
};

const radialBars = new ApexCharts(document.querySelector("#radialBars"), radialBarsOptions);
radialBars.render();


// Generate 15 sample users
const users = Array.from({ length: 15 }, (_, i) => ({
  fullname: `User${i + 1}`,
  email: `user${i + 1}@example.com`,
  phone: `99999${i + 1}`,
  department: ["HR", "Sales", "IT", "Support"][i % 4]
}));

// Generate matching security data
const security = users.map((user, i) => ({
  email: user.email,
  length_ok: i % 2 === 0,
  has_upper: i % 3 !== 0,
  has_lower: true,
  has_digit: i % 4 !== 0,
  has_special: i % 5 === 0,
  common_password: i % 6 === 0,
  used_personal_info: i % 7 === 0
}));

// Merge and tag with risk status
const mergedUsers = users.map(user => {
  const sec = security.find(s => s.email === user.email);
  const passwordRisk = getPasswordStatus(sec);
  return { ...user, passwordRisk };
});

// Risk level logic
function getPasswordStatus(sec) {
  if (!sec) return "Unknown";
  if (sec.common_password) return "Common";
  if (!sec.length_ok || !sec.has_upper || !sec.has_digit) return "Weak";
  return "Strong";
}

function getRiskBadge(risk) {
  switch (risk) {
    case "Weak": return "bg-danger";
    case "Common": return "bg-warning";
    case "Strong": return "bg-success";
    default: return "bg-secondary";
  }
}

// Inject into table
function renderAuditTable(data) {
  const tbody = document.getElementById("auditTableBody");
  tbody.innerHTML = "";
  data.forEach(user => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${user.fullname}</td>
      <td>${user.email}</td>
      <td>${user.phone}</td>
      <td>${user.department}</td>
      <td><span class="badge ${getRiskBadge(user.passwordRisk)}">${user.passwordRisk}</span></td>
    `;
    tbody.appendChild(row);
  });
}

// Search functionality
document.getElementById("searchInput").addEventListener("input", function () {
  const searchTerm = this.value.toLowerCase();
  const filtered = mergedUsers.filter(user =>
    user.fullname.toLowerCase().includes(searchTerm) ||
    user.email.toLowerCase().includes(searchTerm) ||
    user.department.toLowerCase().includes(searchTerm)
  );
  renderAuditTable(filtered);
});

// Initial render
renderAuditTable(mergedUsers);


  // Inject users into HTML table
  document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("#table1 tbody");
    tableBody.innerHTML = "";

    mergedUsers.forEach(user => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${user.fullname}</td>
        <td>${user.email}</td>
        <td>${user.phone}</td>
        <td>${user.department}</td>
        <td><span class="badge ${getRiskBadge(user.passwordRisk)}">${user.passwordRisk}</span></td>
      `;

      tableBody.appendChild(row);
    });
  });
  

// Sample login logs
const recentLogs = [
  { name: "Navaneeth", time: "2025-07-01 09:15", status: "Success" },
  { name: "TestUser", time: "2025-07-01 08:45", status: "Failed" },
  { name: "Admin", time: "2025-06-30 18:20", status: "Success" },
  { name: "DevUser", time: "2025-06-30 14:10", status: "Warning" },
  { name: "Guest", time: "2025-06-30 11:00", status: "Success" }
];

const statusBadges = {
  Success: "bg-success",
  Failed: "bg-danger",
  Warning: "bg-warning"
};

document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById("recentLoginList");
  list.innerHTML = "";

  recentLogs.forEach(log => {
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-start";
    li.innerHTML = `
      <div>
        <div class="fw-bold">${log.name}</div>
        <small class="text-muted">${log.time}</small>
      </div>
      <span class="badge ${statusBadges[log.status]}">${log.status}</span>
    `;
    list.appendChild(li);
  });
});


// Sample Notification Data inject