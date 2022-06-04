from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer


def draw_graph(x_range, y, labels):
    plt.figure(figsize=(10, 8))
    plt.plot(x_range, y)
    plt.xticks(x_range)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.grid(linestyle='--')
    plt.show()


def remove_symbols(dataset: DataFrame):
    return dataset.replace({"[^A-Za-z0-9 ]+": ""}, regex=True)


def convert_textdata_into_vectors(dataset: DataFrame, vectorizer):
    # vectorizer = TfidfVectorizer(stop_words='english') put in main
    return vectorizer.fit_transform(dataset)


def get_sum_of_square_errors(features: DataFrame, max_kernels: int, kmeans_kwargs: dict):
    sse = []
    for k in range(1, max_kernels + 1):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(features)
        sse.append(kmeans.inertia_)

    return sse


def get_clusters_count(sse: list, max_kernels: int):
    """use elbow test"""
    kl = KneeLocator(range(1, max_kernels + 1), sse,
                     curve='convex', direction='decreasing')
    print(f'Точка лiктя: {kl.elbow}')
    return kl.elbow


def get_clusters(features: DataFrame, kmeans_kwargs: dict):
    return KMeans(**kmeans_kwargs).fit(features)


def cluster_predict(element: DataFrame, model):
    return model.predict(element)

