import pandas as pd
from datetime import date

class DataGetter:
    def __init__(self):
        """
        Initializes the data getter and fetches the data.
        """
        self.data = None
        self.url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        self.county_mappings = {}
        self.historical_data = {}

        self.get_data()

    def get_data(self):
        """
        Gets the data from a url and stores it in the appropriate information.
        :return: the data
        """

        # Reads in the data into a dataframe.
        self.data = pd.read_csv(self.url)
        self.data['date'] = pd.to_datetime(self.data['date'], format='%Y-%m-%d').dt.strftime(
            '%Y-%m-%d')  # Converts to date
        self.data['cases'] = self.data['cases'].astype(int)
        self.data = self.data.fillna(method='ffill')
        self.data['deaths'] = self.data['deaths'].astype(int)

        with open("update_date.txt", "w") as f:
            f.write(date.today().strftime('%m/%d/%Y'))

        return self.data

    def check_update(self):
        with open("update_date.txt", "r") as f:
            for line in f:
                if line != date.today().strftime('%m/%d/%Y'):
                    self.get_data()

    def get_all_counties_in_state(self, state):
        """
        Gets all the counties available in the state
        :return: list of all the available counties
        """

        self.check_update()

        if self.data is not None:
            counties = self.data[self.data['state'] == state]['county'].unique()
            return sorted(list(counties))
        else:
            return []

    def get_all_county_data(self, county, state):
        """
        Gets all the county data by the county and state
        :param county: county (capitalized)
        :param state:
        :return: Dataframe containing all the data from that county
        """
        data = self.data[(self.data['state'] == state) & (self.data['county'] == county)]
        return data

    def get_historical_county_cases(self, county, state, n_latest=None):
        """
        Gets the number of cases.
        :return: dataframe with the cases
        """

        cases = self.get_all_county_data(county, state)[['date', 'cases']]

        if n_latest:
            return cases.tail(n_latest)
        else:
            return cases

    def get_historical_county_deaths(self, county, state, n_latest=None):
        """
        Gets the number of deaths.
        :param county: county String
        :param state: state String
        :return: dataframe with the cases
        """

        deaths = self.get_all_county_data(county, state)[['date', 'deaths']]

        if n_latest:
            return deaths.tail(n_latest)
        else:
            return deaths

    def compute_daily_new_cases(self, county, state, n_latest):
        """
        Gets the number of new cases in an area.
        :param county: county String
        :param state: state String
        :param n_latest: number of entries to include
        :return: dataframe with the new cases
        """
        cases = self.get_historical_county_cases(county, state, n_latest)
        cases['cases'] = cases['cases'].diff().fillna(0)

        return cases

    def compute_daily_new_deaths(self, county, state, n_latest):
        """
         Gets the number of new deaths in an area.
        :param county: county String
        :param state: state String
        :param n_latest: number of entries to include
        :return: dataframe with the new cases
        :return: Dataframe with new deaths in an area
        """

        deaths = self.get_historical_county_deaths(county, state, n_latest)
        deaths['deaths'] = deaths['deaths'].diff().fillna(0)

        return deaths
