import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def load_and_prepare_data():
    """Load and prepare the NASA exoplanet data"""
    # Load the NASA exoplanet data
    df = pd.read_csv('nasa_exoplanet_cumulative.csv')
    
    print(f"Loaded {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    
    # Create binary target: CONFIRMED = 1, others = 0
    df['is_exoplanet'] = (df['koi_disposition'] == 'CONFIRMED').astype(int)
    
    print(f"Exoplanets: {df['is_exoplanet'].sum()}")
    print(f"Non-exoplanets: {len(df) - df['is_exoplanet'].sum()}")
    
    return df

def engineer_features(df):
    """Create meaningful features for exoplanet detection"""
    features_df = pd.DataFrame()
    
    # Basic transit features
    features_df['koi_period'] = df['koi_period']
    features_df['koi_depth'] = df['koi_depth']
    features_df['koi_duration'] = df['koi_duration']
    features_df['koi_impact'] = df['koi_impact']
    features_df['koi_model_snr'] = df['koi_model_snr']
    
    # Star properties
    features_df['koi_steff'] = df['koi_steff']
    features_df['koi_slogg'] = df['koi_slogg']
    features_df['koi_srad'] = df['koi_srad']
    features_df['koi_kepmag'] = df['koi_kepmag']
    
    # Derived features
    features_df['transit_depth_log'] = np.log10(features_df['koi_depth'] + 1e-10)
    features_df['period_log'] = np.log10(features_df['koi_period'] + 1e-10)
    features_df['duration_hours'] = features_df['koi_duration'] * 24
    
    # Transit geometry features
    features_df['transit_speed'] = features_df['koi_depth'] / features_df['koi_duration']
    features_df['period_duration_ratio'] = features_df['koi_period'] / features_df['koi_duration']
    
    # Star classification features
    features_df['star_type'] = pd.cut(features_df['koi_steff'], 
                                    bins=[0, 4000, 5000, 6000, 7000, 8000, 10000], 
                                    labels=['M', 'K', 'G', 'F', 'A', 'B'])
    features_df['star_type_encoded'] = features_df['star_type'].astype('category').cat.codes
    
    # Signal quality features
    features_df['snr_depth_ratio'] = features_df['koi_model_snr'] / (features_df['koi_depth'] + 1e-10)
    features_df['transit_quality'] = features_df['koi_model_snr'] * features_df['koi_depth']

    # Remove rows with missing critical features
    critical_features = ['koi_period', 'koi_depth', 'koi_duration', 'koi_steff']
    features_df = features_df.dropna(subset=critical_features)

    # Remove categorical column before training/scaling
    if 'star_type' in features_df.columns:
        features_df = features_df.drop(columns=['star_type'])

    # Fill remaining NaN values only in numeric columns
    features_df = features_df.fillna(features_df.select_dtypes(include=[np.number]).median())

    return features_df

def train_xgboost_model(features_df, target):
    """Train XGBoost model with proper parameters"""
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        features_df, target, test_size=0.2, random_state=42, stratify=target
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # XGBoost parameters optimized for exoplanet detection
    xgb_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 0.1,
        'reg_lambda': 1.0,
        'random_state': 42
    }
    
    # Train the model
    model = xgb.XGBClassifier(**xgb_params)
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Print results
    print("\nModel Performance:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features_df.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return model, scaler, feature_importance

def main():
    """Main training pipeline"""
    print("Loading NASA exoplanet data...")
    df = load_and_prepare_data()
    
    print("\nEngineering features...")
    features_df = engineer_features(df)
    target = df.loc[features_df.index, 'is_exoplanet']
    
    print(f"\nFeature matrix shape: {features_df.shape}")
    print(f"Target distribution: {target.value_counts().to_dict()}")
    
    print("\nTraining XGBoost model...")
    model, scaler, feature_importance = train_xgboost_model(features_df, target)
    
    # Save the model and scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/baseline.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(feature_importance, 'models/feature_importance.pkl')
    
    # Save feature names for the API
    with open('models/feature_names.txt', 'w') as f:
        for feature in features_df.columns:
            f.write(f"{feature}\n")
    
    print("\nModel saved successfully!")
    print("Files created:")
    print("- models/baseline.pkl")
    print("- models/scaler.pkl") 
    print("- models/feature_importance.pkl")
    print("- models/feature_names.txt")

if __name__ == "__main__":
    main()
