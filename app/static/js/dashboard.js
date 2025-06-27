// Bar Chart
const barCtx = document.getElementById('barChart').getContext('2d');
new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['Length OK', 'Uppercase', 'Lowercase', 'Digit', 'Special', 'Common', 'Personal Info'],
        datasets: [{
            label: 'Failures',
            data: [2, 3, 0, 3, 2, 1, 1],
            backgroundColor: '#ff6384'
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { color: "#fff" },
                grid: { color: '#555' }
            },
            x: {
                ticks: { color: "#fff" },
                grid: { color: '#555' }
            }
        }
    }
});

// Pie Chart
const heatmapCtx = document.getElementById('heatmapChart').getContext('2d');
new Chart(heatmapCtx, {
    type: 'pie',
    data: {
        labels: ['Sales', 'Marketing', 'HR', 'Dev', 'Staff'],
        datasets: [{
            data: [25, 15, 10, 30, 20],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#66ff99', '#c266ff']
        }]
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});
