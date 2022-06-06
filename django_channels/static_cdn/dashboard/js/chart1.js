function customer_monitoring_data_chat (returned_date_list, returned_value_list) {
    
    const ctx = document.getElementById('myChart').getContext("2d");

    let delayed;
    //gradient fill
    let gradient = ctx.createLinearGradient(0, 0 , 0, 400)
    gradient.addColorStop(0, "rgba(58, 123, 213, 1)");
    gradient.addColorStop(1, "rgba(0, 210, 255, 0.3)");
    const labels = returned_date_list;
    
    const data = {
        labels,
        datasets: [
            {
                data: returned_value_list,
                label: "Must Name Queries",
                fill: true,
                backgroundColor: gradient,
                //borderColor: "#fff",
                pointBackgroundColor: "#fff",
                tension: 0.1,
            },
        ],
    };

    const config = {
        type: 'line',
        //type: chartType,
        data: data,
        options: {
            radius: 4,
            hitRadius: 25,
            hoverRadius: 10,
            responsive: true,
            animation: {
                onComplete: () => {
                delayed = true;
                },
                delay: (context) => {
                let delay = 0;
                if (context.type === 'data' && context.mode === 'default' && !delayed) {
                   // delay = context.dataIndex * 300 + context.datasetIndex * 100;
                   delay = context.dataIndex * 100 + context.datasetIndex * 100;
                }
                return delay;
                },
            },
            scales: {
                x: {
                    min: 0,
                    // max: 6
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value){
                           // return '$' + value + 'm';
                           return value + 'kWh';
                        },
                    },
                },
            },
        },
    };

    // JS - Destroy exiting Chart Instance to reuse <canvas> element
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    let myChart = new Chart(ctx, config);

    // Scrolling feature
    function scroller(scroll, chart) {
        var myMaxLength = myChart.config.options.scales.x.max
        if (scroll.deltaY > 0) {
            console.log('myMaxLength', myMaxLength + 1)
            if (myChart.config.options.scales.x.max >= labels.length) {
                myChart.config.options.scales.x.min = labels.length - (myMaxLength + 1);
                myChart.config.options.scales.x.max = labels.length;
            } else {
                myChart.config.options.scales.x.min += 1;
                myChart.config.options.scales.x.max += 1;
            };

        } else if (scroll.deltaY < 0) {
            if (myChart.config.options.scales.x.min <= 0) {
                myChart.config.options.scales.x.min = 0;
                myChart.config.options.scales.x.max = 6;
            } else {
                myChart.config.options.scales.x.min -= 1;
                myChart.config.options.scales.x.max -= 1;
            };
        } else {
            // do nothing. Scroller not in use 
        };
        myChart.update();
    }
        // Event Listener for scrolling chart using wheel
        myChart.canvas.addEventListener('wheel', (e) => {
            //customer_monitoring_data_chat()
            scroller(e, myChart)
        });

};

function chartType(type) {
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    let my_returned_date_list = document.getElementById('my_date').value;
    let my_returned_value_list = document.getElementById('my_value').value;
    let returned_date_list = my_returned_date_list.split(',')
    let returned_value_list = my_returned_value_list.split(',')
    console.log(returned_date_list)
    console.log(returned_value_list)
    const ctx = document.getElementById('myChart').getContext("2d");
    const labels = returned_date_list;
    let delayed;
    //gradient fill
    let gradient = ctx.createLinearGradient(0, 0 , 0, 400)
    gradient.addColorStop(0, "rgba(58, 123, 213, 1)");
    gradient.addColorStop(1, "rgba(0, 210, 255, 0.3)");

    const data = {
        labels,
        datasets: [
            {
                data: returned_value_list,
                label: "Must Name Queries " + type,
                fill: true,
                backgroundColor: gradient,
                //borderColor: "#fff",
                pointBackgroundColor: "#fff",
                tension: 0.1,
            },
        ],
    };
    const config = {
        type: type,
        data: data,
        options: {
            radius: 4,
            hitRadius: 25,
            hoverRadius: 10,
            responsive: true,
            animation: {
                onComplete: () => {
                delayed = true;
                },
                delay: (context) => {
                let delay = 0;
                if (context.type === 'data' && context.mode === 'default' && !delayed) {
                    // delay = context.dataIndex * 300 + context.datasetIndex * 100;
                    delay = context.dataIndex * 100 + context.datasetIndex * 100;
                }
                return delay;
                },
            },
            scales: {
                x: {
                    min: 0,
                    //max: 6,
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value){
                            // return '$' + value + 'm';
                            return value + 'kWh';
                        },
                    },
                },
            },
        },
    };
    // JS - Destroy exiting Chart Instance to reuse <canvas> element
    
    let myChart = new Chart(ctx, config);
        // Scrolling feature
        function scroller(scroll, chart) {
            var myMaxLength = myChart.config.options.scales.x.max
            if (scroll.deltaY > 0) {
                console.log('myMaxLength', myMaxLength + 1)
                if (myChart.config.options.scales.x.max >= labels.length) {
                    myChart.config.options.scales.x.min = labels.length - (myMaxLength + 1);
                    myChart.config.options.scales.x.max = labels.length;
                } else {
                    myChart.config.options.scales.x.min += 1;
                    myChart.config.options.scales.x.max += 1;
                };
    
            } else if (scroll.deltaY < 0) {
                if (myChart.config.options.scales.x.min <= 0) {
                    myChart.config.options.scales.x.min = 0;
                    myChart.config.options.scales.x.max = 6;
                } else {
                    myChart.config.options.scales.x.min -= 1;
                    myChart.config.options.scales.x.max -= 1;
                };
            } else {
                // do nothing. Scroller not in use 
            };
            myChart.update();
        }
            // Event Listener for scrolling chart using wheel
            myChart.canvas.addEventListener('wheel', (e) => {
                //customer_monitoring_data_chat()
                scroller(e, myChart)
            });
    
    };


    function displayPoints() {
        let my_number = document.getElementById('numberPoints').value
        
        if (my_number == 'Display Points') {
            my_number = ''
        }
        let number = parseInt(my_number)
        let chartStatus = Chart.getChart("myChart"); // <canvas> id
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }
        let my_returned_date_list = document.getElementById('my_date').value;
        let my_returned_value_list = document.getElementById('my_value').value;
        let returned_date_list = my_returned_date_list.split(',')
        let returned_value_list = my_returned_value_list.split(',')

        const ctx = document.getElementById('myChart').getContext("2d");
        const labels = returned_date_list;
        let delayed;
        //gradient fill
        let gradient = ctx.createLinearGradient(0, 0 , 0, 400)
        gradient.addColorStop(0, "rgba(58, 123, 213, 1)");
        gradient.addColorStop(1, "rgba(0, 210, 255, 0.3)");
        type = 'line'
        const data = {
            labels,
            datasets: [
                {
                    data: returned_value_list,
                    label: "Must Name Queries " + type,
                    fill: true,
                    backgroundColor: gradient,
                    //borderColor: "#fff",
                    pointBackgroundColor: "#fff",
                    tension: 0.1,
                },
            ],
        };
        console.log(number)
        const config = {
            type: type,
            data: data,
            options: {
                radius: 4,
                hitRadius: 25,
                hoverRadius: 10,
                responsive: true,
                animation: {
                    onComplete: () => {
                    delayed = true;
                    },
                    delay: (context) => {
                    let delay = 0;
                    if (context.type === 'data' && context.mode === 'default' && !delayed) {
                        // delay = context.dataIndex * 300 + context.datasetIndex * 100;
                        delay = context.dataIndex * 100 + context.datasetIndex * 100;
                    }
                    return delay;
                    },
                },
                scales: {
                    x: {
                        min: 0,
                        max: number
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value){
                                // return '$' + value + 'm';
                                return value + 'kWh';
                            },
                        },
                    },
                },
            },
        };
        // JS - Destroy exiting Chart Instance to reuse <canvas> element
        
        let myChart = new Chart(ctx, config);
            // Scrolling feature
            function scroller(scroll, chart) {
                
                if (scroll.deltaY > 0) {
                    
                    if (myChart.config.options.scales.x.max >= labels.length) {
                        myChart.config.options.scales.x.min = labels.length - (number + 1);
                        myChart.config.options.scales.x.max = labels.length;
                    } else {
                        myChart.config.options.scales.x.min += 1;
                        myChart.config.options.scales.x.max += 1;
                    };
        
                } else if (scroll.deltaY < 0) {
                    if (myChart.config.options.scales.x.min <= 0) {
                        myChart.config.options.scales.x.min = 0;
                        myChart.config.options.scales.x.max = number;
                    } else {
                        myChart.config.options.scales.x.min -= 1;
                        myChart.config.options.scales.x.max -= 1;
                    };
                } else {
                    // do nothing. Scroller not in use 
                };
                myChart.update();
            }
                // Event Listener for scrolling chart using wheel
                myChart.canvas.addEventListener('wheel', (e) => {
                    //customer_monitoring_data_chat()
                    scroller(e, myChart)
                });
        
        };

function downloadChart(){
    const imageLink = document.createElement('a');
    const canvas = document.getElementById('myChart');
    imageLink.download = 'canvas.png'
    imageLink.href = canvas.toDataURL('image/png', 1);
    imageLink.click();

}
