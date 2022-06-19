from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor


def build_random_forest_regression(x_train : DataFrame, y_train : DataFrame) -> RandomForestRegressor:
    regression = build_random_forest_regression().fit(x_train, y_train)
    return regression


def build_random_forest_regression() -> RandomForestRegressor:
    return RandomForestRegressor()
