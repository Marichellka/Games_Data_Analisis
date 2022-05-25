from pandas import DataFrame
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from scripts.helpers import split_dataframe


def test_regression(
    regression,
    x_test : DataFrame,
    y_test : DataFrame):
    predictions = regression.predict(x_test)
    mean_erorr_result = mean_squared_error(y_test, predictions)
    r2_result = r2_score(y_test, predictions)
    return mean_erorr_result, r2_result


def train_test_dataset_split(
    dataset : DataFrame,
    x_cols : list,
    y_cols : list,
    **kwargs):
    dataset_train, dataset_test = train_test_split(dataset, **kwargs)
    x_train, y_train = split_dataframe(dataset_train, x_cols, y_cols)
    x_test, y_test = split_dataframe(dataset_test, x_cols, y_cols)
    return x_train, y_train, x_test, y_test
