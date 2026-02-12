import numpy as np
import pandas as pd
import random


class AttackSimulator:
    def __init__(self, attack_ratio=0.2, intensity=3.0):
        """
        attack_ratio: fraction of rows to corrupt
        intensity: how aggressive the attack is
        """
        self.attack_ratio = attack_ratio
        self.intensity = intensity

    def inject(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return df

        n_attack = int(len(df) * self.attack_ratio)
        attack_rows = random.sample(range(len(df)), n_attack)

        for col in numeric_cols:
            # SOC-style: spikes, floods, abnormal entropy
            df.loc[attack_rows, col] = (
                df.loc[attack_rows, col].astype(float) * self.intensity
            )

        return df
