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
        features = self.__dataset[x_cols]
        kmeans_kwargs = {
            'init': 'random',
            'n_init': 10,
            'max_iter': 500,
            'random_state': 42,
        }

        max_kernels = 30
        sse = get_sum_of_square_errors(features, max_kernels, kmeans_kwargs)
        draw_graph(x_range=range(1, max_kernels+1), y=sse, 
                    labels=['Number of Clusters','SSE'])
        
        n_clusters = get_clusters_count(sse, max_kernels)
        kmeans_kwargs['n_clusters'] = n_clusters
        self.__model = get_clusters(features, kmeans_kwargs)

        self.__dataset['Cluster_Prediction']=self.__dataset.apply(
            cluster_predict(features, self.__model), axis=0)


    def recommend(self, elements: DataFrame, count: int = 10) -> list:
        prediction = int(cluster_predict(elements, self.__model))

        recommendations = self.__dataset.loc[
            self.__dataset['ClusterPrediction'] == prediction]
        recommendations = recommendations.sample(count)

        return list(recommendations)
