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


def split_list(list : list, elements : list):
    return elements, [other for other in list if other not in elements]
