let state = "Massachusetts";
let county = "Suffolk";
let metric = "cases";

get_data(state, county, metric, true);

// Changing the state and metric
$(document).ready(function(){
    $('.state').click(function(){
        clear_county_form();
        state = this.id;
        get_counties(state);
        $('#state_button').text($(this).text());
    });

    $(document).on('click', '.county', function()
    {
        county = this.id;
        console.log(county);
        $('#county_button').text($(this).text());
        get_data(state, county, metric, true);
    });

    $('.metric').click(function () {
        metric = this.id;
        $('#metric_button').text($(this).text());
        if(county!==null){
            get_data(state, county, metric, false)
        }
    })
});



function populate_county_form(counties){
    $('#county_form').empty();
    for(let i = 0; i< counties.length;i++){
        $('#county_form').append('<li class = \"county\" id =\"' + counties[i]
            +'\"><a href=\"#\" class=\"dropdown-item\">'
            + counties[i] + '</a></li>');
    }
}

function clear_county_form(){
    $('#county_button').text("County");
    county = null;
}

function get_counties(state){
    let state_info = {'state': state};
    state_info = JSON.stringify(state_info);

    fetch('/get_all_counties',{
           headers: {
               'Content-Type': 'application/json',
                'Accept': 'application/json'
           },
            method: 'POST',
            body: state_info
        }).then(function (response){
            return response.json();
        }).then(function (json){
            console.log(json);
            populate_county_form(json['counties'])
        });
}

function get_data(state, county, metric, refetch_tweets) {
    let request_data = {'state': state, 'county': county, 'metric': metric};
    request_data = JSON.stringify(request_data);


    fetch('/get_by_county', {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method: 'POST',
        body: request_data
    }).then(function (response) {
        return response.json();
    }).then(function (json) {
        let new_datepoints = parse_datelist(json['time'], 10);
        createplot(new_datepoints, json['data'], county + ", " + state);
        forecast(json['data'], 10);
        if(refetch_tweets){
            get_tweets(state, county);
        }
    });
}

function forecast(data, number_days){
    let request_data = {'history': data, 'num_days': number_days};
    request_data = JSON.stringify(request_data);

    fetch('/get_forecast', {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method: 'POST',
        body: request_data
    }).then(function (response) {
        return response.json();
    }).then(function (json) {
        let forecast_plotting = [];
        for(let i = 0; i<data.length-1; i++){
            forecast_plotting.push(NaN);
        }
        forecast_plotting.push(data.slice(-1)[0]);
        forecast_plotting = forecast_plotting.concat(json['forecast']);
        console.log(forecast_plotting);
        add_forecast(forecast_plotting);
    });

}

function get_tweets(state, county){
    let request_data = {'state': state, 'county': county};
    request_data = JSON.stringify(request_data);

    $('.sentiment_spin').show();

    fetch('/twitter_sentiment', {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method: 'POST',
        body: request_data
    }).then(function (response) {
        return response.json();
    }).then(function (json) {
        create_radial_plot([json['positives'], json['negatives']]);
        populate_top_phrases(json['top_phrases']);
    });

}

function populate_top_phrases(phrases){
    $('#phrases').empty();
    $('.sentiment_spin').hide();
    for(let i = 0; i<phrases.length;i++){
        $('#phrases').append('<li class = \"list-group-item\">'
            +phrases[i]+'</li>');
    }
}