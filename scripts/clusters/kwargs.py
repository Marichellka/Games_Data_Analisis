kmeans_kwargs = {
    'init': 'random',
    'n_init': 10,
    'max_iter': 500,
    'random_state': 42,
}
bisecting_kmeans_kwargs = {
    'init': 'random',
    'n_init': 10,
    'max_iter': 500,
    'random_state': 42,
    'bisecting_strategy': 'largest_cluster',
}
spectral_kwargs = {
    'n_init': 10,
    'random_state': 42,
    'assign_labels': 'cluster_qr',
}
gaussian_mixture_kwargs = {
    'n_init': 10,
    'max_iter': 500,
    'random_state': 42,
}