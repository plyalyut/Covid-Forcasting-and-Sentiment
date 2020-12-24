var chart2;

function create_radial_plot(data){
    clear_radial_data();
    console.log(data);
    if (data[0] === 0 && data[1] === 0){
        plot_null()
    }
    else{
        let ctx2 = document.getElementById('sentiment').getContext('2d');
        chart2 = new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative'],
                datasets: [{
                    data: data,
                    backgroundColor: ["#60d394","#ee6055"]
                }]
            }
        });
    }

    chart.update();
}

function clear_radial_data(){
    if (chart2 != null){
        chart2.destroy();
    }
}

function plot_null(){
    let ctx2 = document.getElementById('sentiment').getContext('2d');
    chart2 = new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: ['No Data'],
            datasets: [{
                data: [1],
                backgroundColor: ["#DDDDDD",]
            }]
        }
    });
}