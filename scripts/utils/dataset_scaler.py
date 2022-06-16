from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer

# TODO: improve scaling.
class DatasetScaler:

    def __init__(self, dataset: DataFrame, columns : list = None) -> None:
        self.__dataset=dataset.copy(True)
        self.__columns = columns
        if (columns):
            self.__scale()


    @property
    def scaled_dataset(self) -> DataFrame:
        return self.__dataset


    def get_scaled_value(self, value: str, column: str):
        if column not in self.__dictionary.keys():
            return value
        return self.__dictionary[column][value]


    def __scale(self) -> None:
        self.__dictionary = dict()
        for column in self.__columns:
            self.__dictionary[column]=self.__get_column_dictionary(column)
            self.__replace_data(column)
        # vectorized_data = self.__vectorize_data().tocoo().data
        # divided_data = self.__divide_array(vectorized_data, len(self.__columns))
        # for i in range(len(self.__columns)):
        #     self.__dataset[self.__columns[i]]=divided_data[i]


    def __replace_data(self, column) -> None:
        self.__dataset[column] = self.__dataset[column].replace(
            self.__dictionary[column].keys(), 
            self.__dictionary[column].values())

    
    def __get_column_dictionary(self, column: str) -> dict:
        dictionary = dict()
        for element in self.__dataset[column]:
            if element not in dictionary:
                dictionary[element] = 1
            else:
                dictionary[element] += 1
        for key, val in dictionary.items():
            dictionary[key] = val/len(self.__dataset)
        return dictionary


    def __divide_array(self, array : list, n: int):
        divided_arrays = [[] for _ in range(n)]
        for i in range(0, len(array), n):
            for j in range(n):
                divided_arrays[j].append(array[i+j])
        return divided_arrays


    def __remove_symbols(self):
        return self.__dataset[self.__columns].replace([r"[^A-Za-z0-9]+"], [""], regex=True)


    def __combine_data(self, data: DataFrame):
        combined_data = data[self.__columns].apply(lambda row: \
            ' '.join(row.values.astype(str)), axis=1)
        return combined_data


    def __vectorize_data(self):
        data = self.__remove_symbols()
        combined_data = self.__combine_data(data)
        vectorizer = TfidfVectorizer(stop_words='english')
        return vectorizer.fit_transform(list(combined_data))
