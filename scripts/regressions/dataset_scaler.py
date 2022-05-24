from pandas import DataFrame

class Dataset_scaler:

    def __init__(self, dataset: DataFrame):
        self.dataset=dataset


    def scale(self, columns: list):
        self.dictionary = dict()
        for column in columns:
            self.dictionary[column]=self.__get_column_dictionary(column)
            self.__replace_data(column)


    def __get_column_dictionary(self, column: str):
        dictionary = dict()
        for element in self.dataset[column]:
            if str(element) not in dictionary:
                dictionary[str(element)] = len(dictionary)
        return dictionary


    def __replace_data(self, column):
        self.dataset[column] = self.dataset[column].replace(
            self.dictionary[column].keys(), 
            self.dictionary[column].values())