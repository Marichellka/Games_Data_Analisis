from numpy import ravel
from pandas import DataFrame
from sklearn.linear_model import BayesianRidge


def build_bayesian_ridge_regression(x_train : DataFrame, y_train : DataFrame) -> BayesianRidge:
    regression = build_bayesian_ridge_regression().fit(x_train, ravel(y_train))
    return regression


def build_bayesian_ridge_regression() -> BayesianRidge:
    return BayesianRidge()
