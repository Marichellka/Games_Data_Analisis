from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def build_polynomial_regression(x_train : DataFrame, y_train : DataFrame):
    regression = make_pipeline(PolynomialFeatures(degree=4), LinearRegression()).fit(x_train, y_train)
    return regression
