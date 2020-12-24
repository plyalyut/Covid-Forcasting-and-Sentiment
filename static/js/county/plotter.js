var chart;

function createplot(labels, data, title){
    cleardata();
    let ctx = document.getElementById('covid_plot').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels ,
            datasets: [{
                label: title,
                data: data
            },
                {
                    label: 'Forecast',
                    data: [],
                    borderDash: [10,5],
                    borderColor: "#666CFF",
                }
            ]
        }
    });
}



function add_forecast(data){
    if(chart != null){
        chart.data.datasets[1].data = data;
        chart.update();
    }
}

function cleardata(){
    if (chart != null){
        chart.destroy();
    }
}


