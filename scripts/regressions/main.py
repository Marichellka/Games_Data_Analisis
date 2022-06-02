from pandas import DataFrame
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements
from scripts.regressions.helpers import get_regression_model

def regression_analysis(dataset: DataFrame):
    x_cols = delete_useless_elements(list(dataset.columns), 
        useless_elements=["Name", "Publisher", "Global_Sales", "Region_Sales"])
    y_cols = ["Region_Sales"]

    dataset_scaler = DatasetScaler(dataset, x_cols)

    regression_model, score = get_regression_model(dataset_scaler.scaled_dataset, x_cols, y_cols)
