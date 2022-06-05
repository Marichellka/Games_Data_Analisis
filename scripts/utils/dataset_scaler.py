from pandas import DataFrame
from scripts.helpers import get_key_by_value

class DatasetScaler:

    def __init__(self, dataset: DataFrame, columns : list = None):
        self.__dataset=dataset.copy(True)
        if (columns):
            self.__scale(columns)


    @property
    def scaled_dataset(self):
        return self.__dataset


    def get_scaled_value(self, value: str, column: str):
        return self.__dictionary[column][value]


    def __scale(self, columns : list):
        self.__dictionary = dict()
        for column in columns:
            self.__dictionary[column]=self.__get_column_dictionary(column)
            self.__replace_data(column)


    def __get_column_dictionary(self, column: str):
        dictionary = dict()
        for element in self.__dataset[column]:
            if element not in dictionary:
                dictionary[element] = len(dictionary)
        return dictionary


    def __replace_data(self, column):
        self.__dataset[column] = self.__dataset[column].replace(
            self.__dictionary[column].keys(), 
            self.__dictionary[column].values())


    def scale_row(self, row: DataFrame):
        for column in row.columns:
            try:
                row[column] = self.__dictionary[column][row[column]]
            except:
                row[column] = len(self.__dictionary[column])
        return row

    def unscale_data(self, scaled_data: DataFrame, cols: list):
        data = scaled_data
        for i in range(len(scaled_data)):
            data.iloc[i] = self.__get_normal_row_from_scaled(data.iloc[i], cols)
        return data
    
    def __get_normal_row_from_scaled(self, scaled_row: DataFrame, cols: list):
        row = scaled_row
        for column in cols:
            row[column] = get_key_by_value(self.__dictionary[column], scaled_row[column])
        return row
