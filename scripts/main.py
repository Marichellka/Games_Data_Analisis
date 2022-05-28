import pandas as pd
from pickle import dump
from scripts.cleansing import read_and_cleanse
from scripts.config import DATA_PATH_VGSALES, ASSET_PATH_GAMESMODEL
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements, split_list
from scripts.regressions.helpers import get_regression_model
from scripts.correlation.helpers import print_coor_matrix

#TODO: create web API

dataset = read_and_cleanse(DATA_PATH_VGSALES, mode_columns=["Year"], float_columns=["Year"])

all_cols = delete_useless_elements(list(dataset.columns),
    ["Rank", "Name", "Year", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"])

dataset = dataset[all_cols]

y_cols, x_cols = split_list(all_cols, ["Global_Sales"])

dataset_scaler = DatasetScaler(dataset, x_cols)

regression_model, score = get_regression_model(dataset_scaler.scaled_dataset, x_cols, y_cols, shuffle=True)

predictions = regression_model.predict(dataset_scaler.scaled_dataset[x_cols])

print_coor_matrix(dataset_scaler.scaled_dataset, "Global_Sales", x_cols)

dump(regression_model, open(ASSET_PATH_GAMESMODEL, "wb"))
