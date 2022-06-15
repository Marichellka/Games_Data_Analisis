from pandas import DataFrame
from sklearn.neural_network import MLPRegressor


def build_mlp_regression(x_train : DataFrame, y_train : DataFrame) -> MLPRegressor:
    regression = build_mlp_regression().fit(x_train, y_train)
    return regression


def build_mlp_regression() -> MLPRegressor:
    return MLPRegressor()
