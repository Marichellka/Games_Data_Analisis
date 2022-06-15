from pandas import DataFrame
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.feature_extraction.text import TfidfVectorizer
from scripts.config import ASSET_PATH_ELBOWPLOT, ASSET_PATH_CLUSTERSPLOT


def draw_graph(x_range, y, labels) -> None:
    plt.figure(figsize=(10, 8))
    plt.plot(x_range, y)
    plt.xticks(x_range)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.grid(linestyle='--')
    plt.show()


def remove_symbols(dataset: DataFrame, cols: list):
    return dataset[cols].replace([r"[^A-Za-z0-9]+"], [""], regex=True)


def combine_data(dataset: DataFrame, cols: list):
    combined_data = dataset[cols].apply(lambda row: \
        ' '.join(row.values.astype(str)), axis=1)
    return combined_data


def vectorize_data(dataset: DataFrame, cols: list):
    data = remove_symbols(dataset, cols)
    combined_data = combine_data(data, cols)
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(list(combined_data))


def get_sum_of_square_errors(features: DataFrame, algorithm: object, max_kernels: int, **kwargs: dict) -> list:
    sse = []
    for k in range(1, max_kernels + 1):
        clustering = algorithm(n_clusters=k, **kwargs).fit(features)
        sse.append(clustering.inertia_)

    return sse


def get_clusters_count(sse: list) -> int:
    """use elbow test"""
    kl = KneeLocator(range(1, len(sse) + 1), sse,
                     curve='convex', direction='decreasing')
    return kl.elbow


def get_clusters(features: DataFrame, algorithm: object, **kwargs: dict):
    return algorithm(**kwargs).fit(features)


def cluster_predict(elements, model):
    return model.predict(elements)

  
def plot_elbow_test(sse : list) -> None:
    plt.plot(list(range(0, len(sse))), sse)
    plt.xlabel("Number of clusters")
    plt.ylabel("SSE")
    plt.savefig(ASSET_PATH_ELBOWPLOT)


def devide_array(array : list, n: int):
    devided_arrays = [[] for i in range(n)]
    for i in range(0, len(array), n):
        for j in range(n):
            devided_arrays[j].append(array[i+j])
    return devided_arrays


def draw_subplot(fig: plt.figure, pos: int, data: list, 
                colors: list, view: tuple, labels: list):
    ax = fig.add_subplot(pos, projection='3d')
    ax.scatter(data[labels[0]], data[labels[1]], 
                data[labels[2]], c=colors, s=1)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    ax.view_init(view[0], view[1])


def show_clusters(features, cols: list, y_kmeans): 
    fig = plt.figure(figsize=(16,6))
    draw_subplot(fig, 131, features, y_kmeans, 
                view=(60, 30), labels = cols)
    draw_subplot(fig, 132, features, y_kmeans, 
                view=(0, 60), labels = cols)
    draw_subplot(fig, 132, features, y_kmeans,
                view=(0, -80), labels = cols)
    plt.savefig(ASSET_PATH_CLUSTERSPLOT)
