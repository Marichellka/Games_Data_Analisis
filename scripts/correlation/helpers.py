from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from scripts.config import ASSET_PATH_CORRELATION

def draw_corr(data: DataFrame, method: str) ->None:
    plt.figure(figsize=(10,6))
    sns.heatmap(data.corr(method), annot = True)
    plt.savefig(ASSET_PATH_CORRELATION+"_"+method+".jpg")

def print_coor_matrix(dataFrame: DataFrame) -> None:
    draw_corr(dataFrame, "pearson")
    draw_corr(dataFrame, "kendall")
    draw_corr(dataFrame, "spearman")
