# Covid-Forecasting-And-Sentiment

This application was used for plotting, forecasting COVID19 cases and deaths at the county level. The Twitter API was used to obtain tweets from the selected counties and sentiment analysis and keyword extraction were performed to find the average sentiment of users within the chosen area.

## Running the application
1) Clone the repository.
```
git clone https://github.com/plyalyut/Covid-Forecasting-And-Sentiment
```
2) Build the docker image 
```
docker build -t COVID_TRACKER
```
3) Deploy your docker container
```
docker run -d -p 5000:5000 COVID_TRACKER 
```





