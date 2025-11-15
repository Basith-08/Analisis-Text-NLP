# Analisis Text NLP - Preprocessing Tool

Aplikasi web untuk preprocessing teks menggunakan NLP (Natural Language Processing) dengan Python sebagai backend dan Vue.js sebagai frontend.

## Fitur

- **Preprocessing Teks Otomatis**
  - Pembersihan data (hapus emoji, karakter khusus, angka)
  - Tokenisasi (pemisahan kata)
  - Stopword removal (hapus kata umum)
  - Support untuk teks Bahasa Indonesia

- **Upload Dataset**
  - Upload file CSV sendiri (maks. 16MB)
  - Validasi otomatis format CSV
  - Preview dataset setelah upload
  - Auto-select dataset yang baru diupload

- **Dua Mode Input**
  - Dataset Processing: Proses file CSV secara batch
  - Custom Text: Proses teks manual secara real-time

- **Visualisasi Hasil**
  - Tabel perbandingan teks asli dan hasil preprocessing
  - Badge untuk tokens dan filtered tokens
  - Preview dataset sebelum diproses

## Teknologi

### Backend
- Python 3.13.6
- Flask (Web Framework)
- Pandas & NumPy (Data Processing)
- NLTK (Tokenization)
- Sastrawi (Indonesian Stemmer)
- Emoji (Emoji Removal)

### Frontend
- Vue 3
- Vite
- Bun (Package Manager & Runtime)

## Struktur Proyek

```
code/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── nlp_processor.py       # NLP preprocessing pipeline
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DatasetProcessor.vue
│   │   │   └── CustomTextProcessor.vue
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── datasets/
│   └── dataset_ui_nlp - Sheet1.csv
└── README.md
```

## Instalasi

### 1. Setup Backend (Python)

```bash
cd backend

# Buat virtual environment (opsional tapi direkomendasikan)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Frontend (Vue + Bun)

```bash
cd frontend

# Install dependencies dengan Bun
bun install
```

## Menjalankan Aplikasi

### Cara 1: Manual (2 Terminal)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
Backend akan berjalan di `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```
Frontend akan berjalan di `http://localhost:3000`

### Cara 2: Menggunakan Script (Otomatis)

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

## Penggunaan

1. Buka browser dan akses `http://localhost:3000`

2. **Upload Dataset (Opsional):**
   - Klik "Dataset Processing" tab
   - Pada bagian "Upload Dataset Baru", klik "Choose File"
   - Pilih file CSV dari komputer Anda (maks. 16MB)
   - Klik tombol "Upload"
   - Dataset akan otomatis tersimpan dan terpilih

3. **Mode Dataset Processing:**
   - Pilih dataset dari dropdown (atau gunakan dataset yang baru diupload)
   - Klik tombol "Refresh" untuk memperbarui daftar dataset
   - Pilih kolom teks yang ingin diproses
   - Tentukan jumlah data yang akan diproses
   - Klik "Proses Dataset"
   - Lihat hasil preprocessing dalam tabel

4. **Mode Custom Text:**
   - Klik tab "Custom Text"
   - Masukkan teks manual atau pilih contoh
   - Klik "Proses Teks"
   - Lihat hasil preprocessing

## Pipeline Preprocessing

1. **Input Teks**: Ambil teks dari dataset atau input manual
2. **Cleaning**:
   - Konversi ke lowercase
   - Hapus emoji
   - Hapus URL, mention, hashtag
   - Hapus angka
   - Hapus tanda baca dan karakter khusus
3. **Tokenisasi**: Pisahkan teks menjadi kata-kata
4. **Stopword Removal**: Hapus kata-kata umum yang tidak bermakna
5. **Output**: Tampilkan hasil dalam tabel

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/datasets` - List available datasets
- `POST /api/upload-dataset` - Upload new CSV dataset (max 16MB)
- `POST /api/load-dataset` - Load and preview dataset
- `POST /api/preprocess` - Preprocess dataset
- `POST /api/preprocess-custom` - Preprocess custom text

## Troubleshooting

### Backend tidak terhubung
- Pastikan Python backend berjalan di port 5000
- Cek apakah semua dependencies terinstall
- Jalankan `python app.py` di folder backend

### NLTK Resource Error
NLTK akan otomatis mendownload resource yang diperlukan saat pertama kali dijalankan.

### Dataset tidak muncul
Pastikan file CSV ada di folder `datasets/`

## Kontribusi

Aplikasi ini dikembangkan untuk tugas Pemrosesan Bahasa Alami.

## Lisensi

MIT License
