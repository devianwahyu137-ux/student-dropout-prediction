import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Jaya Jaya Institut - Prediksi Dropout", layout="wide", page_icon="🎓")

# Menampilkan Logo
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=150)

st.title("Sistem Prediksi Risiko Dropout Mahasiswa")
st.markdown("---")

# Mappings untuk data kategorikal agar lebih mudah dipahami User (UI -> Model)
marital_map = {'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto Union': 5, 'Legally Separated': 6}
course_map = {
    'Biofuel Production Tech': 33, 'Animation & Multimedia': 171, 'Social Service (Evening)': 8014,
    'Agronomy': 9003, 'Communication Design': 9070, 'Veterinary Nursing': 9085, 'Informatics Eng': 9119,
    'Equinculture': 9130, 'Management': 9147, 'Social Service': 9238, 'Tourism': 9254,
    'Nursing': 9500, 'Oral Hygiene': 9556, 'Advertising & Marketing': 9670,
    'Journalism & Comm': 9773, 'Basic Education': 9853, 'Management (Evening)': 9991
}
attendance_map = {'Daytime': 1, 'Evening': 0}
tuition_map = {'Paid / Up to date': 1, 'Unpaid / Arrears': 0}
gender_map = {'Male': 1, 'Female': 0}
scholarship_map = {'Yes': 1, 'No': 0}
displaced_map = {'Yes': 1, 'No': 0}
special_needs_map = {'Yes': 1, 'No': 0}
debtor_map = {'Yes': 1, 'No': 0}
international_map = {'Yes': 1, 'No': 0}

# Load the model
@st.cache_resource
def load_model():
    if os.path.exists("model/model.joblib"):
        return joblib.load("model/model.joblib")
    elif os.path.exists("model.joblib"):
        return joblib.load("model.joblib")
    else:
        st.error("Model file not found!")
        return None

model = load_model()

@st.cache_data
def get_default_data():
    df = pd.read_csv("clean_data.csv")
    X = df.drop(columns=['Status', 'Dropout_Flag'], errors='ignore')
    return X.iloc[0:1], X.columns.tolist()

default_df, columns = get_default_data()

# Membuat Tab
tab1, tab2 = st.tabs(["🔮 Prediksi Mahasiswa", "📖 Panduan Penggunaan"])

with tab2:
    st.header("Panduan Penggunaan Aplikasi")
    st.markdown("""
    **Sistem Prediksi Risiko Dropout** ini dibuat untuk membantu Jaya Jaya Institut mendeteksi mahasiswa yang berisiko putus kuliah secara dini.
    
    ### Cara Menggunakan:
    Terdapat 2 mode prediksi yang bisa Anda pilih di Tab **Prediksi Mahasiswa**:
    1. **Input Manual (Satu per Satu):** 
       Gunakan mode ini jika Anda hanya ingin mengecek satu mahasiswa. Masukkan data demografi, akademik, dan ekonomi mahasiswa tersebut menggunakan *slider* dan *dropdown* yang telah disediakan. Setelah selesai, klik tombol **Prediksi Risiko Dropout**.
    2. **Upload File (Massal):**
       Gunakan mode ini jika Anda memiliki data puluhan atau ratusan mahasiswa sekaligus (misal data satu angkatan) dalam format CSV. 
       - Siapkan file CSV yang memiliki kolom-kolom yang sama persis dengan dataset awal.
       - Upload file tersebut, dan sistem akan otomatis memprediksi semuanya dalam hitungan detik.
       - Anda bisa melihat hasilnya dalam bentuk tabel dan mengunduhnya.
       
    ### Interpretasi Hasil:
    - 🔴 **Berisiko Tinggi (Dropout):** Mahasiswa sangat berisiko untuk putus kuliah. Disarankan untuk segera dipanggil oleh dosen pembimbing.
    - 🟢 **Aman (Tidak Berisiko):** Mahasiswa memiliki peluang besar untuk lulus atau bertahan.
    """)

with tab1:
    mode = st.radio("Pilih Mode Prediksi:", ["Input Manual (1 Mahasiswa)", "Upload File CSV (Prediksi Massal)"])
    
    if mode == "Input Manual (1 Mahasiswa)":
        st.subheader("Masukkan Data Mahasiswa")
        
        col1, col2 = st.columns(2)
        
        user_input = {}
        
        with col1:
            st.markdown("#### 👤 Data Demografi & Status")
            marital = st.selectbox("Marital Status", list(marital_map.keys()))
            course = st.selectbox("Course (Jurusan)", list(course_map.keys()))
            attendance = st.selectbox("Daytime/Evening Attendance", list(attendance_map.keys()))
            gender = st.selectbox("Gender", list(gender_map.keys()))
            age = st.slider("Age at enrollment", min_value=16, max_value=80, value=20)
            
            st.markdown("#### 💰 Data Finansial")
            tuition = st.selectbox("Tuition fees up to date", list(tuition_map.keys()))
            scholarship = st.selectbox("Scholarship holder", list(scholarship_map.keys()))
            debtor = st.selectbox("Debtor", list(debtor_map.keys()))
            
        with col2:
            st.markdown("#### 📚 Performa Akademik (Semester 1 & 2)")
            # Menggunakan slider untuk input numerik akademik
            user_input['Curricular_units_1st_sem_enrolled'] = st.slider("SKS Semester 1 (Enrolled)", 0, 30, 6)
            user_input['Curricular_units_1st_sem_approved'] = st.slider("SKS Semester 1 (Approved/Lulus)", 0, 30, 5)
            user_input['Curricular_units_1st_sem_grade'] = st.slider("Nilai Rata-rata Semester 1", 0.0, 20.0, 12.0, step=0.1)
            
            user_input['Curricular_units_2nd_sem_enrolled'] = st.slider("SKS Semester 2 (Enrolled)", 0, 30, 6)
            user_input['Curricular_units_2nd_sem_approved'] = st.slider("SKS Semester 2 (Approved/Lulus)", 0, 30, 5)
            user_input['Curricular_units_2nd_sem_grade'] = st.slider("Nilai Rata-rata Semester 2", 0.0, 20.0, 12.0, step=0.1)

        # Sisanya menggunakan default value dari dataset agar user tidak terlalu banyak mengisi
        for feature in columns:
            if feature not in user_input and feature not in ['Marital_status', 'Course', 'Daytime_evening_attendance', 'Gender', 'Tuition_fees_up_to_date', 'Scholarship_holder', 'Age_at_enrollment', 'Debtor']:
                user_input[feature] = float(default_df[feature].values[0])
                
        # Update dengan mapped values
        user_input['Marital_status'] = marital_map[marital]
        user_input['Course'] = course_map[course]
        user_input['Daytime_evening_attendance'] = attendance_map[attendance]
        user_input['Gender'] = gender_map[gender]
        user_input['Tuition_fees_up_to_date'] = tuition_map[tuition]
        user_input['Scholarship_holder'] = scholarship_map[scholarship]
        user_input['Age_at_enrollment'] = age
        user_input['Debtor'] = debtor_map[debtor]
        
        input_df = pd.DataFrame([user_input])
        input_df = input_df[columns] # Reorder to match model
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔮 Prediksi Risiko Dropout", use_container_width=True):
            if model:
                prediction = model.predict(input_df)[0]
                if prediction == 1:
                    st.error("⚠️ MAHASISWA BERISIKO TINGGI UNTUK DROPOUT")
                    st.write("Segera lakukan intervensi akademik atau berikan bimbingan konseling.")
                else:
                    st.success("✅ MAHASISWA AMAN (Tidak berisiko dropout)")
            
    else:
        st.subheader("Upload Data CSV untuk Prediksi Massal")
        st.write("Silakan upload file CSV yang berisi data mahasiswa. Format kolom harus sama dengan dataset asli.")
        uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
        
        if uploaded_file is not None:
            try:
                batch_data = pd.read_csv(uploaded_file, sep=';')
                # Check if it has the right columns (or try comma separator)
                if len(batch_data.columns) < 10:
                    batch_data = pd.read_csv(uploaded_file, sep=',')
                    
                st.write(f"Berhasil memuat {len(batch_data)} baris data mahasiswa.")
                
                if st.button("Jalankan Prediksi Massal"):
                    with st.spinner("Memproses prediksi..."):
                        # Ensure we only pass required columns to model
                        X_batch = batch_data.copy()
                        if 'Status' in X_batch.columns:
                            X_batch = X_batch.drop(columns=['Status'])
                        if 'Dropout_Flag' in X_batch.columns:
                            X_batch = X_batch.drop(columns=['Dropout_Flag'])
                            
                        # Fill missing columns with defaults if any
                        for col in columns:
                            if col not in X_batch.columns:
                                X_batch[col] = float(default_df[col].values[0])
                        
                        # Reorder
                        X_batch = X_batch[columns]
                        
                        predictions = model.predict(X_batch)
                        batch_data['Prediksi_Dropout'] = ["🔴 BERISIKO" if p == 1 else "🟢 AMAN" for p in predictions]
                        
                        st.success("Prediksi selesai!")
                        st.dataframe(batch_data[['Prediksi_Dropout'] + [c for c in batch_data.columns if c != 'Prediksi_Dropout']])
                        
                        # Download button
                        csv_output = batch_data.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Download Hasil Prediksi (CSV)",
                            data=csv_output,
                            file_name="hasil_prediksi_massal.csv",
                            mime="text/csv",
                        )
            except Exception as e:
                st.error(f"Terjadi kesalahan saat membaca file: {str(e)}")

st.markdown("---")
st.write("Dashboard Monitoring dapat diakses melalui Looker Studio (Lihat README.md)")
