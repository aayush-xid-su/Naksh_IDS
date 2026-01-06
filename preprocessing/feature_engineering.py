from sklearn.feature_selection import VarianceThreshold

def remove_low_variance(X, threshold=0.01):
    selector = VarianceThreshold(threshold)
    return selector.fit_transform(X), selector
