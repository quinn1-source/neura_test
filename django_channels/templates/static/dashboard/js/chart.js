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
                label: "Minecrafty Sales",
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
                y: {
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
    const myChart = new Chart(ctx, config);
}