fetch('/data?chart_type=pace')
    .then(response => response.json())
    .then(chartData => {
        const ctx = document.getElementById('myChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: chartData.datasets.map(dataset => ({
                    ...dataset,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                }))
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                stacked: false,
                scales: {
                    x: {
                        type: 'category',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Week Start'
                        },
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Pace (min/km)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Pace graph'
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching chart data:', error));
