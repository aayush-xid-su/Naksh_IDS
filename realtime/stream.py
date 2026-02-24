import os
import glob
import pandas as pd
from datetime import datetime

def stream_datasets(data_dir="data", batch_size=512):
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    for csv in csv_files:
        df = pd.read_csv(csv)
        # Stream in batches
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start:start+batch_size].copy()
            yield batch, os.path.basename(csv)
