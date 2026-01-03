# ga/fitness.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

def fitness_function(ga_instance, solution, solution_idx,
                     X_train, X_test, y_train, y_test):

    # ---- Ensure NumPy arrays (CRITICAL FIX) ----
    if not isinstance(y_train, np.ndarray):
        y_train = y_train.to_numpy()

    if not isinstance(y_test, np.ndarray):
        y_test = y_test.to_numpy()

    # ---- Feature mask ----
    feature_mask = solution[:-2] > 0.5
    num_selected = feature_mask.sum()

    if num_selected == 0:
        return 0.0

    # ---- Hyperparameters ----
    n_estimators = int(np.clip(solution[-2], 30, 80))
    max_depth = int(np.clip(solution[-1], 5, 15))

    # ---- Subsampling (memory-safe) ----
    max_samples = 8000
    n_train = X_train.shape[0]

    if n_train > max_samples:
        idx = np.random.choice(n_train, max_samples, replace=False)
        X_train_sub = X_train[idx][:, feature_mask]
        y_train_sub = y_train[idx]      # ✅ NumPy-safe
    else:
        X_train_sub = X_train[:, feature_mask]
        y_train_sub = y_train

    # ---- Lightweight RF ----
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=5,
        max_features="sqrt",
        n_jobs=1,
        random_state=42
    )

    model.fit(X_train_sub, y_train_sub)

    preds = model.predict(X_test[:, feature_mask])
    score = f1_score(y_test, preds, average="weighted")

    # ---- Feature penalty ----
    penalty = num_selected / X_train.shape[1]

    return score - 0.1 * penalty
