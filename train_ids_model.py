import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# IDS-style numeric data
X = np.random.rand(2000, 20)   # 20 features (safe default)
y = np.random.choice([0, 1], size=2000)  # 0=benign, 1=attack

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

with open("models/ids_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ IDS model trained and saved")
print("📦 Location: models/ids_model.pkl")
print("📏 File size should now be > 0 bytes")
