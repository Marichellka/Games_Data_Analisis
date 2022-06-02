from pandas import DataFrame
from scripts.utils.dataset_scaler import DatasetScaler
from scripts.helpers import delete_useless_elements
from scripts.clusters.helpers import draw_graph, get_clusters, get_clusters_count, get_sum_of_square_errors

def clustering(dataset: DataFrame):
    features = delete_useless_elements(list(dataset.columns), 
        useless_elements=["Region_Sales", "Global_Sales"])

    dataset_scaler = DatasetScaler(dataset, features)

    # Визначаємо кількість кластерів
    kmeans_kwargs = {
        'init': 'random',
        'n_init': 10,
        'max_iter': 300,
        'random_state': 42,
    }

    max_kernels = 30
    sse = get_sum_of_square_errors(features, max_kernels, kmeans_kwargs)
    draw_graph(x_range=range(1, max_kernels+1), y=sse, 
                labels=['Number of Clusters','SSE'])
    
    n_clusters = get_clusters_count(sse, max_kernels)
    kmeans_kwargs['n_clusters']=n_clusters
    clusters = get_clusters()