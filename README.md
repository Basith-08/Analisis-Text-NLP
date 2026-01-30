# Analisis Sentimen & Preprocessing NLP

Aplikasi web lengkap untuk analisis sentimen, mulai dari preprocessing teks, training model machine learning, hingga prediksi sentimen pada data baru.

## Fitur Utama

- **Preprocessing Teks Lengkap**
  - Case folding, pembersihan (URL, emoji, mention, angka, dll.).
  - Tokenisasi & Stopword Removal (dengan daftar custom).
  - **Stemming** untuk Bahasa Indonesia menggunakan Sastrawi (opsional).

- **Training & Evaluasi Model**
  - Ekstraksi fitur dengan **Bag-of-Words (BoW)** dan **TF-IDF**.
  - Training tiga model klasifikasi: **Naive Bayes, Decision Tree, dan SVM**.
  - Evaluasi performa model menggunakan Akurasi, Presisi, Recall, dan F1-Score.
  - Visualisasi **Confusion Matrix** untuk setiap model.
  - Perbandingan hasil untuk menemukan model terbaik.

- **Prediksi Sentimen**
  - Gunakan model terbaik yang telah dilatih untuk memprediksi sentimen dari teks baru secara real-time.

- **Manajemen Dataset**
  - Upload file CSV (maks. 16MB) dan langsung gunakan untuk training.
  - Pilih kolom teks dan label secara dinamis.

- **Notebook Analisis**
  - Termasuk notebook Jupyter (`sentiment_analysis_pipeline.ipynb`) yang mendemonstrasikan seluruh alur kerja secara transparan.

### ✨ Fitur Baru: Persistensi Model Otomatis
    
Aplikasi ini sekarang secara otomatis **menyimpan model terbaik** ke disk setelah proses training selesai.
    
- **Tidak Perlu Training Ulang**: Saat aplikasi dijalankan kembali, model terbaik yang sudah tersimpan akan **dimuat secara otomatis**.
- **Langsung Siap Prediksi**: Anda bisa langsung menggunakan fitur prediksi tanpa harus melatih ulang model setiap kali server dinyalakan.
- **Efisien**: Menghemat waktu dan sumber daya komputasi. Model disimpan di `backend/models/best_model.joblib`.

## Teknologi

### Backend
- Python 3.11+
- Flask (Web Framework)
- Pandas & NumPy (Manipulasi Data)
- NLTK (Tokenization, Stopwords)
- Sastrawi (Indonesian Stemmer)
- **Scikit-learn** (Ekstraksi Fitur, Model ML, Evaluasi)
- Joblib (Persistensi Model)

### Frontend
- Vue 3 (Composition API)
- Vite
- Bun (Package Manager & Runtime)

### Analisis & Visualisasi
- Jupyter Notebook
- Matplotlib & Seaborn

## Struktur Proyek

```
code/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── nlp_processor.py       # Pipeline preprocessing NLP
│   ├── models/                # Direktori untuk model yang disimpan
│   │   └── best_model.joblib  # File model terbaik (dibuat otomatis)
│   └── requirements.txt       # Dependensi Python
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DatasetProcessor.vue
│   │   │   ├── CustomTextProcessor.vue
│   │   │   ├── TrainingView.vue       # UI untuk training
│   │   │   └── ResultsView.vue        # UI untuk hasil evaluasi
│   │   └── App.vue              # Komponen utama
│   └── ...
├── datasets/
│   └── ... (contoh: GojekAppReview.csv)
├── sentiment_analysis_pipeline.ipynb # Notebook alur kerja ML
└── README.md
```

## Instalasi

### 1. Setup Backend (Python)

```bash
cd backend

# Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependensi
pip install -r requirements.txt
```

### 2. Setup Frontend (Vue + Bun)

```bash
cd frontend

# Install dependensi
bun install
```

## Menjalankan Aplikasi

Jalankan backend dan frontend secara bersamaan menggunakan skrip yang tersedia.

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

Aplikasi akan tersedia di `http://localhost:3000` (frontend) dan `http://localhost:5000` (backend).

## Alur Kerja Aplikasi

1.  **Tab Preprocessing**: Lakukan preprocessing pada dataset atau teks custom untuk melihat hasilnya (cleaning, tokenisasi, dll.).
2.  **Tab Training & Evaluasi**:
    - **(Hanya saat pertama kali atau jika ingin model baru)** Pilih dataset, kolom teks, dan kolom label.
    - Klik "Mulai Training & Evaluasi".
    - Backend akan melatih 6 kombinasi model dan **menyimpan yang terbaik secara otomatis ke disk**. Hasil perbandingan akan ditampilkan.
3.  **Tab Prediksi Teks**:
    - Masukkan teks baru.
    - Klik "Prediksi Sentimen".
    - Aplikasi akan menggunakan model terbaik yang **tersimpan di disk** (atau dari sesi training terakhir) untuk memberikan prediksi.
    
> **Catatan**: Jika file `backend/models/best_model.joblib` sudah ada saat aplikasi dimulai, Anda bisa langsung ke "Tab Prediksi Teks" tanpa perlu training ulang.

## API Endpoints

- `GET /api/health`: Health check.
- `GET /api/datasets`: Daftar dataset yang tersedia.
- `POST /api/upload-dataset`: Upload dataset CSV baru.
- `POST /api/load-dataset`: Muat kolom dari dataset.
- `POST /api/preprocess`: Proses teks dari dataset (hanya preprocessing).
- `POST /api/preprocess-custom`: Proses teks custom (hanya preprocessing).
- `POST /api/train_evaluate`: Latih dan evaluasi model.
- `POST /api/predict`: Prediksi sentimen pada teks baru.

## Lisensi

MIT License
