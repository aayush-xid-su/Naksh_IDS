# realtime/simulator.py
import numpy as np
import pandas as pd

def generate_batch(batch_size: int, feature_names: list):
    """
    Generate simulated real-time batch data
    """
    data = {}
    for f in feature_names:
        # random numerical/fake data
        data[f] = np.random.rand(batch_size)
    return pd.DataFrame(data)
