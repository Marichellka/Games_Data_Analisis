from scripts.cleansing import read_and_cleanse
from scripts.clusters.helpers import get_clusters_count, get_sum_of_square_errors, plot_elbow_test
from scripts.config import DATA_PATH_SALES
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements, split_list
from scripts.regressions.helpers import get_regression_model, predict_unscaled

#TODO: create web API

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

all_cols = delete_useless_elements(list(dataset.columns),
    ["Name", "Publisher", "Global_Sales"])

dataset = dataset[all_cols]

y_cols, x_cols = split_list(all_cols, ["Region_Sales"])

dataset_scaler = DatasetScaler(dataset, x_cols)

regression_model, score = get_regression_model(dataset_scaler.scaled_dataset, x_cols, y_cols)
