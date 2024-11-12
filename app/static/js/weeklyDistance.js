// chart.js
fetch('/data')
    .then(response => response.json())
    .then(chartData => {
        console.log("Chart Data Structure:", chartData);
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: chartData.datasets
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Start of Week'
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Distance (km)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: function(tooltipItem) {
                                const activityDate = tooltipItem[0].raw.date;
                                return activityDate;
                            },
                            label: function(tooltipItem) {
                                const distance = tooltipItem.raw;
                                return ' ' + distance + ' km';
                            }
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching chart data:', error));
