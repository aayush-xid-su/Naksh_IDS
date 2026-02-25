import pandas as pd
import time
import os

def stream_csv_files(data_dir, batch_size=5, delay=1):
    files = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(".csv")
    ]

    for file_path in files:
        df = pd.read_csv(file_path)
        dataset_name = os.path.basename(file_path)

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size].copy()
            yield dataset_name, batch
            time.sleep(delay)
