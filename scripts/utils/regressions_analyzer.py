from itertools import combinations
from pandas import DataFrame

from scripts.regressions.helpers import test_regressions, train_test_dataset_split

class RegressionsAnalyzer:

    def __init__(
        self,
        dataset : DataFrame,
        regressions : list,
        x_cols : list,
        y_cols : list) -> None:
        self.__regressions = regressions
        self.__dataset = dataset
        self.__x_cols = x_cols
        self.__y_cols = y_cols


    @property
    def raw_scores(self) -> dict:
        return self.__regressions_scores


    def run(self) -> None:
        x_cols_combinations = {}
        idx = 0
        for length in range(1, len(self.__x_cols) + 1):
            for combination in combinations(self.__x_cols, length):
                x_cols_combinations[idx] = list(combination)
                idx += 1
        self.__x_cols_combinations = x_cols_combinations

        regressions_lookup = {}
        for idx, regression in enumerate(self.__regressions):
            regressions_lookup[idx] = regression
        self.__regressions_lookup = regressions_lookup

        regressions_scores = {}
        
        for idx, combination in self.__x_cols_combinations.items():
            regressions_scores[idx] = self.get_regressions_scores(combination)

        self.__regressions_scores = regressions_scores


    def get_regressions_scores(self, x_cols : list) -> dict:
        x_train, y_train, x_test, y_test = \
            train_test_dataset_split(self.__dataset, x_cols, self.__y_cols)
        
        fit_regressions = [regression.fit(x_train, y_train) \
            for regression in self.__regressions]

        regressions_tests = list(test_regressions(fit_regressions, x_test, y_test))

        beneficial_funcs = [
            lambda x: x, # mean squared error
            lambda x: [value + abs(min(x)) for value in x] # r2_score
        ]

        regressions_scores = {}

        for idx, score in enumerate(self.evaluate_regressions_tests(regressions_tests, beneficial_funcs)):
            regressions_scores[idx] = score

        return regressions_scores


    # beneficial_funcs is a list of functions used to convert corresponding values into beneficial ones.
    # it is expected that the return value will be >= 0.
    def evaluate_regressions_tests(self, regressions_tests : list, beneficial_funcs : list) -> dict:
        beneficial_criterions_lists = \
            [beneficial_funcs[idx](test_values) \
                for idx, test_values in enumerate(list(map(list, zip(*regressions_tests))))]
        max_criterions_list = \
            [max(criterions) \
                for criterions in beneficial_criterions_lists]
        # worst == 0, best == number of criterions in regressions_tests
        regressions_scores = \
            [sum([value / max_criterions_list[idx] for idx, value in enumerate(test)]) \
                for test in regressions_tests]
        return regressions_scores


    def dump_scores(self, filename : str) -> None:
        with open(filename, "w") as text_file:
            for i, regressions_scores in self.__regressions_scores.items():
                for j, score in regressions_scores.items():
                    text_file.write(f"Combination: {self.__x_cols_combinations[i]}, ")
                    text_file.write(f"Regression: {self.__regressions_lookup[j]}, ")
                    text_file.write(f"Score: {score}\n")
