from scripts.cleansing import read_and_cleanse
from scripts.config import DATA_PATH_SALES
from scripts.regressions.dataset_scaler import Dataset_scaler
from scripts.helpers import delete_useless_elements
from scripts.regressions.helpers import get_regression_model

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

x_cols = delete_useless_elements(list(dataset.columns), 
    useless_elements=["Name", "Publisher", "Global_Sales", "Region_Sales"])
y_cols = ["Region_Sales"]

dataset_scaler = Dataset_scaler(dataset)
dataset_scaler.scale(x_cols)

regression_model, score = get_regression_model(dataset, x_cols, y_cols)
