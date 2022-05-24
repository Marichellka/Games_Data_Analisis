import matplotlib.pyplot as plt
from pandas import DataFrame


def plot_timeline(
    dataset : DataFrame,
    date_column : str,
    value_column : str,
    label : str = "",
    windows : list = []):
    series = dataset.sort_values([date_column]).groupby(date_column)[value_column].sum()
    rolling_means = [(series.rolling(window=n).mean(), n) for n in windows]
    for rolling_mean, window in rolling_means:
        plt.plot(rolling_mean, label=f"Rolling mean trend, n = {window}")
    plt.plot(series, label=label)
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()
