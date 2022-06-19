from pandas import DataFrame
from sklearn.linear_model import PoissonRegressor


def build_poisson_regression(x_train : DataFrame, y_train : DataFrame) -> PoissonRegressor:
    regression = build_poisson_regression().fit(x_train, y_train)
    return regression


def build_poisson_regression() -> PoissonRegressor:
    return PoissonRegressor()
