import pandas as pd
from pandas import DataFrame

def read_and_cleanse(dataset_path : str,
    delete_columns : list = [],
    mean_columns : list = [],
    mode_columns : list = [],
    **kwargs):
    dataset = pd.read_csv(dataset_path, **kwargs)
    for column in delete_columns:
        dataset = dataset.drop(column, axis=1)
    cleanse_data(dataset, mean_columns, mode_columns)
    return dataset


def cleanse_data(dataset : DataFrame,
    mean_columns : list = [],
    mode_columns : list = []):
    replace_with_mean(dataset, mean_columns)
    replace_with_mode(dataset, mode_columns)

def replace_with_mean(dataset : DataFrame, columns : list):
    for column in columns:
        dataset[column].fillna(dataset[column].mean(numeric_only=True), inplace=True)

def replace_with_mode(dataset : DataFrame, columns : list):
    for column in columns:
        dataset[column].fillna(dataset[column].mode()[0], inplace=True)


def refactor_data(dataset: DataFrame):
    regions = {'NA_Sales':'North America', 'EU_Sales':'Europe', 
    'JP_Sales':'Japan', 'Other_Sales':'Other'}
    new_dataset = pd.DataFrame(columns = [])
    for ind in range(len(dataset)):
        row = dataset.iloc[ind:].head(1)
        for key, value in regions.items():
            new_row = row[['Name','Platform','Year','Genre','Publisher']]
            new_row = insert_columns(new_row, columns=['Region', 'Region_Sales', 'Global_Sales'],
                                    values=[[value], row[[key]].values[0], row[['Global_Sales']].values[0]])
            new_dataset = pd.concat([new_dataset, new_row])
    return new_dataset


def insert_columns(row, columns, values):
    for index in range(len(row.columns), \
        len(row.columns)+len(columns)):
        row.insert(index, columns[index], values[index])
    return row
        

dataset = read_and_cleanse("data/vgsales.csv", delete_columns=['Rank'])
refactor_data(dataset).to_csv('data/sales.csv')

