import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Prediksi Dropout Mahasiswa", layout="wide")

st.title("Sistem Prediksi Risiko Dropout Mahasiswa")
st.write("Aplikasi ini memprediksi apakah seorang mahasiswa berisiko mengalami *dropout* atau tidak.")

# Load the model and data template
@st.cache_resource
def load_model():
    return joblib.load("model/model.joblib")

model = load_model()

# We need the exact columns expected by the model
# We can read the first row of clean_data to get column names and default values
@st.cache_data
def get_default_data():
    df = pd.read_csv("clean_data.csv")
    X = df.drop(columns=['Status', 'Dropout_Flag'])
    return X.iloc[0:1], X.columns.tolist()

default_df, columns = get_default_data()

st.sidebar.header("Input Data Mahasiswa")

# Create input fields for top features in the sidebar, and others in expander
top_features = [
    'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade',
    'Curricular_units_1st_sem_approved',
    'Tuition_fees_up_to_date',
    'Curricular_units_1st_sem_grade'
]

user_input = {}

for feature in top_features:
    user_input[feature] = st.sidebar.number_input(
        feature.replace('_', ' '),
        value=float(default_df[feature].values[0])
    )

with st.sidebar.expander("Fitur Lainnya (Lanjutan)"):
    for feature in columns:
        if feature not in top_features:
            user_input[feature] = st.number_input(
                feature.replace('_', ' '),
                value=float(default_df[feature].values[0])
            )

# Create a dataframe from user input
input_df = pd.DataFrame([user_input])
# Ensure column order matches the model
input_df = input_df[columns]

if st.button("Prediksi Risiko Dropout"):
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("⚠️ MAHASISWA BERISIKO TINGGI UNTUK DROPOUT")
        st.write("Disarankan untuk memberikan bimbingan khusus atau intervensi akademik secepatnya.")
    else:
        st.success("✅ MAHASISWA AMAN (Tidak berisiko dropout)")
        st.write("Teruskan pemantauan berkala untuk memastikan performa akademik tetap stabil.")
        
st.markdown("---")
st.write("Dashboard Monitoring dapat diakses melalui Looker Studio (Lihat README.md)")
