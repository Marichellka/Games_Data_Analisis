from pandas import DataFrame


def print_coor_matrix(dataFrame: DataFrame) -> None:
    print("Pearson correlation\n", dataFrame.corr("pearson"))
    print("Kendall correlation\n", dataFrame.corr("kendall"))
    print("Spearman correlation\n", dataFrame.corr("spearman"))
