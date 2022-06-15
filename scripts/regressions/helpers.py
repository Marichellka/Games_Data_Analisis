from typing import Iterator, Tuple
from pandas import DataFrame
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from scripts.helpers import split_dataframe
from scripts.regressions.bayesian_ridge import build_bayesian_ridge_regression
from scripts.regressions.gradient_boosting import build_gradient_boosting_regression
from scripts.regressions.linear import build_linear_regression
from scripts.regressions.mlp import build_mlp_regression
from scripts.regressions.polynomial import build_polynomial_regression
from scripts.regressions.random_forest import build_random_forest_regression
from scripts.regressions.tweedie import build_tweedie_regression
from scripts.regressions.poisson import build_poisson_regression
from scripts.utils.dataset_scaler import DatasetScaler


def test_regression(
    regression,
    x_test : DataFrame,
    y_test : DataFrame) -> list:
    predictions = regression.predict(x_test)
    mean_erorr_result = mean_squared_error(y_test, predictions)
    r2_result = r2_score(y_test, predictions)
    return [mean_erorr_result, r2_result]


def test_regressions(
    regressions : list,
    x_test : DataFrame,
    y_test : DataFrame) -> Iterator:
    for regression in regressions:
        yield test_regression(regression, x_test, y_test)


def get_regressions(
    x_train : DataFrame,
    y_train : DataFrame) -> Iterator:
    yield build_linear_regression(x_train, y_train)
    yield build_polynomial_regression(x_train, y_train, 2)
    yield build_polynomial_regression(x_train, y_train, 3)
    yield build_polynomial_regression(x_train, y_train, 4)
    yield build_bayesian_ridge_regression(x_train, y_train)
    yield build_gradient_boosting_regression(x_train, y_train)
    yield build_tweedie_regression(x_train, y_train)
    yield build_poisson_regression(x_train, y_train)
    yield build_random_forest_regression(x_train, y_train)
    yield build_mlp_regression(x_train, y_train)


def get_regressions() -> Iterator:
    yield build_linear_regression()
    yield build_polynomial_regression(2)
    yield build_polynomial_regression(3)
    yield build_polynomial_regression(4)
    yield build_bayesian_ridge_regression()
    yield build_gradient_boosting_regression()
    yield build_tweedie_regression()
    yield build_poisson_regression()
    yield build_random_forest_regression()
    yield build_mlp_regression()


def train_test_dataset_split(
    dataset : DataFrame,
    x_cols : list,
    y_cols : list,
    **kwargs) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    dataset_train, dataset_test = train_test_split(dataset, **kwargs)
    x_train, y_train = split_dataframe(dataset_train, x_cols, y_cols)
    x_test, y_test = split_dataframe(dataset_test, x_cols, y_cols)
    return x_train, y_train, x_test, y_test


def predict_unscaled(model, x : dict, scaler : DatasetScaler):
    x_scaled = [scaler.get_scaled_value(value, key) for (key, value) in x.items()]
    return model.predict([x_scaled])
