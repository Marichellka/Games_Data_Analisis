from scripts.cleansing import read_and_cleanse, stack_dataset
from scripts.config import DATA_PATH_SALES
from scripts.regressions.helpers import test_regression, train_test_dataset_split
from scripts.regressions.linear import build_linear_regression
from scripts.regressions.dataset_scaler import Dataset_scaler
from scripts.helpers import delete_useless_elements

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

x_cols = delete_useless_elements(list(dataset.columns), 
    useless_elements=["Name", "Publisher", "Global_Sales", "Region_Sales"])
y_cols = ["Region_Sales"]

dataset_scaler = Dataset_scaler(dataset)
dataset_scaler.scale(x_cols)

x_train, y_train, x_test, y_test = train_test_dataset_split(dataset, x_cols, y_cols)

linear_regression = build_linear_regression(x_train, y_train)
linear_result_mean, linear_result_r2 = test_regression(linear_regression, x_test, y_test)
print(linear_result_mean, linear_result_r2)
