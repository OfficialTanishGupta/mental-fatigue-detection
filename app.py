import streamlit as st
import joblib
import numpy as np
import os

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Mental Fatigue Detector",
    page_icon="🧠",
    layout="centered"
)

# ------------------ Load Model Safely ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model", "fatigue_model.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "model", "label_encoder.pkl"))

# ------------------ Title ------------------
st.title("🧠 Mental Fatigue Detection System")
st.write("Predict your mental fatigue level based on daily habits.")

# ------------------ Inputs ------------------
with st.expander("📊 Enter Your Daily Habits"):
    sleep = st.slider("Sleep Hours", 4, 9, 7)
    screen = st.slider("Screen Time (hrs/day)", 1, 12, 5)
    work = st.slider("Work/Study Hours", 1, 12, 6)
    breaks = st.slider("Breaks per day", 1, 10, 4)
    activity = st.slider("Physical Activity (mins)", 0, 60, 30)
    caffeine = st.slider("Caffeine Intake (cups)", 0, 5, 2)

# ------------------ Prediction ------------------
if st.button("🔍 Predict Fatigue Level"):
    input_data = np.array([[sleep, screen, work, breaks, activity, caffeine]])

    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)[0]

    fatigue_label = encoder.inverse_transform(prediction)[0]
    fatigue_score = int(max(probabilities) * 100)

    # ------------------ Results ------------------
    st.metric("Fatigue Score", f"{fatigue_score} / 100")

    if fatigue_label == "High":
        st.error("Fatigue Level: HIGH")
    elif fatigue_label == "Medium":
        st.warning("Fatigue Level: MEDIUM")
    else:
        st.success("Fatigue Level: LOW")

    # ------------------ Analysis ------------------
    st.subheader("🔍 Analysis")
    if sleep < 6:
        st.write("• Low sleep duration may increase fatigue.")
    if screen > 7:
        st.write("• High screen time contributes to mental strain.")
    if breaks < 3:
        st.write("• Taking fewer breaks reduces recovery time.")
    if activity < 20:
        st.write("• Low physical activity affects mental freshness.")

    # ------------------ Recommendations ------------------
    st.subheader("💡 Recommendations")

    if fatigue_label == "High":
        st.write("✔ Aim for 7–8 hours of quality sleep")
        st.write("✔ Reduce screen exposure, especially before bedtime")
        st.write("✔ Take frequent short breaks during work")
        st.write("✔ Add light physical activity like walking or stretching")

    elif fatigue_label == "Medium":
        st.write("✔ Maintain consistent sleep routine")
        st.write("✔ Balance work with regular breaks")
        st.write("✔ Limit caffeine intake late in the day")

    else:
        st.write("✔ Keep maintaining healthy daily habits")
        st.write("✔ Stay consistent with sleep and activity levels")
