function parse_datelist(timedata, num_future_datapoints){
    /**
     * Parses the time and converts it tomthe appropriate slot
     * @param timedata
     */
    let new_time_data = [];
    for(let i = 0; i<timedata.length;i++) {
        let parsed_date = parse_date(timedata[i]);
        new_time_data.push(convert_to_string(parsed_date));
    }
    let future_dates = generate_n_next_dates(timedata, 1, num_future_datapoints);
    for(let i = 0; i<future_dates.length;i++){
        new_time_data.push(convert_to_string(future_dates[i]))
    }
    return new_time_data;
}

function parse_date(time){
    /**
     * Parses datetime
     * @param time: time data
     */
    let temp_string = String(time);
    let year = temp_string.substring(0,4);
    let month = temp_string.substring(5,7);
    let day = temp_string.substring(8,10);
    return [year, month, day];
}

function generate_n_next_dates(date_data, delta, number_new_datapoints){
    /**
     * Generates the next n days in the list.
     */
    let last_date = date_data.slice(-1)[0];
    last_date = this.parse_date(last_date);
    last_date = new Date(parseInt(last_date[0]), parseInt(last_date[1])-1, parseInt(last_date[2]));
    let new_dates = [];
    for(let i = 0; i<number_new_datapoints; i++){
        last_date.setDate(last_date.getDate() + delta);
        new_dates.push([last_date.getFullYear(), last_date.getMonth()+1, last_date.getDate()])
    }
    return new_dates;
}

function convert_to_string(datapoint) {
    /**
     * @param datapoint: Datapoint with three entries [year, month, day]
     */

    return datapoint[1] + "-" + datapoint[2] + "-" + datapoint[0]
}
