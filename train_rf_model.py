# train_rf_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import joblib

# -----------------------------
# 1. Load datasets
# -----------------------------
datasets = [
    "data/dataset1.csv",
    "data/dataset2.csv",
    "data/dataset3.csv",
    "data/dataset4.csv"
]

df_list = [pd.read_csv(f) for f in datasets]
data = pd.concat(df_list, ignore_index=True)

# -----------------------------
# 2. Define features and target
# -----------------------------
target_column = "Attack_Type"  # Replace with your actual target
features = [col for col in data.columns if col != target_column]

X = data[features].copy()
y = data[target_column].copy()

# -----------------------------
# 2.1 Drop rows with missing target
# -----------------------------
mask = y.notna()
X = X.loc[mask, :].copy()
y = y.loc[mask].copy()

# -----------------------------
# 3. Drop fully empty columns
# -----------------------------
X = X.dropna(axis=1, how='all')

# -----------------------------
# 4. Convert datetime columns safely (warning-free)
# -----------------------------
for col in X.columns:
    if pd.api.types.is_object_dtype(X[col]):
        try:
            # Parse datetime strings with explicit format
            X[col] = pd.to_datetime(X[col], format="%Y-%m-%d %H:%M:%S", errors='coerce')
        except Exception:
            continue
    if pd.api.types.is_datetime64_any_dtype(X[col]):
        # Create numeric features
        X[col + "_year"] = X[col].dt.year
        X[col + "_month"] = X[col].dt.month
        X[col + "_day"] = X[col].dt.day
        X[col + "_hour"] = X[col].dt.hour
        X[col + "_minute"] = X[col].dt.minute
        X[col + "_second"] = X[col].dt.second
        X.drop(col, axis=1, inplace=True)

# -----------------------------
# 5. Handle numeric columns
# -----------------------------
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
# Keep only columns with at least one non-NaN value
numeric_cols = [col for col in numeric_cols if X[col].notna().any()]

if numeric_cols:
    imputer_num = SimpleImputer(strategy='median')
    X[numeric_cols] = imputer_num.fit_transform(X[numeric_cols])

# -----------------------------
# 6. Handle categorical columns
# -----------------------------
categorical_cols = X.select_dtypes(include=['object', 'category']).columns
label_encoders = {}
for col in categorical_cols:
    X[col] = X[col].astype(str)
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# -----------------------------
# 7. Fill any remaining NaNs
# -----------------------------
X.fillna(0, inplace=True)

# -----------------------------
# 8. Split train/test
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 9. Train Random Forest
# -----------------------------
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# -----------------------------
# 10. Evaluate
# -----------------------------
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 11. Save model with feature names
# -----------------------------
joblib.dump(
    {"model": rf_model, "feature_names": X.columns.tolist(), "label_encoders": label_encoders},
    "models/rf_v1.joblib"
)

print("Model saved as models/rf_v1.joblib with feature names and label encoders.")
