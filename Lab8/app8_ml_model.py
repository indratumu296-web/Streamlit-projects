from pathlib import Path

import numpy as np
import joblib
import streamlit as st

MODEL_PATH = Path(__file__).with_name("model.pkl")

st.title("Iris Flower Prediction")

if not MODEL_PATH.exists():
    st.error("Model file not found. Run `train_iris.py` to generate `model.pkl`.")
    st.stop()

model = joblib.load(MODEL_PATH)
classes = ["Setosa", "Versicolor", "Virginica"]

with st.form("prediction_form"):
    sepal_length = st.slider("Sepal Length", 4.0, 8.0, 5.1)
    sepal_width = st.slider("Sepal Width", 2.0, 4.5, 3.5)
    petal_length = st.slider("Petal Length", 1.0, 7.0, 1.4)
    petal_width = st.slider("Petal Width", 0.1, 2.5, 0.2)
    submit = st.form_submit_button("Predict")

if submit:
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]], dtype=float)
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities) * 100

    st.success(f"Prediction: **{classes[prediction]}**")
    st.metric("Confidence", f"{confidence:.1f}%")