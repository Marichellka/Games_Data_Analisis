from pandas import DataFrame
from sklearn.linear_model import LinearRegression


def build_linear_regression(x_train : DataFrame, y_train : DataFrame) -> LinearRegression:
    regression = LinearRegression().fit(x_train, y_train)
    return regression


def build_linear_regression() -> LinearRegression:
    return LinearRegression()
