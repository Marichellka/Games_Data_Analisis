from pandas import DataFrame


def split_dataframe(
    dataset : DataFrame,
    first_cols : list,
    second_cols : list):
    first = dataset[first_cols]
    second = dataset[second_cols]
    return first, second
