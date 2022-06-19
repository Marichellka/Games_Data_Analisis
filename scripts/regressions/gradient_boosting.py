from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor


def build_gradient_boosting_regression(x_train : DataFrame, y_train : DataFrame) -> GradientBoostingRegressor:
    regression = build_gradient_boosting_regression().fit(x_train, y_train)
    return regression


def build_gradient_boosting_regression() -> GradientBoostingRegressor:
    return GradientBoostingRegressor()
