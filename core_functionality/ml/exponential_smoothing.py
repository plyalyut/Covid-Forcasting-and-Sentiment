import numpy as np
import pandas as pd

from darts import TimeSeries
from darts.models import ExponentialSmoothing


def run_regression(data, num_new_datapoints):
    """
    Runs the regression model and
    :param data:
    :param num_new_datapoints:
    :return:
    """
    gpr = ExponentialSmoothing()
    data = np.array(data).reshape(-1, 1)
    series = TimeSeries.from_times_and_values(pd.DatetimeIndex(list(range(len(data)))), data)
    gpr.fit(series)
    return gpr.predict(num_new_datapoints).values().flatten().tolist()
