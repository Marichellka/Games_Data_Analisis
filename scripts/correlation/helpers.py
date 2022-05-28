from pandas import DataFrame
import pingouin as pg


def print_coor_matrix(dataFrame: DataFrame, column: str, columns: list):
    corrmat = pg.pairwise_corr(dataFrame, columns=[columns, [column]])
    print(corrmat)