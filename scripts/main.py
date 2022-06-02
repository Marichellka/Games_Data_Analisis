from scripts.cleansing import read_and_cleanse
from scripts.config import DATA_PATH_SALES
from scripts.regressions.main import regression_analysis
from scripts.clusters.main import clustering

#TODO: create web API

dataset = read_and_cleanse(DATA_PATH_SALES, mode_columns=["Year"])

regression_analysis(dataset)

clustering(dataset)