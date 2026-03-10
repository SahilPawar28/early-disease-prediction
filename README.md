# 🩺 ML-Based Early Disease Prediction System

A complete end-to-end machine learning pipeline that predicts diseases from blood sample biomarkers.

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `Early_Disease_Prediction_System.ipynb` | Full Google Colab notebook (train, evaluate, save model) |
| `streamlit_app.py` | Interactive web app for predictions |
| `blood_samples_dataset_test.csv` | Your input dataset |

---

## 🚀 PART A — Run in Google Colab

### Step 1: Open the Notebook
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click **File → Upload notebook** → select `Early_Disease_Prediction_System.ipynb`

### Step 2: Upload Dataset
- When the notebook prompts (Step 2 cell), upload `blood_samples_dataset_test.csv`

### Step 3: Run All Cells
- Click **Runtime → Run all** (`Ctrl+F9`)
- The notebook will train 7 models and automatically download `disease_prediction_model.zip`

### What the Notebook Does
```
✅ Data loading & cleaning
✅ EDA (charts: distribution, correlation heatmap, feature plots)
✅ SMOTE for class imbalance handling
✅ Trains 7 ML models:
   - Logistic Regression
   - K-Nearest Neighbors
   - Random Forest
   - Gradient Boosting
   - XGBoost
   - LightGBM
   - SVM
✅ Cross-validation (StratifiedKFold, k=5)
✅ Confusion matrix + classification report
✅ Feature importance plots
✅ SHAP explainability
✅ Ensemble Voting Classifier (top 3 models)
✅ Saves model artifacts (model.pkl, scaler.pkl, label_encoder.pkl)
✅ Interactive prediction widget (ipywidgets)
```

---

## 🌐 PART B — Run Streamlit Web App

### Prerequisites — Install dependencies
```bash
pip install streamlit scikit-learn xgboost lightgbm imbalanced-learn joblib shap matplotlib pandas numpy
```

### Step 1: Get the model files
After running the Colab notebook, extract `disease_prediction_model.zip`.
Your folder structure should look like:
```
your_project/
├── streamlit_app.py
├── disease_prediction_model/
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_names.json
```

### Step 2: Run locally
```bash
streamlit run streamlit_app.py
```
Opens at: http://localhost:8501

### Step 3: Deploy to Streamlit Cloud (Free!)
1. Push your project to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo + `streamlit_app.py`
4. Click **Deploy** — live URL in ~2 minutes!

---

## 🖥️ Streamlit App Features

| Feature | Detail |
|---------|--------|
| **Biomarker Input** | 24 sliders organized into 4 tabs (Blood Cell, Metabolic, Cardiovascular, Liver) |
| **Prediction Result** | Color-coded disease card with confidence % and risk level |
| **Probability Bars** | Visual breakdown of all 6 class probabilities |
| **Recommendations** | Disease-specific health tips |
| **Top Risk Factors** | Highlights highest biomarker values |
| **Chart** | Matplotlib probability bar chart |
| **Report Export** | Download full patient report as .txt |

---

## 🧬 Dataset Details

| Property | Value |
|----------|-------|
| Rows | 486 patients |
| Features | 24 blood biomarkers |
| Target | Disease (6 classes) |
| Missing values | None |
| Feature range | 0.0 – 1.0 (normalized) |

**Disease classes:**
- 🍬 Diabetes (294 samples)
- 🩸 Anemia (84 samples)
- 🧬 Thalassemia (48 samples)
- ❤️ Heart Disease (39 samples)
- 💊 Thrombocytopenia (16 samples)
- ✅ Healthy (5 samples)

**Biomarkers used:**
Glucose, Cholesterol, Hemoglobin, Platelets, White Blood Cells, Red Blood Cells, Hematocrit, MCV, MCH, MCHC, Insulin, BMI, Systolic BP, Diastolic BP, Triglycerides, HbA1c, LDL, HDL, ALT, AST, Heart Rate, Creatinine, Troponin, C-reactive Protein

---

## ⚠️ Disclaimer
This system is for **educational and research purposes only**. It is not a substitute for professional medical diagnosis. Always consult a licensed physician for medical advice.
