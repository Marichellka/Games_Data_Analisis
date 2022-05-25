from pandas import DataFrame
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from scripts.helpers import split_dataframe
from scripts.regressions.linear import build_linear_regression
from scripts.regressions.polynomial import build_polynomial_regression


def test_regression(
    regression,
    x_test : DataFrame,
    y_test : DataFrame):
    predictions = regression.predict(x_test)
    mean_erorr_result = mean_squared_error(y_test, predictions)
    r2_result = r2_score(y_test, predictions)
    return [mean_erorr_result, r2_result]


def test_regressions(
    regressions : list,
    x_test : DataFrame,
    y_test : DataFrame):
    for regression in regressions:
        yield test_regression(regression, x_test, y_test)


def get_regressions(
    x_train : DataFrame,
    y_train : DataFrame):
    yield build_linear_regression(x_train, y_train)
    yield build_polynomial_regression(x_train, y_train, 2)
    yield build_polynomial_regression(x_train, y_train, 3)
    yield build_polynomial_regression(x_train, y_train, 4)
    yield build_polynomial_regression(x_train, y_train, 5)


def train_test_dataset_split(
    dataset : DataFrame,
    x_cols : list,
    y_cols : list,
    **kwargs):
    dataset_train, dataset_test = train_test_split(dataset, **kwargs)
    x_train, y_train = split_dataframe(dataset_train, x_cols, y_cols)
    x_test, y_test = split_dataframe(dataset_test, x_cols, y_cols)
    return x_train, y_train, x_test, y_test


def get_regression_model(
    dataset : DataFrame,
    x_cols : list,
    y_cols : list,
    **kwargs):
    x_train, y_train, x_test, y_test = \
        train_test_dataset_split(dataset, x_cols, y_cols, **kwargs)
    regressions = list(get_regressions(x_train, y_train))
    regressions_tests = list(test_regressions(regressions, x_test, y_test))
    beneficial_funcs = [
        lambda x: x, # mean squared error
        lambda x: [value + abs(min(x)) for value in x] # r2_score
    ]
    return get_best_regression(regressions, regressions_tests, beneficial_funcs)


# beneficial_funcs is a list of functions used to convert corresponding values into beneficial ones.
# it is expected that the return value will be >= 0.
def get_best_regression(regressions : list, regressions_tests : list, beneficial_funcs : list):
    beneficial_criterions_lists = \
        [beneficial_funcs[idx](test_values) \
            for idx, test_values in enumerate(list(map(list, zip(*regressions_tests))))]
    max_criterions_list = \
        [max(criterions) \
            for criterions in beneficial_criterions_lists]
    regressions_scores = \
        [sum([value / max_criterions_list[idx] for idx, value in enumerate(test)]) \
            for test in regressions_tests]
    # worst == 0, best == number of criterions in regressions_tests
    max_score = max(regressions_scores)
    return regressions[regressions_scores.index(max_score)], max_score
