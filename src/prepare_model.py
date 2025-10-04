#!/usr/bin/env python3
"""Script to train a model and prepare data for the FastAPI server."""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def prepare_data():
    """Prepare the NASA exoplanet data for training."""
    print("Loading NASA exoplanet data...")
    
    # Read the CSV file, skipping comment lines
    df = pd.read_csv('nasa_exoplanet_cumulative.csv', comment='#')
    
    print(f"Loaded {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Create a binary label based on koi_disposition
    # CONFIRMED = 1 (planet), everything else = 0 (false positive/candidate)
    df['label'] = (df['koi_disposition'] == 'CONFIRMED').astype(int)
    
    print(f"Label distribution:")
    print(df['label'].value_counts())
    print(f"Disposition distribution:")
    print(df['koi_disposition'].value_counts())
    
    # Select the most important features for exoplanet classification
    # Focus on features that are most predictive and have good coverage
    feature_columns = [
        'koi_period',           # Orbital period
        'koi_depth',           # Transit depth
        'koi_duration',        # Transit duration
        'koi_impact',          # Impact parameter
        'koi_model_snr',       # Signal-to-noise ratio
        'koi_steff',           # Stellar temperature
        'koi_slogg',           # Stellar surface gravity
        'koi_srad',            # Stellar radius
        'koi_kepmag',          # Kepler magnitude
        'ra', 'dec'            # Coordinates
    ]
    
    print(f"Selected features: {feature_columns}")
    
    # Check which features exist in the dataset
    available_features = [col for col in feature_columns if col in df.columns]
    missing_features = [col for col in feature_columns if col not in df.columns]
    
    if missing_features:
        print(f"Missing features: {missing_features}")
    
    print(f"Using features: {available_features}")
    
    # Remove rows where ALL selected features are missing
    df_clean = df.dropna(subset=available_features, how='all')
    print(f"After removing rows with all features missing: {len(df_clean)} records")
    
    # Prepare features and labels
    X = df_clean[available_features].copy()
    y = df_clean['label'].copy()
    
    # Fill missing values with median for numerical columns
    for col in X.columns:
        if X[col].dtype in ['float64', 'int64']:
            median_val = X[col].median()
            X[col] = X[col].fillna(median_val)
        else:
            X[col] = X[col].fillna(0)
    
    print(f"Final dataset shape: {X.shape}")
    print(f"Missing values after filling: {X.isnull().sum().sum()}")
    
    return X, y, df_clean

def train_model():
    """Train the RandomForest model."""
    print("Preparing data...")
    X, y, df_clean = prepare_data()
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training XGBoost model...")
    clf = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    model_path = 'models/baseline.pkl'
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")
    
    # Save feature names for reference
    feature_names_path = 'models/feature_names.txt'
    with open(feature_names_path, 'w') as f:
        for feature in X.columns:
            f.write(f"{feature}\n")
    print(f"Feature names saved to {feature_names_path}")
    
    return clf, X.columns.tolist()

if __name__ == "__main__":
    model, feature_names = train_model()
    print(f"Model trained with {len(feature_names)} features")
    print("Ready to start FastAPI server!")
