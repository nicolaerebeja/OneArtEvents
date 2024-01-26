// statistici generale : Start
countStatisticiGenerale(2024)

function extAnXstGen(element) {
    var anul = element.innerText;
    $('#statisticiGeneralePePeriaoada > span').text(anul)

    $('#evenimenteXan').text(0)
    $('#dansatoriXan').text(0)
    $('#venitXan').text(0)

    countStatisticiGenerale(anul)
}

function countStatisticiGenerale(anulSelectat) {
    fetch('/analytics/countStatisticiGenerale?year=' + anulSelectat)
        .then(response => response.json())
        .then(data => {

            console.log(data.dansatori)
            $('#evenimenteXan').text(data.evenimente)
            $('#dansatoriXan').text(data.dansatori)
            $('#venitXan').text(data.venit)

        })
        .catch(error => console.error('Error fetching data:', error));
}

// statistici generale : End


// Statistici pe Perioada : Start

countEventsMonthByYear(2024)

var chartCountEventsMonthUpdateChart
var chartCountEventsMonthUpdatePie
var chartCountEventsMonthUpdateLineChart

function extrageAnul(element) {
    var anul = element.innerText;
    $('#statisticiPePeriaoada > span').text(anul)

    chartCountEventsMonthUpdateChart.destroy();
    chartCountEventsMonthUpdatePie.destroy();
    chartCountEventsMonthUpdateLineChart.destroy();

    countEventsMonthByYear(anul)
}

function countEventsMonthByYear(anulSelectat) {
    fetch('/analytics/countEventsMonth?year=' + anulSelectat)
        .then(response => response.json())
        .then(data => {
            // Aici ai acces la date sub formă de obiect JSON
            countEventsMonthUpdateChart(data);
            countEventsMonthUpdatePie(data);

            const cumulativeData = {};
            let totalEvents = 0;

            Object.keys(data).forEach(month => {
                totalEvents += data[month];
                cumulativeData[month] = totalEvents;
            });

            // Actualizează graficul folosind datele cumulative
            countEventsMonthUpdateLineChart(cumulativeData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

var backgroundColors

function generateRandomColor() {
    var baseColor = 100; // Nuanța de roșu închis de pornire (0-255)
    var variation = 30; // Variația pentru a obține nuanțe diferite

    // Generare aleatoare a nuanței de roșu închis
    var red = baseColor + Math.floor(Math.random() * variation);
    var green = Math.floor(Math.random() * variation);
    var blue = Math.floor(Math.random() * variation);

    return `rgb(${red},${green},${blue})`;
}

var monthMapping = {
    1: 'ianuarie',
    2: 'februarie',
    3: 'martie',
    4: 'aprilie',
    5: 'mai',
    6: 'iunie',
    7: 'iulie',
    8: 'august',
    9: 'septembrie',
    10: 'octombrie',
    11: 'noiembrie',
    12: 'decembrie'
};


function countEventsMonthUpdateChart(data) {
    backgroundColors = Object.keys(data).map(function () {
        return generateRandomColor();
    });
    var ctx = document.getElementById('evenimenteXluna').getContext('2d');
    chartCountEventsMonthUpdateChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data).map(function (key) {
                return monthMapping[key];
            }),
            datasets: [{
                label: 'Număr evenimente pe lună',
                data: Object.values(data),  // Valorile vor fi înălțimile barelor
                backgroundColor: backgroundColors,
                borderColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false,
                }
            }
        },
    });
}

function countEventsMonthUpdatePie(data) {
    backgroundColors = Object.keys(data).map(function () {
        return generateRandomColor();
    });
    var ctx = document.getElementById('evenimenteXlunaPie').getContext('2d');

    chartCountEventsMonthUpdatePie = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data).map(function (key) {
                    return monthMapping[key];
                }),
                datasets: [{
                    label: 'Număr evenimente pe lună',
                    data: Object.values(data),
                    backgroundColor: backgroundColors,
                }]
            },
        }
    )
    ;
}

function countEventsMonthUpdateLineChart(data) {
    var ctx = document.getElementById('evenimenteTotale').getContext('2d');
    chartCountEventsMonthUpdateLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Număr total acumulativ de evenimente',
                data: Object.values(data),
                fill: false,
                borderColor: 'rgb(255,0,0)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });
}

// Statistici pe Perioada : End


fetch('/analytics/countEventsXDancers')
    .then(response => response.json())
    .then(data => {
        // Transformă datele în format potrivit pentru Chart.js
        const labels = Object.keys(data);
        const values = Object.values(data);

        // Sortează datele în ordine crescătoare
        const sortedIndices = values.map((value, index) => index).sort((a, b) => values[a] - values[b]);
        const sortedLabels = sortedIndices.map(index => labels[index]);
        const sortedValues = sortedIndices.map(index => values[index]);

        // Actualizează chart-ul
        updateHorizontalBarChart(sortedLabels, sortedValues);
    })
    .catch(error => console.error('Error fetching data:', error));

function updateHorizontalBarChart(labels, values) {
    var ctx = document.getElementById('eventsXDancers').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Număr de evenimente pe dansator',
                data: values,
                backgroundColor: 'rgba(141,15,15,0.6)',
                borderColor: 'rgb(213,3,3)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });
}


// Datele pentru pie chart
var data = {
    labels: ['Referal', 'Facebook', 'Direct', 'Organic'],
    datasets: [{
        data: [60, 15, 20, 12],
        backgroundColor: ['#344767', '#1a73e8', '#e91e63', '#344767'],
    }]
};

// Configurații pentru pie chart
var options = {
    responsive: true,
    plugins: {
        legend: {
            display: false
        },
        title: {
            display: false
        }
    },
    maintainAspectRatio: false,
    aspectRatio: 1,
};

// Obține contextul canvasului
// var ctx = document.getElementById('pie-chart').getContext('2d');
//
// // Creează pie chart
// var pieChart = new Chart(ctx, {
//     type: 'pie',
//     data: data,
//     options: options
// });

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});