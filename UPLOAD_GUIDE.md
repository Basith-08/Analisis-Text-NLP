# Panduan Upload Dataset

Fitur upload dataset memungkinkan Anda untuk mengupload file CSV sendiri dan langsung memprosesnya.

## Cara Upload Dataset

### 1. Akses Halaman Dataset Processing
- Buka aplikasi di `http://localhost:3000`
- Pastikan tab **"Dataset Processing"** aktif

### 2. Upload File CSV
- Pada bagian **"Upload Dataset Baru"** (di atas dropdown pilihan dataset)
- Klik tombol **"Choose File"** atau **"Browse"**
- Pilih file CSV dari komputer Anda
- File akan divalidasi secara otomatis

### 3. Klik Upload
- Setelah file terpilih, klik tombol **"Upload"**
- Tunggu proses upload selesai (ditandai dengan loading spinner)
- Jika berhasil, akan muncul pesan sukses berwarna hijau

### 4. Dataset Otomatis Terpilih
- Dataset yang baru diupload akan otomatis terpilih di dropdown
- Preview dataset akan muncul di bawah
- Kolom teks akan terdeteksi otomatis

## Validasi File

Aplikasi akan memvalidasi file CSV dengan kriteria:

### Format File
- **Ekstensi**: Hanya file `.csv` yang diperbolehkan
- **Ukuran**: Maksimal 16MB
- **Encoding**: UTF-8 (recommended)

### Struktur CSV
- File harus berisi header (baris pertama sebagai nama kolom)
- Minimal memiliki 1 kolom
- Data harus dalam format CSV standar

## Contoh File CSV yang Valid

```csv
id,name,text,category
1,Sample 1,Ini adalah contoh teks pertama,kategori_a
2,Sample 2,Contoh teks kedua untuk diproses,kategori_b
3,Sample 3,Teks ketiga dengan emoji 😊,kategori_a
```

## Tips Upload

1. **Pastikan Format CSV Benar**
   - Gunakan comma (,) sebagai delimiter
   - Jangan gunakan semicolon (;)
   - Hindari karakter khusus dalam nama kolom

2. **Nama File**
   - Gunakan nama file yang deskriptif
   - Hindari spasi, gunakan underscore (_) atau dash (-)
   - Contoh: `dataset_komentar_2025.csv`

3. **Kolom Teks**
   - Pastikan ada kolom yang berisi teks untuk diproses
   - Nama kolom yang umum: `text`, `content`, `comment`, `caption`, `description`
   - Aplikasi akan mendeteksi kolom teks secara otomatis

4. **Ukuran File**
   - Jika file terlalu besar (>16MB), pertimbangkan untuk:
     - Split file menjadi beberapa bagian
     - Filter hanya data yang diperlukan
     - Compress atau remove kolom yang tidak perlu

## Troubleshooting

### Error: "Hanya file CSV yang diperbolehkan"
**Penyebab**: File yang dipilih bukan format CSV

**Solusi**:
- Pastikan file berekstensi `.csv`
- Jangan upload file Excel (.xlsx) atau text (.txt)
- Convert file ke CSV terlebih dahulu

### Error: "Ukuran file maksimal 16MB"
**Penyebab**: File terlalu besar

**Solusi**:
- Reduce jumlah baris dalam CSV
- Hapus kolom yang tidak diperlukan
- Split file menjadi beberapa bagian kecil

### Error: "Invalid CSV file"
**Penyebab**: Struktur CSV tidak valid atau corrupt

**Solusi**:
- Buka file di Excel/LibreOffice dan save ulang sebagai CSV
- Periksa apakah ada karakter khusus atau error dalam file
- Pastikan encoding UTF-8

### Upload Berhasil tapi Dataset Tidak Muncul
**Solusi**:
- Klik tombol **"Refresh"** di samping dropdown
- Reload halaman browser (F5)
- Periksa console browser untuk error (F12)

## Lokasi Penyimpanan

File yang diupload akan disimpan di:
```
code/datasets/[nama_file].csv
```

File akan tetap tersimpan bahkan setelah aplikasi direstart, sehingga bisa digunakan kembali.

## Keamanan

- Aplikasi hanya menerima file CSV
- File size dibatasi 16MB untuk mencegah overflow
- Filename di-sanitize otomatis untuk keamanan
- File divalidasi sebelum disimpan

## Contoh Use Case

### Use Case 1: Analisis Komentar Social Media
```csv
timestamp,username,comment,likes
2025-01-01,user1,Keren banget! 🔥,10
2025-01-01,user2,Sangat membantu,5
```

### Use Case 2: Review Produk
```csv
product_id,product_name,review_text,rating
P001,Product A,Produk bagus dan berkualitas,5
P002,Product B,Harga terjangkau,4
```

### Use Case 3: Feedback Survey
```csv
respondent_id,question,answer_text,date
R001,Apa pendapat Anda?,Saya sangat puas,2025-01-15
R002,Apa pendapat Anda?,Perlu perbaikan,2025-01-15
```

## Next Steps Setelah Upload

1. **Preview Dataset**: Periksa preview untuk memastikan data benar
2. **Pilih Kolom**: Pilih kolom teks yang ingin diproses
3. **Set Limit**: Tentukan jumlah data (untuk testing mulai dari 10-50 data)
4. **Proses**: Klik "Proses Dataset"
5. **Analisis Hasil**: Lihat hasil preprocessing dalam tabel

---

Jika Anda mengalami masalah yang tidak tercantum di sini, silakan periksa:
- README.md untuk dokumentasi lengkap
- QUICKSTART.md untuk panduan cepat
- Console browser (F12) untuk error messages
