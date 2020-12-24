from flask import Flask, jsonify, request, render_template
import core_functionality.ml.exponential_smoothing as forecast
import core_functionality.data.DataGetter as DataGetter
import core_functionality.twitter.TwitterSentiment as Twitter
from core_functionality.ml.sentiment_analysis import SentimentAnalysis
from core_functionality.ml.keyword_extraction import KeywordExtractor

app = Flask(__name__)

datagetter = DataGetter.DataGetter()
twitter_fetcher = Twitter.TwitterClient()
sentiment_analysis = SentimentAnalysis()
keyword_extraction = KeywordExtractor()

@app.route('/get_forecast', methods=['POST'])
def forecast_next_datapoints():
    """
    Runs the endpoint to generate forecasts based off of previous data.
    :return:
    """

    if request.method == 'POST':
        historical_data = request.get_json()
        fitted_params = forecast.run_regression(historical_data['history'], historical_data['num_days'])
        message = {'forecast': fitted_params}
        return jsonify(message)

@app.route('/get_all_counties', methods=['POST'])
def get_counties():
    state_information = request.get_json()
    counties = datagetter.get_all_counties_in_state(state_information['state'])
    message = {'state': state_information['state'], 'counties': counties}
    return jsonify(message)


@app.route('/get_by_county', methods=['POST'])
def get_covid_by_county():
    request_json = request.get_json()

    message = {}

    if request_json['metric'] == 'cases':
        cases_df = datagetter.get_historical_county_cases(request_json['county'], request_json['state'], 30)
        message['time'] = cases_df['date'].to_list()
        message['data'] = cases_df['cases'].to_list()
        return jsonify(message)
    elif request_json['metric'] == 'deaths':
        deaths_df = datagetter.get_historical_county_deaths(request_json['county'], request_json['state'], 30)
        message['time'] = deaths_df['date'].to_list()
        message['data'] = deaths_df['deaths'].to_list()
        return jsonify(message)
    elif request_json['metric'] == 'new_cases':
        cases_df = datagetter.compute_daily_new_cases(request_json['county'], request_json['state'], 30)
        message['time'] = cases_df['date'].to_list()
        message['data'] = cases_df['cases'].to_list()
        return jsonify(message)
    elif request_json['metric'] == 'new_deaths':
        deaths_df = datagetter.compute_daily_new_deaths(request_json['county'], request_json['state'], 30)
        message['time'] = deaths_df['date'].to_list()
        message['data'] = deaths_df['deaths'].to_list()
        return jsonify(message)
    else:
        return jsonify(message)

@app.route('/twitter_sentiment', methods=['POST'])
def get_twitter_info():
    request_json = request.get_json()

    tweets = twitter_fetcher.search_covid_tweets_latitude_longitude(request_json['county'], request_json['state'])
    positive, negatives = sentiment_analysis.calculate_overall_sentiment(tweets)
    message = {'positives': positive, 'negatives': negatives}
    extracted = keyword_extraction.extract_keywords(tweets)
    message['top_phrases'] = extracted
    return jsonify(message)

@app.route('/home')
def home_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
