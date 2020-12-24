# Covid Tracks

This application was used for plotting, forecasting COVID19 cases and deaths at the county level. The Twitter API was used to obtain tweets from the selected counties and sentiment analysis and keyword extraction were performed to find the average sentiment of users within the chosen area.

## Running the application
1) Clone the repository and enter the repository.
```bash
git clone https://github.com/plyalyut/Covid-Forecasting-And-Sentiment
cd Covid-Forecasting-And-Sentiment
```
2) Create a new YAML file titled config.yaml at the root of the repo that contains your Twitter API keys. The contents should be formated as such:
```YAML
consumer_key: INSERT_KEY_HERE
consumer_secret: INSERT_SECRET_KEY_HERE
```

3) Build the docker image 
```bash
docker build -t COVID_TRACKER .
```
4) Deploy your docker container
```bash
docker run -d -p 5000:5000 COVID_TRACKER 
```





