import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from typing import Callable


def change_float_to_int(dataset: DataFrame, columns : list) -> None:
    dataset[columns] = dataset[columns].astype('int')


def cleanse_data(
    dataset : DataFrame,
    mean_columns : list = [],
    mode_columns : list = [],
    float_columns : list = [],
    delete_columns : list = [],
    sort_column : str = None,
    low_percentile : int = 25,
    high_percentile : int = 75) -> None:
    for column in delete_columns:
        dataset.drop(column, axis=1, inplace=True)
    replace_with_mean(dataset, mean_columns)
    replace_with_mode(dataset, mode_columns)
    change_float_to_int(dataset, float_columns)
    if (sort_column):
        sorted_data = np.sort(dataset[sort_column])
        q1 = np.percentile(sorted_data, low_percentile)
        q3 = np.percentile(sorted_data, high_percentile)
        iqr = q3 - q1
        lower_range = q1 - 1.5 * iqr
        upper_range = q3 + 1.5 * iqr
        outlier_free_list = [x for x in dataset[sort_column] if (
            (x > lower_range) & (x < upper_range))]
        dataset = dataset.loc[dataset[sort_column].isin(outlier_free_list)]

    return dataset


def replace_with_mean(dataset : DataFrame, columns : list) -> None:
    for column in columns:
        dataset[column].fillna(dataset[column].mean(numeric_only=True), inplace=True)


def replace_with_mode(dataset : DataFrame, columns : list) -> None:
    for column in columns:
        dataset[column].fillna(dataset[column].mode()[0], inplace=True)


def stack_dataset(dataset: DataFrame, stack_cols : dict, new_cols : list, values_func : Callable) -> DataFrame:
    old_cols = list(filter(lambda c: c not in stack_cols.keys(), dataset.columns))
    new_rows = []
    for _, row in dataset.iterrows():
        for key, value in stack_cols.items():
            new_row = [*row[old_cols], *values_func(row, key, value)]
            new_rows.append(new_row)
    return pd.DataFrame(data=new_rows, columns=[old_cols + new_cols])
