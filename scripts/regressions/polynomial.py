from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def build_polynomial_regression(x_train : DataFrame, y_train : DataFrame, degree : int) -> Pipeline:
    regression = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression()).fit(x_train, y_train)
    return regression


def build_polynomial_regression(degree : int) -> Pipeline:
    regression = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
    return regression
