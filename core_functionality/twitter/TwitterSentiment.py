import yaml
import geocoder
import tweepy


class TwitterClient:

    def __init__(self):
        """
        Sets up the authentication and api connection
        """
        yaml = self.__process_yaml()
        self.api = self.__set_up_client(yaml)

    def __process_yaml(self):
        """
        Processes the YAML file containing the credentials.
        :return: Dictionary object with credentials
        """
        with open("config.yaml") as file:
            return yaml.safe_load(file)

    def __set_up_client(self, yaml):
        """
        Extracts the API key and API secret and sets up connection to Twitter.
        :param yaml: Loaded in dictionary.
        :return: API connection
        """
        auth = tweepy.AppAuthHandler(yaml['consumer_key'], yaml['consumer_secret'])
        return tweepy.API(auth)

    def get_latitude_longitude_via_county_state(self, county, state):
        """
        Gets the latitude and longitude location from a county or state.
        :param county: County of the location
        :param state: state of the location
        :return: latitude and longitude coordinates tuple
        """
        g = geocoder.arcgis(county + ',' + state)
        return g.latlng

    def get_latitude_longitude_string(self, county, state, radius=10):
        """
        Returns the latitude and longitude string representation.
        :param county: County (string)
        :param state: State (string)
        :param radius: number of radius outside of exact geographical location
        :return: String of search area
        """
        latlng = self.get_latitude_longitude_via_county_state(county, state)
        return "{},{},{}km".format(latlng[0], latlng[1], radius)

    def search_covid_tweets_latitude_longitude(self, county, state):
        """
        Fetches the Tweets in a given county and state (limit 20) matching on Covid,
        Covid19, or coronavirus. Filtering retweets and maintaining the english language
        :param county:
        :param state:
        :return: Text representation of the tweets
        """
        geographical_location = self.get_latitude_longitude_string(county, state)
        possible_q = "covid OR covid19 OR coronavirus -filter:retweets"

        text_information = []

        for tweet in tweepy.Cursor(self.api.search, q=possible_q, count=20, geocode=geographical_location,
                                   lang='en').items(20):
            text_information.append(tweet.text)

        return text_information
