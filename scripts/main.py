from numpy import rec
from pickle import dump
from scripts.cleansing import cleanse_data
from scripts.config import ASSET_PATH_REGRESSIONS_DUMP, DATA_PATH_VGSALES
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements, split_list, read_dataset
from scripts.regressions.helpers import get_regressions
from scripts.correlation.helpers import print_coor_matrix
from scripts.utils.regressions_analyzer import RegressionsAnalyzer
from scripts.utils.recommendation_system import RecommendationSystem

#TODO: create web API

# regressions
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


# recommendations
delete_cols = ["Rank", "Name", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]

dataset = read_and_cleanse(DATA_PATH_VGSALES, mode_columns=["Year"])

x_cols = [col for col in dataset.columns if col not in delete_cols]

dataset_scaler = DatasetScaler(dataset, x_cols)

recommendation = RecommendationSystem(dataset_scaler.scaled_dataset)
recommendation.build_system(x_cols)

test = dataset.iloc[[100]][x_cols]
print(test, '\n')
test = dataset_scaler.scale_row(test)
recommendations = recommendation.recommend(test)
recommendations = dataset_scaler.unscale_data(recommendations, x_cols)
print(str(recommendations[["Name"]+x_cols]))

