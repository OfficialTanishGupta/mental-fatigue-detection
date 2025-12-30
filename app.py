import streamlit as st
import joblib
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Mental Fatigue Detector",
    page_icon="🧠",
    layout="centered"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ Load Model & Files ------------------
model = joblib.load(os.path.join(BASE_DIR, "model", "fatigue_model.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "model", "label_encoder.pkl"))

evaluation_path = os.path.join(BASE_DIR, "model", "evaluation_report.txt")
feature_path = os.path.join(BASE_DIR, "model", "feature_importance.csv")

# ------------------ Title ------------------
st.title("🧠 Mental Fatigue Detection System")
st.write("An ML-powered system with model evaluation and insights.")

# ------------------ Sidebar ------------------
st.sidebar.header("📊 Navigation")
option = st.sidebar.radio(
    "Select View",
    ["Prediction", "Model Evaluation"]
)

# ------------------ PREDICTION VIEW ------------------
if option == "Prediction":
    with st.expander("📥 Enter Daily Habits"):
        sleep = st.slider("Sleep Hours", 4, 9, 7)
        screen = st.slider("Screen Time (hrs)", 1, 12, 5)
        work = st.slider("Work/Study Hours", 1, 12, 6)
        breaks = st.slider("Breaks per day", 1, 10, 4)
        activity = st.slider("Physical Activity (mins)", 0, 60, 30)
        caffeine = st.slider("Caffeine Intake (cups)", 0, 5, 2)

    if st.button("🔍 Predict Fatigue"):
        input_data = np.array([[sleep, screen, work, breaks, activity, caffeine]])

        prediction = model.predict(input_data)
        probabilities = model.predict_proba(input_data)[0]

        fatigue_label = encoder.inverse_transform(prediction)[0]
        fatigue_score = int(max(probabilities) * 100)

        st.metric("Fatigue Score", f"{fatigue_score} / 100")

        if fatigue_label == "High":
            st.error("Fatigue Level: HIGH")
        elif fatigue_label == "Medium":
            st.warning("Fatigue Level: MEDIUM")
        else:
            st.success("Fatigue Level: LOW")

# ------------------ MODEL EVALUATION VIEW ------------------
if option == "Model Evaluation":

    st.subheader("📈 Model Accuracy & Report")

    # Read evaluation report
    with open(evaluation_path, "r") as f:
        st.text(f.read())

    # ------------------ Confusion Matrix ------------------
    st.subheader("🔢 Confusion Matrix")

    # Load dataset to recreate test split
    data = pd.read_csv(os.path.join(BASE_DIR, "data", "fatigue_data.csv"))
    X = data.drop("fatigue_level", axis=1)
    y = encoder.transform(data["fatigue_level"])

    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)

    fig, ax = plt.subplots()
    ax.imshow(cm)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks(range(len(encoder.classes_)))
    ax.set_yticks(range(len(encoder.classes_)))
    ax.set_xticklabels(encoder.classes_)
    ax.set_yticklabels(encoder.classes_)

    for i in range(len(cm)):
        for j in range(len(cm)):
            ax.text(j, i, cm[i, j], ha="center", va="center")

    st.pyplot(fig)

    # ------------------ Feature Importance ------------------
    st.subheader("📊 Feature Importance")

    feature_df = pd.read_csv(feature_path)
    feature_df = feature_df.sort_values(by="importance", ascending=True)

    fig2, ax2 = plt.subplots()
    ax2.barh(feature_df["feature"], feature_df["importance"])
    ax2.set_xlabel("Importance Score")
    ax2.set_title("Feature Importance")

    st.pyplot(fig2)
