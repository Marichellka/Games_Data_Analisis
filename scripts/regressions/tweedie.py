from pandas import DataFrame
from sklearn.linear_model import TweedieRegressor


def build_tweedie_regression(x_train : DataFrame, y_train : DataFrame) -> TweedieRegressor:
    regression = build_tweedie_regression().fit(x_train, y_train)
    return regression


def build_tweedie_regression() -> TweedieRegressor:
    return TweedieRegressor()
