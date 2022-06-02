from pandas import DataFrame

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
            if str(element) not in dictionary:
                dictionary[str(element)] = 1
            else:
                dictionary[str(element)] += 1
        return dictionary


    def __replace_data(self, column):
        self.__dataset[column] = self.__dataset[column].replace(
            self.__dictionary[column].keys(), 
            self.__dictionary[column].values())
