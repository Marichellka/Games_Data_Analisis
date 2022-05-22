from scripts.cleansing import read_and_cleanse
from scripts.config import DATA_PATH_SALES
from scripts.regressions.helpers import test_regression, train_test_dataset_split
from scripts.regressions.linear import build_linear_regression

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

# TODO: Marichellka please add non-numeric columns to x_cols. 
x_cols = ["Year"]
y_cols = ["Global_Sales"]

x_train, y_train, x_test, y_test = train_test_dataset_split(dataset, x_cols, y_cols)

linear_regression = build_linear_regression(x_train, y_train)
linear_result_mean, linear_result_r2 = test_regression(linear_regression, x_test, y_test)
print(linear_result_mean, linear_result_r2)
