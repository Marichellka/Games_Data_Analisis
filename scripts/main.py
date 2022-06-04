from numpy import rec
from scripts.cleansing import read_and_cleanse
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.config import DATA_PATH_VGSALES
from scripts.utils.recommendation_system import RecommendationSystem

#TODO: create web API

delete_cols = ["Rank", "Name", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]

dataset = read_and_cleanse(DATA_PATH_VGSALES, mode_columns=["Year"])

x_cols = [col for col in dataset.columns if col not in delete_cols]

dataset_scaler = DatasetScaler(dataset, x_cols)

recommandation = RecommendationSystem(dataset_scaler.scaled_dataset)
recommandation.build_system(x_cols)