document.addEventListener("DOMContentLoaded", function () {
    // Department-wise Password Issues - Stacked Bar
    const departmentBarCtx = document.getElementById("departmentBarChart").getContext("2d");
    new Chart(departmentBarCtx, {
      type: 'bar',
      data: {
        labels: ["HR", "Sales", "Tech", "Support", "Finance"],
        datasets: [
          {
            label: "Weak Passwords",
            data: [15, 25, 30, 10, 20],
            backgroundColor: "#f87171"
          },
          {
            label: "Common Passwords",
            data: [10, 18, 12, 6, 9],
            backgroundColor: "#fbbf24"
          },
          {
            label: "Personal Info Used",
            data: [7, 12, 15, 5, 11],
            backgroundColor: "#6366f1"
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: false
          },
          animation: {
            duration: 1000,
            easing: 'easeOutQuart'
          }
        },
        scales: {
          x: { stacked: true },
          y: { stacked: true, beginAtZero: true }
        }
      }
    });

    // Password Strength Pie Chart
    const pieCtx = document.getElementById("strengthPieChart").getContext("2d");
    new Chart(pieCtx, {
      type: 'doughnut',
      data: {
        labels: ["Strong", "Weak", "Common"],
        datasets: [{
          data: [60, 25, 15],
          backgroundColor: ["#34d399", "#f87171", "#fbbf24"],
        }]
      },
      options: {
        responsive: true,
        cutout: '70%',
        plugins: {
          legend: { position: 'bottom' },
          animation: {
            animateScale: true,
            animateRotate: true
          }
        }
      }
    });

    // Login Activity Over Time - Line Chart
    const loginCtx = document.getElementById("loginLineChart").getContext("2d");
    new Chart(loginCtx, {
      type: 'line',
      data: {
        labels: ["June 20", "June 21", "June 22", "June 23", "June 24", "June 25", "June 26"],
        datasets: [
          {
            label: "Success Logins",
            data: [15, 20, 18, 25, 22, 27, 30],
            borderColor: "#10b981",
            backgroundColor: "#10b98133",
            fill: true,
            tension: 0.4
          },
          {
            label: "Failed Logins",
            data: [5, 8, 6, 10, 7, 97, 11],
            borderColor: "#ef4444",
            backgroundColor: "#ef444433",
            fill: true,
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: false
          },
          animation: {
            duration: 1200,
            easing: 'easeOutExpo'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 5
            }
          }
        }
      }
    });
  });
