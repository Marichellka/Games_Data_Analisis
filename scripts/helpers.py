from pandas import DataFrame

def split_dataframe(
    dataset : DataFrame,
    first_cols : list,
    second_cols : list):
    first = dataset[first_cols]
    second = dataset[second_cols]
    return first, second


def delete_useless_elements(list, useless_elements):
    for elem in useless_elements:
        list.remove(elem)
    return list
    

def get_key_by_value(dict: dict, value):
    return [key for key, val in dict.items() if val == value][0]
