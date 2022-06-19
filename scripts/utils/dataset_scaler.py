from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer

class DatasetScaler:

    def __init__(self, dataset: DataFrame, columns : list = None) -> None:
        self.__original_dataset=dataset
        self.__dataset=dataset.copy(True)
        self.__columns = columns
        if (columns):
            self.__scale()


    @property
    def scaled_dataset(self) -> DataFrame:
        return self.__dataset


    @property
    def original_dataset(self) -> DataFrame:
        return self.__original_dataset


    def __scale(self) -> None:
        vectorized_data = self.__vectorize_data().tocoo().data
        divided_data = self.__divide_array(vectorized_data, len(self.__columns))
        for i in range(len(self.__columns)):
            self.__dataset[self.__columns[i]]=divided_data[i]


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
