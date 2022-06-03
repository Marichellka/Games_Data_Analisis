from pickle import dump
from scripts.cleansing import cleanse_data
from scripts.config import ASSET_PATH_REGRESSIONS_DUMP, DATA_PATH_VGSALES
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements, split_list, read_dataset
from scripts.regressions.helpers import get_regressions
from scripts.correlation.helpers import print_coor_matrix
from scripts.utils.regressions_analyzer import RegressionsAnalyzer

#TODO: create web API

delete_cols = ["Rank", "Name", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]

dataset = read_dataset(DATA_PATH_VGSALES)

cleanse_data(
    dataset,
    mode_columns=["Year"],
    float_columns=["Year"],
    delete_columns=delete_cols)

y_cols, x_cols = split_list(list(dataset.columns), ["Global_Sales"])

dataset_scaler = DatasetScaler(dataset, x_cols)

regressions = list(get_regressions())

analyzer = RegressionsAnalyzer(dataset_scaler.scaled_dataset, regressions, x_cols, y_cols)

analyzer.run()

analyzer.dump_scores(ASSET_PATH_REGRESSIONS_DUMP)

print_coor_matrix(dataset_scaler.scaled_dataset, "Global_Sales", x_cols)
