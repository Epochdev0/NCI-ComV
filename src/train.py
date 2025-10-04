"""Simple training script: loads CSV with features + label, trains RandomForest, saves model."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# ----------------------
# 1. Load dataset
# ----------------------
file_path = "nasa_exoplanet_cumulative.csv"  # Change to your dataset path
df = pd.read_csv(file_path, comment="#")

# ----------------------
# 2. Drop irrelevant columns
# ----------------------
drop_cols = [
    'kepid', 'kepoi_name', 'kepler_name', 'koi_pdisposition',
    'koi_tce_delivname', 'ra', 'dec'
]
# Drop error columns (ending with _err1/_err2)
drop_cols += [col for col in df.columns if col.endswith(('_err1', '_err2'))]

df_clean = df.drop(columns=drop_cols, errors="ignore")

# ----------------------
# 3. Handle missing values
# ----------------------
# Drop columns with >40% missing values
threshold = 0.4
missing_ratio = df_clean.isna().mean()
drop_missing = missing_ratio[missing_ratio > threshold].index.tolist()
df_clean = df_clean.drop(columns=drop_missing)

# Fill remaining missing values
for col in df_clean.columns:
    if df_clean[col].dtype in [np.float64, np.int64]:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    else:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# ----------------------
# 4. Encode target column
# ----------------------
target = 'koi_disposition'
X = df_clean.drop(columns=[target])
y = df_clean[target]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ----------------------
# 5. Scale numeric features
# ----------------------
X_numeric = X.select_dtypes(include=[np.number])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)

# ----------------------
# 6. Train/test split
# ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ----------------------
# 7. Train Random Forest
# ----------------------
rf = RandomForestClassifier(
    n_estimators=200, random_state=42, class_weight="balanced"
)
rf.fit(X_train, y_train)

# ----------------------
# 8. Evaluation
# ----------------------
y_pred = rf.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ----------------------
# 9. Feature Importances
# ----------------------
importances = pd.Series(rf.feature_importances_, index=X_numeric.columns)
top_features = importances.sort_values(ascending=False).head(10)

print("\nTop 10 Features by Importance:")
print(top_features)
