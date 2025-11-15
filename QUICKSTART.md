# Quick Start Guide

## Instalasi Dependencies Selesai!

Semua dependencies Python telah terinstall dengan sukses. Sekarang Anda bisa menjalankan aplikasi.

## Menjalankan Aplikasi

### Opsi 1: Menggunakan Script Otomatis (RECOMMENDED)

```bash
./run.sh
```

Script ini akan otomatis menjalankan backend dan frontend secara bersamaan.

### Opsi 2: Manual (2 Terminal Terpisah)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```

## Akses Aplikasi

Setelah kedua server berjalan:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Cara Menggunakan

### 1. Dataset Processing Mode
1. Pilih dataset dari dropdown (dataset sudah tersedia di folder `datasets/`)
2. Pilih kolom teks yang ingin diproses (otomatis terdeteksi: comment_text, video_caption)
3. Tentukan jumlah data yang ingin diproses (default: 50)
4. Klik "Proses Dataset"
5. Lihat hasil preprocessing dalam tabel

### 2. Custom Text Mode
1. Klik tab "Custom Text"
2. Masukkan teks manual atau pilih contoh
3. Klik "Proses Teks"
4. Lihat hasil preprocessing

## Fitur Preprocessing

Pipeline yang diterapkan:
1. **Cleaning**: Hapus emoji, URL, mention, hashtag, angka, tanda baca
2. **Tokenization**: Pisahkan teks menjadi kata-kata
3. **Stopword Removal**: Hapus kata-kata umum (yang, dan, di, dll)
4. **Normalization**: Konversi ke lowercase

## Hasil Output

Untuk setiap teks, Anda akan melihat:
- **Teks Asli**: Teks sebelum diproses
- **Teks Bersih**: Teks setelah cleaning
- **Tokens**: Semua kata hasil tokenisasi
- **Filtered Tokens**: Kata-kata setelah stopword removal
- **Jumlah**: Total filtered tokens

## Dataset yang Tersedia

- `dataset_ui_nlp - Sheet1.csv` - Dataset komentar TikTok Universitas Indonesia

Kolom dalam dataset:
- university
- tiktok_account
- followers
- video_caption
- likes
- video_comments_count
- shares
- upload_date
- comment_text

## Troubleshooting

### Backend tidak terhubung
```bash
# Cek apakah backend berjalan
curl http://localhost:5000/api/health

# Jika error, restart backend
cd backend
source venv/bin/activate
python app.py
```

### NLTK Error
NLTK resources akan didownload otomatis saat pertama kali dijalankan. Jika ada error, tunggu hingga download selesai.

### Port sudah digunakan
Jika port 5000 atau 3000 sudah digunakan, ubah di:
- Backend: `backend/app.py` (line terakhir: `app.run(..., port=5000)`)
- Frontend: `frontend/vite.config.js` (server.port)

## Tips

1. Mulai dengan dataset kecil (50-100 data) untuk testing
2. Gunakan Custom Text untuk testing preprocessing secara cepat
3. Periksa hasil preprocessing untuk memastikan pipeline bekerja dengan baik
4. Dataset dapat ditambah dengan menaruh file CSV di folder `datasets/`

Selamat mencoba!
