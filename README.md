# Proyek Akhir: Deteksi Dini Mahasiswa Dropout (Jaya Jaya Institut)

## Business Understanding
Jaya Jaya Institut merupakan institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dengan reputasi yang baik. Namun, mereka menghadapi masalah tingginya angka mahasiswa yang tidak menyelesaikan pendidikan (dropout). Hal ini berdampak negatif pada performa dan reputasi institusi.

### Permasalahan Bisnis
Pihak institusi kesulitan mendeteksi mahasiswa yang berpotensi *dropout* secara dini, sehingga terlambat memberikan bimbingan atau intervensi.

### Cakupan Proyek
1. Melakukan analisis data performa mahasiswa untuk mengidentifikasi faktor utama penyebab *dropout*.
2. Membangun Business Dashboard untuk memantau performa mahasiswa secara keseluruhan.
3. Membangun model *Machine Learning* yang dapat memprediksi risiko *dropout* seorang mahasiswa.

## Persiapan
Sumber data: [Students Performance Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

Setup environment:
Proyek ini menggunakan **Python 3.9+**. Berikut langkah-langkah persiapannya:

1. Buat virtual environment dan aktifkan:
```bash
python3 -m venv venv
# Mac/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

2. Instal *dependencies*:
```bash
pip install -r requirements.txt
```

3. Menjalankan Dashboard:
Dashboard telah dibuat menggunakan **Looker Studio** dan dapat diakses langsung secara *online* tanpa proses *setup* lokal. Tautan tersedia di bagian bawah dokumen ini.

4. Menjalankan Prototype Machine Learning (Streamlit):
Aplikasi prediksi berbasis *web* dapat dijalankan di lokal dengan:
```bash
streamlit run app.py
```
Aplikasi ini juga telah di-deploy ke Streamlit Community Cloud (Link di bagian bawah).

## Business Dashboard
Dashboard telah dibuat menggunakan Looker Studio untuk memantau faktor-faktor penting yang memengaruhi performa mahasiswa. Metrik utama yang difokuskan meliputi riwayat akademik (SKS dan nilai) serta status finansial.

**Link Dashboard:** [Jaya Jaya Institut: Student Dropout Dashboard](https://datastudio.google.com/reporting/7d908a9b-87cd-4ed5-a8b7-dc5e02ba38c4)

## Machine Learning Prototype
Prototype machine learning di-*deploy* ke Streamlit Community Cloud dan memungkinkan staf untuk memprediksi apakah seorang mahasiswa berisiko *dropout*.

**Link Streamlit App:** `[Link Streamlit App Anda di sini]` (Mohon sesuaikan setelah mendeploy app)

## Conclusion
Berdasarkan analisis *Exploratory Data Analysis* (EDA) dan pemodelan Machine Learning (Random Forest dengan akurasi ~88%), dapat ditarik kesimpulan:

1. **Performa Akademik:** Faktor paling krusial adalah jumlah SKS (Curricular Units) yang disetujui (*approved*) dan nilai rata-rata pada semester ke-2 dan ke-1. Mahasiswa dengan persentase kelulusan mata kuliah yang rendah sangat berisiko *dropout*.
2. **Faktor Finansial:** Status tunggakan biaya SPP (*Tuition fees up to date*) juga sangat berpengaruh. Mahasiswa yang telat membayar SPP memiliki tingkat *dropout* yang jauh lebih tinggi.

## Rekomendasi Action Items
Berdasarkan kesimpulan di atas, pihak institusi (Jaya Jaya Institut) direkomendasikan melakukan langkah-langkah berikut:

1. **Sistem Peringatan Dini (Early Warning System) Akademik:**
   Gunakan model *machine learning* yang telah dibangun untuk menscan nilai UTS/UAS semester 1 dan 2 secara otomatis. Jika sistem mendeteksi risiko *dropout*, segera hubungi pembimbing akademik untuk melakukan sesi konseling dengan mahasiswa bersangkutan.
2. **Keringanan/Restrukturisasi Finansial:**
   Bagi mahasiswa yang terdeteksi menunggak SPP, jangan langsung dijatuhkan sanksi akademik berat. Tawarkan program beasiswa, cicilan pembayaran, atau pekerjaan paruh waktu di kampus untuk meringankan beban finansial mereka.
3. **Program Tutoring Tambahan:**
   Tingkatkan fasilitas bimbingan belajar gratis untuk mata kuliah dasar (semester 1 dan 2) yang memiliki tingkat ketidaklulusan tinggi, karena kegagalan di semester awal sangat memukul motivasi mahasiswa.
