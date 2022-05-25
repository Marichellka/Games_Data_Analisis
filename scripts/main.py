from scripts.cleansing import read_and_cleanse
from scripts.config import DATA_PATH_SALES
from scripts.regressions.helpers import get_regression_model

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

# TODO: Marichellka please add non-numeric columns to x_cols. 
x_cols = ["Year"]
y_cols = ["Global_Sales"]

regression_model, score = get_regression_model(dataset, x_cols, y_cols)
