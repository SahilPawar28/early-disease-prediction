"""
🩺 Early Disease Prediction System — Streamlit App
====================================================
Run locally:
    pip install streamlit joblib scikit-learn xgboost lightgbm imbalanced-learn shap
    streamlit run streamlit_app.py

Or deploy to Streamlit Cloud:
    1. Push this file + disease_prediction_model/ folder to GitHub
    2. Go to share.streamlit.io → New app → Select your repo
"""

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Disease Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1565C0, #0D47A1);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #F8F9FA;
        border-left: 5px solid #1565C0;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .healthy   { background: #E8F5E9; border: 2px solid #4CAF50; color: #1B5E20; }
    .disease   { background: #FFF3E0; border: 2px solid #FF9800; color: #E65100; }
    .critical  { background: #FFEBEE; border: 2px solid #F44336; color: #B71C1C; }
    .prob-bar  { height: 12px; border-radius: 6px; margin: 4px 0; }
    .stSlider > div > div { background: #E3F2FD; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load Model Artifacts
# ─────────────────────────────────────────────
MODEL_DIR = "disease_prediction_model"

@st.cache_resource
def load_artifacts():
    model   = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    scaler  = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    le      = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
    with open(os.path.join(MODEL_DIR, "feature_names.json")) as f:
        features = json.load(f)
    return model, scaler, le, features

try:
    model, scaler, le, feature_names = load_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"⚠️ Could not load model: {e}\n\nMake sure `disease_prediction_model/` folder is in the same directory as this script.")

# ─────────────────────────────────────────────
# Disease Info
# ─────────────────────────────────────────────
DISEASE_INFO = {
    "Diabetes": {
        "emoji": "🍬", "color": "#FF9800",
        "risk": "High",
        "description": "Chronic condition affecting blood sugar regulation.",
        "tips": ["Monitor blood glucose daily", "Low-carb, balanced diet", "Regular aerobic exercise", "HbA1c check every 3 months"],
        "card_class": "disease"
    },
    "Heart Disease": {
        "emoji": "❤️", "color": "#F44336",
        "risk": "Critical",
        "description": "Cardiovascular condition affecting heart function.",
        "tips": ["Low-sodium diet", "Cardio exercise 30 min/day", "Avoid smoking & alcohol", "Regular ECG & BP monitoring"],
        "card_class": "critical"
    },
    "Anemia": {
        "emoji": "🩸", "color": "#9C27B0",
        "risk": "Moderate",
        "description": "Low red blood cell count or hemoglobin levels.",
        "tips": ["Iron-rich foods (spinach, red meat)", "Vitamin C supplementation", "Avoid tea/coffee with meals", "Regular CBC blood test"],
        "card_class": "disease"
    },
    "Thalassemia": {
        "emoji": "🧬", "color": "#3F51B5",
        "risk": "High",
        "description": "Inherited blood disorder affecting hemoglobin production.",
        "tips": ["Regular blood transfusions if needed", "Folic acid supplements", "Genetic counseling", "Avoid iron supplements unless prescribed"],
        "card_class": "critical"
    },
    "Thrombocytopenia": {
        "emoji": "💊", "color": "#00BCD4",
        "risk": "Moderate",
        "description": "Abnormally low platelet count in blood.",
        "tips": ["Avoid blood thinners (aspirin, ibuprofen)", "Protect from injury/cuts", "Report unusual bruising immediately", "Regular platelet count monitoring"],
        "card_class": "disease"
    },
    "Healthy": {
        "emoji": "✅", "color": "#4CAF50",
        "risk": "Low",
        "description": "No significant disease markers detected.",
        "tips": ["Annual health check-ups", "Maintain balanced diet", "Regular exercise (150 min/week)", "Adequate sleep (7-9 hours)"],
        "card_class": "healthy"
    }
}

# ─────────────────────────────────────────────
# Sidebar — About & Instructions
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/medical-doctor.png", width=80)
    st.title("🩺 Disease Predictor")
    st.markdown("---")
    st.markdown("""
    **How to Use:**
    1. Enter patient biomarker values
    2. Click **Predict Disease**
    3. Review results & recommendations

    **Conditions Detected:**
    - 🍬 Diabetes
    - ❤️ Heart Disease
    - 🩸 Anemia
    - 🧬 Thalassemia
    - 💊 Thrombocytopenia
    - ✅ Healthy

    ---
    ⚠️ *For educational purposes only. Always consult a licensed physician.*
    """)
    st.markdown("---")

    if model_loaded:
        st.success("✅ Model loaded successfully")
        st.metric("Features", len(feature_names))
        st.metric("Classes", len(le.classes_))
    else:
        st.error("❌ Model not loaded")

# ─────────────────────────────────────────────
# Main Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🩺 ML-Based Early Disease Prediction System</h1>
    <p>Enter blood sample biomarker values to predict potential health conditions</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.stop()

# ─────────────────────────────────────────────
# Input Section — Organized by Category
# ─────────────────────────────────────────────
st.subheader("📋 Patient Biomarker Input")
st.info("All values are normalized (0.0 – 1.0). Enter values from the patient's blood report.")

feature_groups = {
    "🔴 Blood Cell Markers": [
        "Hemoglobin", "Platelets", "White Blood Cells", "Red Blood Cells",
        "Hematocrit", "Mean Corpuscular Volume",
        "Mean Corpuscular Hemoglobin", "Mean Corpuscular Hemoglobin Concentration"
    ],
    "🍬 Metabolic Markers": [
        "Glucose", "Insulin", "BMI", "HbA1c", "Triglycerides"
    ],
    "❤️ Cardiovascular Markers": [
        "Cholesterol", "LDL Cholesterol", "HDL Cholesterol",
        "Systolic Blood Pressure", "Diastolic Blood Pressure",
        "Heart Rate", "Troponin"
    ],
    "🧪 Liver & Inflammation Markers": [
        "ALT", "AST", "Creatinine", "C-reactive Protein"
    ]
}

patient_values = {}

tabs = st.tabs(list(feature_groups.keys()))
for tab, (group_name, group_features) in zip(tabs, feature_groups.items()):
    with tab:
        cols = st.columns(2)
        for i, feat in enumerate(group_features):
            if feat in feature_names:
                with cols[i % 2]:
                    patient_values[feat] = st.slider(
                        feat,
                        min_value=0.0,
                        max_value=1.0,
                        value=0.5,
                        step=0.01,
                        key=f"slider_{feat}"
                    )

# Fill any missing features with 0.5
for feat in feature_names:
    if feat not in patient_values:
        patient_values[feat] = 0.5

# ─────────────────────────────────────────────
# Prediction
# ─────────────────────────────────────────────
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    predict_clicked = st.button("🔍 Predict Disease", use_container_width=True, type="primary")

if predict_clicked:
    # Build input array
    input_array = np.array([[patient_values[f] for f in feature_names]])
    input_scaled = scaler.transform(input_array)

    # Predict
    pred_encoded = model.predict(input_scaled)[0]
    pred_proba   = model.predict_proba(input_scaled)[0]
    pred_disease = le.inverse_transform([pred_encoded])[0]
    confidence   = pred_proba.max() * 100

    info = DISEASE_INFO.get(pred_disease, DISEASE_INFO["Healthy"])

    st.markdown("---")
    st.subheader("📊 Prediction Results")

    # ── Result Card ──
    st.markdown(f"""
    <div class="result-card {info['card_class']}">
        <div style="font-size: 3rem;">{info['emoji']}</div>
        <div style="font-size: 1.6rem; margin: 0.5rem 0;">Predicted: {pred_disease}</div>
        <div style="font-size: 1rem; opacity: 0.85;">{info['description']}</div>
        <div style="font-size: 1rem; margin-top: 0.5rem;">
            Confidence: <strong>{confidence:.1f}%</strong> &nbsp;|&nbsp; Risk Level: <strong>{info['risk']}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Columns: Probabilities + Recommendations ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📈 Class Probabilities")
        prob_df = pd.DataFrame({
            "Disease": le.classes_,
            "Probability": pred_proba
        }).sort_values("Probability", ascending=False)

        for _, row in prob_df.iterrows():
            pct = row["Probability"] * 100
            dis_info = DISEASE_INFO.get(row["Disease"], {})
            color = dis_info.get("color", "#607D8B")
            emoji = dis_info.get("emoji", "🔬")
            st.markdown(f"""
            <div style="margin: 6px 0;">
                <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                    <span>{emoji} {row['Disease']}</span>
                    <span><b>{pct:.1f}%</b></span>
                </div>
                <div style="background:#eee; border-radius:6px; height:10px;">
                    <div style="background:{color}; width:{pct}%; height:10px; border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("#### 💡 Health Recommendations")
        for tip in info["tips"]:
            st.markdown(f"✔️ {tip}")

        st.markdown("#### 🔬 Top Contributing Biomarkers")
        # Show highest input values as "risk factors"
        top_inputs = sorted(patient_values.items(), key=lambda x: x[1], reverse=True)[:5]
        for feat, val in top_inputs:
            level = "🔴 High" if val > 0.75 else ("🟡 Moderate" if val > 0.4 else "🟢 Low")
            st.markdown(f"- **{feat}**: {val:.2f} ({level})")

    # ── Matplotlib Probability Chart ──
    st.markdown("#### 📊 Probability Chart")
    fig, ax = plt.subplots(figsize=(8, 3.5))
    colors_list = [DISEASE_INFO.get(d, {}).get("color", "#607D8B") for d in prob_df["Disease"]]
    bars = ax.barh(prob_df["Disease"], prob_df["Probability"], color=colors_list, alpha=0.85)
    ax.set_xlabel("Probability")
    ax.set_title("Predicted Disease Probabilities", fontweight="bold")
    ax.set_xlim(0, 1.1)
    for bar, val in zip(bars, prob_df["Probability"]):
        ax.text(val + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val*100:.1f}%", va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Export Report ──
    st.markdown("---")
    st.subheader("📄 Export Patient Report")
    report_lines = [
        "EARLY DISEASE PREDICTION REPORT",
        "=" * 40,
        f"Predicted Disease:  {pred_disease}",
        f"Confidence:         {confidence:.1f}%",
        f"Risk Level:         {info['risk']}",
        "",
        "CLASS PROBABILITIES:",
    ]
    for _, row in prob_df.iterrows():
        report_lines.append(f"  {row['Disease']:<22} {row['Probability']*100:.2f}%")
    report_lines += ["", "PATIENT BIOMARKERS:", "-" * 40]
    for feat in feature_names:
        report_lines.append(f"  {feat:<40} {patient_values[feat]:.4f}")
    report_lines += ["", "RECOMMENDATIONS:"]
    for tip in info["tips"]:
        report_lines.append(f"  • {tip}")
    report_lines += ["", "⚠️ Disclaimer: For educational purposes only. Consult a licensed physician."]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Report (TXT)",
        data=report_text,
        file_name="disease_prediction_report.txt",
        mime="text/plain"
    )

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<center style="color: #888; font-size: 0.85rem;">
    🩺 Early Disease Prediction System &nbsp;|&nbsp;
    Built with Scikit-learn, XGBoost, LightGBM & Streamlit &nbsp;|&nbsp;
    ⚠️ Not a substitute for professional medical advice
</center>
""", unsafe_allow_html=True)
