import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

data = pd.read_csv("data.csv")
data['diagnosis'] = data['diagnosis'].map({'B': 0, 'M': 1})

X = data[[
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
    'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se',
    'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
    'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst',
    'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]]
y = data['diagnosis']

imputer = SimpleImputer(strategy='mean')
imputer.fit(X)

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)
model = KNeighborsClassifier(n_neighbors=11)
model.fit(train_X, train_y)

st.markdown("""
    <style>
        .title-center {
            text-align: center;
            padding: 1rem;
        }
        .stButton>button {
            display: block;
            width: 100%;
            text-align: center;
            margin: 1rem auto;
        }
        div[data-testid="stHorizontalBlock"] > div {
            display: flex;
            align-items: stretch;
        }
        div.row-widget.stRadio > div {
            flex-direction: row;
            justify-content: center;
        }
        div[data-baseweb="base-input"] {
            justify-content: center;
        }
        div.stSuccess, div.stError {
            text-align: center;
        }
        [data-testid="stMarkdownContainer"] {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-center">Breast Cancer Classifier</h1>', unsafe_allow_html=True)

fields = [
    ("radius_mean", "Tumor Radius (Average)"),
    ("texture_mean", "Tumor Texture (Average)"),
    ("perimeter_mean", "Tumor Perimeter (Average)"),
    ("area_mean", "Tumor Area (Average)"),
    ("smoothness_mean", "Tumor Smoothness (Average)"),
    ("compactness_mean", "Tumor Compactness (Average)"),
    ("concavity_mean", "Tumor Concavity (Average)"),
    ("concave points_mean", "Concave Indentations (Average)"),
    ("symmetry_mean", "Tumor Symmetry (Average)"),
    ("fractal_dimension_mean", "Tumor Complexity (Average)"),
    ("radius_se", "Tumor Radius Variation"),
    ("texture_se", "Tumor Texture Variation"),
    ("perimeter_se", "Tumor Perimeter Variation"),
    ("area_se", "Tumor Area Variation"),
    ("smoothness_se", "Tumor Smoothness Variation"),
    ("compactness_se", "Tumor Compactness Variation"),
    ("concavity_se", "Tumor Concavity Variation"),
    ("concave points_se", "Concave Indentations Variation"),
    ("symmetry_se", "Tumor Symmetry Variation"),
    ("fractal_dimension_se", "Tumor Complexity Variation"),
    ("radius_worst", "Tumor Radius (Largest Observed)"),
    ("texture_worst", "Tumor Texture (Largest Observed)"),
    ("perimeter_worst", "Tumor Perimeter (Largest Observed)"),
    ("area_worst", "Tumor Area (Largest Observed)"),
    ("smoothness_worst", "Tumor Smoothness (Largest Observed)"),
    ("compactness_worst", "Tumor Compactness (Largest Observed)"),
    ("concavity_worst", "Tumor Concavity (Largest Observed)"),
    ("concave points_worst", "Concave Indentations (Largest Observed)"),
    ("symmetry_worst", "Tumor Symmetry (Largest Observed)"),
    ("fractal_dimension_worst", "Tumor Complexity (Largest Observed)")
]

with st.container():
    input_data = {}
    cols = st.columns(4)
    for i, (field, label) in enumerate(fields):
        col = cols[i % 4]
        with col:
            input_data[field] = st.number_input(label, min_value=0.01, step=0.01)

    st.write("")
    
    if st.button("Predict Cancer Cell"):
        input_df = pd.DataFrame([{col: input_data.get(col, float('nan')) for col in X.columns}])
        imputed_data = imputer.transform(input_df)
        prediction = model.predict(imputed_data)[0]
        result = "Malignant" if prediction == 1 else "Benign"
        if result == "Benign":
            st.success(f"Prediction: {result}")
        else:
            st.error(f"Prediction: {result}")