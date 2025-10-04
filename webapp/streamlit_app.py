"""Minimal Streamlit app to load a saved model and make predictions."""
import streamlit as st
import pandas as pd
import joblib

st.title('Exoplanet Classifier - Demo')

model_path = st.sidebar.text_input('Model path', 'models/baseline.pkl')

if st.sidebar.button('Load model'):
	clf = joblib.load(model_path)
	st.sidebar.success('Model loaded')

uploaded = st.file_uploader('Upload CSV with features', type='csv')

if uploaded:
    df = pd.read_csv(uploaded)
    st.write('Preview')
    st.dataframe(df.head())
    
if st.button('Predict'):
    X = df
    preds = clf.predict(X)
    df['prediction'] = preds
    st.write(df[['prediction']].head())
