# Quick Start: Analisis Sentimen dalam 3 Menit

Panduan ini akan memandu Anda untuk melatih model dan melakukan prediksi sentimen secepat mungkin.

## 1. Jalankan Aplikasi

Gunakan skrip yang sudah disediakan untuk menjalankan backend dan frontend secara bersamaan.

**Di Linux/Mac:**
```bash
./run.sh
```

**Di Windows:**
```bat
run.bat
```

Setelah skrip berjalan, buka browser dan akses **[http://localhost:3000](http://localhost:3000)**.

## 2. Latih Model (Training)

1.  **Buka Tab "Training & Evaluasi"**.
2.  **Pilih Dataset**: Pilih dataset yang ingin digunakan, misalnya `GojekAppReviewV4.0.0-V4.9.3_Cleaned.csv`.
3.  **Pilih Kolom**:
    *   Kolom Teks (Fitur): `review`
    *   Kolom Label (Target): `sentiment`
4.  **Mulai Training**: Klik tombol **"Mulai Training & Evaluasi"**.

Tunggu beberapa saat hingga proses selesai. Anda akan melihat tabel perbandingan performa model dan visualisasi *confusion matrix*. Sistem akan secara otomatis menentukan dan menyimpan model terbaik.

## 3. Lakukan Prediksi

Setelah model selesai dilatih:

1.  **Buka Tab "Prediksi Teks"**.
2.  **Masukkan Teks**: Ketik sebuah kalimat di kotak teks. Contoh:
    *   `"Aplikasinya keren dan sangat membantu saya sehari-hari."`
    *   `"Sangat lambat dan sering error, mengecewakan."`
3.  **Prediksi**: Klik tombol **"Prediksi Sentimen"**.

Hasil prediksi (positif, negatif, atau netral) dan probabilitasnya akan muncul di bawah tombol.

---

**Selesai!** Anda telah berhasil melatih model klasifikasi sentimen dan menggunakannya untuk prediksi.

### Ingin Tahu Lebih Lanjut?

- **Tab Preprocessing**: Lihat bagaimana teks dibersihkan sebelum diproses.
- **File `sentiment_analysis_pipeline.ipynb`**: Pelajari setiap langkah alur kerja machine learning secara mendalam, dari data mentah hingga prediksi.
- **File `README.md`**: Dapatkan informasi lengkap tentang arsitektur, fitur, dan cara kustomisasi aplikasi.
