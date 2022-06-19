from typing import Tuple
import pandas as pd
from pandas import DataFrame

def read_dataset(dataset_path : str, **kwargs) -> DataFrame:
    dataset = pd.read_csv(dataset_path, **kwargs)
    return dataset


def split_dataframe(
    dataset : DataFrame,
    first_cols : list,
    second_cols : list) -> Tuple[DataFrame, DataFrame]:
    first = dataset[first_cols]
    second = dataset[second_cols]
    return first, second

  
def get_key_by_value(dict: dict, value):
    return [key for key, val in dict.items() if val == value][0]

  
def split_list(list : list, elements : list) -> Tuple[list, list]:
    return elements, [other for other in list if other not in elements]
