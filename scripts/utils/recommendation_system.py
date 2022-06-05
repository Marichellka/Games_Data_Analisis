from typing import List
from pandas import DataFrame
from scripts.clusters.helpers import draw_graph, get_clusters, \
get_clusters_count, get_sum_of_square_errors, cluster_predict

class RecommendationSystem:

    def __init__(
        self, 
        dataset: DataFrame) -> None:
        self.__dataset = dataset


    def build_system(self, x_cols:list):
        features = self.__dataset.loc[:, x_cols]
        features.fillna(features.mean(numeric_only=True), inplace=True)
        kmeans_kwargs = {
            'init': 'random',
            'n_init': 10,
            'max_iter': 500,
            'random_state': 42,
        }

        max_kernels = 30
        sse = get_sum_of_square_errors(features, max_kernels, kmeans_kwargs)
        
        n_clusters= get_clusters_count(sse, max_kernels)
        self.__model = get_clusters(features, n_clusters=n_clusters, **kmeans_kwargs)

        clusters = cluster_predict(features, self.__model)
        self.__dataset['Cluster_Prediction']=list(clusters)


    def recommend(self, elements: DataFrame, count: int = 10) -> DataFrame:
        prediction = int(cluster_predict(elements, self.__model))

        recommendations = self.__dataset.loc[
            self.__dataset['Cluster_Prediction'] == prediction]
        recommendations = recommendations.sample(count)

        return DataFrame(recommendations)

    def show_clusters_info(self, sse: list, max_kernels:int):
        draw_graph(x_range=range(1, max_kernels+1), y=sse, 
                    labels=['Number of Clusters','SSE'])
