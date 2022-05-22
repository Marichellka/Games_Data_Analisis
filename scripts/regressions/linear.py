from pandas import DataFrame
from sklearn.linear_model import LinearRegression

def build_linear_regression(x_train : DataFrame, y_train : DataFrame):
    regression = LinearRegression().fit(x_train, y_train)
    return regression
