function getChartColorsArray(chartId) {
    if (document.getElementById(chartId) !== null) {
        var colors = document.getElementById(chartId).getAttribute("data-colors");
        if (colors) {
            colors = JSON.parse(colors);
            return colors.map(function (value) {
                var newValue = value.replace(" ", "");
                if (newValue.indexOf(",") === -1) {
                    var color = getComputedStyle(document.documentElement).getPropertyValue(
                        newValue
                    );
                    if (color) return color;
                    else return newValue;
                } else {
                    var val = value.split(",");
                    if (val.length == 2) {
                        var rgbaColor = getComputedStyle(
                            document.documentElement
                        ).getPropertyValue(val[0]);
                        rgbaColor = "rgba(" + rgbaColor + "," + val[1] + ")";
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
        } else {
            console.warn('data-colors Attribute not found on:', chartId);
        }
    }
}
document.addEventListener('DOMContentLoaded', function () {
    var areaChartColors = getChartColorsArray("area-chart");

    fetch('/save-selections/')
        .then(response => response.json())
        .then(data => {
            var monthlyUserCounts = data.monthly_user_counts;
            console.log(monthlyUserCounts)
            var monthlyVisitorCounts = data.monthly_visitor_counts
            var options = {
                series: [{
                    name: 'Users',
                    data: monthlyUserCounts
                },
                    // {
                    //     name: 'Visitor',
                    //     data: monthlyVisitorCounts
                    // }
                ],
                chart: {
                    height: 350,
                    type: 'area',
                    toolbar: {
                        show: false
                    },
                },
                colors: areaChartColors,
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: 'smooth',
                    width: 2,
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        inverseColors: false,
                        opacityFrom: 0.45,
                        opacityTo: 0.05,
                        stops: [20, 100, 100, 100]
                    },
                },
                xaxis: {
                    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                },

                markers: {
                    size: 3,
                    strokeWidth: 3,

                    hover: {
                        size: 4,
                        sizeOffset: 2
                    }
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'right',
                },
            };

            var chart = new ApexCharts(document.querySelector("#area-chart"), options);
            chart.render();
        })
        .catch(error => console.error('Error fetching data:', error));
});
// var areaChartColors = getChartColorsArray("area-chart");
// if (areaChartColors) {
//     var options = {
//         series: [{
//             name: 'Users',
//             data: [18, 21, 45, 36, 65, 47, 51, 32, 40, 28, 31, 26]
//         },
//         //     {
//         //     name: 'Previous',
//         //     data: [30, 11, 22, 18, 32, 23, 58, 45, 30, 36, 15, 34]
//         // }
//         ],
//         chart: {
//             height: 350,
//             type: 'area',
//             toolbar: {
//                 show: false
//             },
//         },
//         colors: areaChartColors,
//         dataLabels: {
//             enabled: false
//         },
//         stroke: {
//             curve: 'smooth',
//             width: 2,
//         },
//         fill: {
//             type: 'gradient',
//             gradient: {
//                 shadeIntensity: 1,
//                 inverseColors: false,
//                 opacityFrom: 0.45,
//                 opacityTo: 0.05,
//                 stops: [20, 100, 100, 100]
//             },
//         },
//         xaxis: {
//             categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
//         },
//
//         markers: {
//             size: 3,
//             strokeWidth: 3,
//
//             hover: {
//                 size: 4,
//                 sizeOffset: 2
//             }
//         },
//         legend: {
//             position: 'top',
//             horizontalAlign: 'right',
//         },
//     };
//
//     var chart = new ApexCharts(document.querySelector("#area-chart"), options);
//     chart.render();
// }