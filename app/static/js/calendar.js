const activityData = [
    { date: "2024-11-01", v: 5.0 },
    { date: "2024-11-02", v: 10.2 },
    { date: "2024-11-03", v: 7.3 },
    { date: "2024-11-04", v: 6.5 },
    { date: "2024-11-05", v: 8.0 },
    { date: "2024-11-06", v: 12.4 },
    { date: "2024-11-07", v: 5.0 },
    { date: "2024-11-08", v: 10.2 },
    { date: "2024-11-12", v: 7.3 },
    { date: "2024-11-15", v: 6.5 },
    { date: "2024-11-20", v: 8.0 },
    { date: "2024-11-25", v: 12.4 },
];

function getStartOfWeek(date) {
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    const startOfWeek = new Date(date.setDate(diff));
    startOfWeek.setHours(0, 0, 0, 0);
    return startOfWeek;
}

const matrixData = activityData.map(entry => {
    const date = new Date(entry.date);
    const startOfWeek = getStartOfWeek(new Date(entry.date));
    return {
        x: startOfWeek.getTime(),
        y: date.getDay(),
        v: entry.v,
        fullDate: entry.date,
    };
});
console.log(matrixData);

fetch('/data?chart_type=calendar')
    .then(response => response.json())
    .then(chartData => {
        console.log("calendar data:", chartData )
        const ctx = document.getElementById('myChart')?.getContext('2d');
        if (!ctx) {
            console.error("calendarChart canvas element not found.");
            return;
        }

        const weeksWithData = [...new Set(chartData.datasets.map(dataPoint => dataPoint.y))];

        chart = new Chart(ctx, {
            type: 'matrix',
            data: {
                datasets: [{
                    label: 'Activity Distance',
                    data: chartData.datasets,
                    backgroundColor({ raw }) {
                        const baseColor = 'rgba(49, 191, 250';
                        const alpha = Math.max(0.05 + (raw.v / 18), 0.1);
                        return `${baseColor}, ${alpha})`;
                    },
                    borderWidth: 1,
                    width: ({chart}) => (chart.chartArea || {}).width / (chart.scales.x.ticks.length + 1) - 7,
                    height: ({chart}) =>(chart.chartArea || {}).height / 7 - 3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'week',
                            displayFormats: {
                                week: 'MMM dd'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Start of Week'
                        },
                        position: 'top',
                        offset: true,
                        ticks: {
                            maxRotation: 0,
                            autoSkip: true,
                            padding: 1
                        },
                        grid: {
                            display: false,
                            drawBorder: false,
                        }
                    },
                    y: {
                        type: 'category',
                        labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                        position: 'left',
                        offset: true,
                        ticks: {
                            callback: function(value, index) {
                                return this.chart.options.scales.y.labels[index];
                            }
                        },
                        grid: {
                            display: false,
                            drawBorder: false,
                            tickLength: 0,
                        },
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: ctx => {
                                const { fullDate } = ctx[0].raw;
                                const date = new Date(fullDate);
                                const monthDay = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                                return `Date: ${monthDay}`;
                            },
                            label: ctx => `Distance: ${ctx.raw.v} km`
                        }
                    },
                    title: {
                        display: true,
                        text: 'Strava Calendar'
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching chart data:', error));
