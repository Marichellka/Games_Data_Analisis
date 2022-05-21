import pandas as pd
from pandas import DataFrame

def read_and_cleanse(dataset_path : str, \
    mean_columns : list = [], \
    mode_columns : list = [],
    **kwargs):
    dataset = pd.read_csv(dataset_path, **kwargs)
    cleanse_data(dataset, mean_columns, mode_columns)
    return dataset

def cleanse_data(dataset : DataFrame, \
    mean_columns : list = [], \
    mode_columns : list = []):
    for column in mean_columns:
        replace_with_mean(dataset, column)
    for column in mode_columns:
        replace_with_mode(dataset, column)

def replace_with_mean(dataset : DataFrame):
    dataset.fillna(dataset.mean(numeric_only=True), inplace=True)

def replace_with_mode(dataset : DataFrame):
    for column in dataset.columns:
        dataset[column].fillna(dataset[column].mode()[0], inplace=True)
