#!/usr/bin/env python3
"""
Script untuk generate dokumentasi aplikasi NLP dalam format DOCX
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from datetime import datetime

def add_heading_with_style(doc, text, level=1, color=None):
    """Add heading dengan custom style"""
    heading = doc.add_heading(text, level=level)
    if color:
        for run in heading.runs:
            run.font.color.rgb = color
    return heading

def add_paragraph_with_style(doc, text, bold=False, italic=False, size=11):
    """Add paragraph dengan custom style"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Calibri'
    if bold:
        run.font.bold = True
    if italic:
        run.font.italic = True
    return p

def add_bullet_point(doc, text, level=0):
    """Add bullet point"""
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5 * (level + 1))
    return p

def add_code_block(doc, code, language=""):
    """Add code block dengan background"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.5)

    run = p.add_run(code)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)

    # Add shading
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'F0F0F0')
    p._element.get_or_add_pPr().append(shading_elm)

    return p

def create_dokumentasi():
    """Create dokumentasi lengkap"""
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # ==================== COVER PAGE ====================
    title = doc.add_heading('DOKUMENTASI APLIKASI', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_heading('Analisis Data Teks dengan NLP', 2)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle2 = doc.add_heading('(Natural Language Processing)', 2)
    subtitle2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()
    doc.add_paragraph()

    # Project info centered
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('\nAplikasi Preprocessing Teks\n')
    run.font.size = Pt(14)
    run.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Backend: Python 3.13.6 (Flask, Pandas, NLTK)\n')
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Frontend: Vue 3 + Vite + Bun\n')
    run.font.size = Pt(12)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()

    # Date
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'\n\n{datetime.now().strftime("%d %B %Y")}')
    run.font.size = Pt(12)

    # Page break
    doc.add_page_break()

    # ==================== DAFTAR ISI ====================
    add_heading_with_style(doc, 'DAFTAR ISI', 1, RGBColor(0, 0, 128))

    toc_items = [
        "1. PENDAHULUAN",
        "2. CARA MENJALANKAN APLIKASI",
        "   2.1 Instalasi Dependencies",
        "   2.2 Menjalankan Backend",
        "   2.3 Menjalankan Frontend",
        "   2.4 Menggunakan Script Otomatis",
        "3. SUMBER DATA",
        "   3.1 Dataset yang Digunakan",
        "   3.2 Struktur Dataset",
        "   3.3 Akun dan Topik",
        "4. PIPELINE PREPROCESSING",
        "   4.1 Input Teks",
        "   4.2 Text Cleaning",
        "   4.3 Tokenisasi",
        "   4.4 Stopword Removal",
        "   4.5 Output",
        "5. ARSITEKTUR APLIKASI",
        "   5.1 Backend (Python Flask)",
        "   5.2 Frontend (Vue.js)",
        "   5.3 API Endpoints",
        "6. FITUR APLIKASI",
        "7. CONTOH PENGGUNAAN",
        "8. TROUBLESHOOTING",
    ]

    for item in toc_items:
        doc.add_paragraph(item, style='List Bullet' if not item[0].isdigit() else 'Normal')

    doc.add_page_break()

    # ==================== 1. PENDAHULUAN ====================
    add_heading_with_style(doc, '1. PENDAHULUAN', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc,
        'Aplikasi Analisis Data Teks dengan NLP (Natural Language Processing) adalah aplikasi '
        'web yang dirancang untuk melakukan preprocessing teks secara otomatis. Aplikasi ini '
        'menggunakan Python sebagai backend dan Vue.js sebagai frontend, dengan fokus pada '
        'pemrosesan teks Bahasa Indonesia.')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Tujuan Aplikasi:', bold=True)
    add_bullet_point(doc, 'Memudahkan preprocessing data teks untuk analisis NLP')
    add_bullet_point(doc, 'Menyediakan pipeline preprocessing yang terstruktur')
    add_bullet_point(doc, 'Memberikan visualisasi hasil preprocessing yang jelas')
    add_bullet_point(doc, 'Support untuk batch processing dataset CSV')
    add_bullet_point(doc, 'Interface yang user-friendly dan mudah digunakan')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Teknologi yang Digunakan:', bold=True)

    doc.add_paragraph('Backend:')
    add_bullet_point(doc, 'Python 3.13.6')
    add_bullet_point(doc, 'Flask 3.1.0 - Web Framework')
    add_bullet_point(doc, 'Pandas 2.2.3 - Data Processing')
    add_bullet_point(doc, 'NumPy 2.2.1 - Numerical Computing')
    add_bullet_point(doc, 'NLTK 3.9.1 - Natural Language Toolkit')
    add_bullet_point(doc, 'Sastrawi 1.0.1 - Indonesian Stemmer')
    add_bullet_point(doc, 'Emoji 2.14.0 - Emoji Processing')

    doc.add_paragraph('Frontend:')
    add_bullet_point(doc, 'Vue 3.5.24 - Progressive JavaScript Framework')
    add_bullet_point(doc, 'Vite 7.2.2 - Build Tool')
    add_bullet_point(doc, 'Bun - JavaScript Runtime & Package Manager')

    doc.add_page_break()

    # ==================== 2. CARA MENJALANKAN APLIKASI ====================
    add_heading_with_style(doc, '2. CARA MENJALANKAN APLIKASI', 1, RGBColor(0, 0, 128))

    # 2.1 Instalasi Dependencies
    add_heading_with_style(doc, '2.1 Instalasi Dependencies', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc, 'Backend (Python):', bold=True)
    add_paragraph_with_style(doc,
        'Pastikan Python 3.13.6 sudah terinstall di sistem Anda. Kemudian install dependencies:')

    add_code_block(doc, '''cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\\Scripts\\activate  # Windows

pip install -r requirements.txt''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Frontend (Vue + Bun):', bold=True)
    add_paragraph_with_style(doc,
        'Pastikan Bun sudah terinstall (https://bun.sh). Kemudian install dependencies:')

    add_code_block(doc, '''cd frontend
bun install''')

    # 2.2 Menjalankan Backend
    doc.add_paragraph()
    add_heading_with_style(doc, '2.2 Menjalankan Backend', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Buka terminal pertama dan jalankan server Flask:')

    add_code_block(doc, '''cd backend
source venv/bin/activate
python app.py''')

    add_paragraph_with_style(doc,
        'Backend akan berjalan di http://localhost:5000')

    # 2.3 Menjalankan Frontend
    doc.add_paragraph()
    add_heading_with_style(doc, '2.3 Menjalankan Frontend', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Buka terminal kedua dan jalankan development server:')

    add_code_block(doc, '''cd frontend
bun run dev''')

    add_paragraph_with_style(doc,
        'Frontend akan berjalan di http://localhost:3000')

    # 2.4 Script Otomatis
    doc.add_paragraph()
    add_heading_with_style(doc, '2.4 Menggunakan Script Otomatis', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Untuk kemudahan, tersedia script yang menjalankan backend dan frontend secara otomatis:')

    add_paragraph_with_style(doc, 'Linux/Mac:', bold=True)
    add_code_block(doc, '''chmod +x run.sh
./run.sh''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Windows:', bold=True)
    add_code_block(doc, '''run.bat''')

    add_paragraph_with_style(doc,
        'Script akan otomatis menjalankan backend di port 5000 dan frontend di port 3000. '
        'Buka browser dan akses http://localhost:3000 untuk menggunakan aplikasi.')

    doc.add_page_break()

    # ==================== 3. SUMBER DATA ====================
    add_heading_with_style(doc, '3. SUMBER DATA', 1, RGBColor(0, 0, 128))

    # 3.1 Dataset yang Digunakan
    add_heading_with_style(doc, '3.1 Dataset yang Digunakan', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Aplikasi ini menggunakan dataset komentar dan caption dari media sosial TikTok. '
        'Dataset disimpan dalam format CSV dan berisi informasi lengkap tentang aktivitas '
        'akun TikTok.')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Nama File:', bold=True)
    add_bullet_point(doc, 'dataset_ui_nlp - Sheet1.csv')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Lokasi:', bold=True)
    add_bullet_point(doc, 'Folder: datasets/')
    add_bullet_point(doc, 'Path lengkap: code/datasets/dataset_ui_nlp - Sheet1.csv')

    # 3.2 Struktur Dataset
    doc.add_paragraph()
    add_heading_with_style(doc, '3.2 Struktur Dataset', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Dataset terdiri dari 50 baris data dengan 9 kolom yang berisi informasi berikut:')

    doc.add_paragraph()

    # Create table
    table = doc.add_table(rows=10, cols=3)
    table.style = 'Light Grid Accent 1'

    # Header
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Nama Kolom'
    header_cells[1].text = 'Tipe Data'
    header_cells[2].text = 'Keterangan'

    # Data
    data_rows = [
        ('university', 'String', 'Nama universitas'),
        ('tiktok_account', 'String', 'Username akun TikTok'),
        ('followers', 'Integer', 'Jumlah followers akun'),
        ('video_caption', 'String', 'Caption/deskripsi video (TEKS UNTUK DIPROSES)'),
        ('likes', 'Integer', 'Jumlah likes video'),
        ('video_comments_count', 'Integer', 'Jumlah komentar pada video'),
        ('shares', 'Integer', 'Jumlah share video'),
        ('upload_date', 'Date', 'Tanggal upload video'),
        ('comment_text', 'String', 'Teks komentar dari user (TEKS UNTUK DIPROSES)'),
    ]

    for i, (col, dtype, desc) in enumerate(data_rows, 1):
        cells = table.rows[i].cells
        cells[0].text = col
        cells[1].text = dtype
        cells[2].text = desc

    doc.add_paragraph()
    add_paragraph_with_style(doc,
        'Kolom yang digunakan untuk preprocessing: comment_text dan video_caption',
        bold=True, italic=True)

    # 3.3 Akun dan Topik
    doc.add_paragraph()
    add_heading_with_style(doc, '3.3 Akun dan Topik yang Dianalisis', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc, 'Akun TikTok:', bold=True)
    add_bullet_point(doc, '@ui_official - Akun resmi Universitas Indonesia')
    add_bullet_point(doc, 'Followers: 1,250,000')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Topik Konten:', bold=True)
    add_bullet_point(doc, 'Open house kampus')
    add_bullet_point(doc, 'Tour kampus Universitas Indonesia')
    add_bullet_point(doc, 'Kegiatan mahasiswa')
    add_bullet_point(doc, 'Tips masuk UI')
    add_bullet_point(doc, 'Life at UI / kehidupan kampus')
    add_bullet_point(doc, 'Career Expo dan acara kampus')
    add_bullet_point(doc, 'Rekomendasi tempat belajar')
    add_bullet_point(doc, 'Ospek dan tradisi kampus')
    add_bullet_point(doc, 'Kegiatan volunteer mahasiswa')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Periode Data:', bold=True)
    add_bullet_point(doc, 'Tanggal: 1 Januari 2025 - 10 Januari 2025')
    add_bullet_point(doc, 'Total video: 10 video')
    add_bullet_point(doc, 'Total komentar: 50 komentar')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Karakteristik Teks:', bold=True)
    add_bullet_point(doc, 'Bahasa: Indonesia (dengan campuran bahasa gaul)')
    add_bullet_point(doc, 'Mengandung emoji')
    add_bullet_point(doc, 'Mengandung mention (@) dan hashtag (#)')
    add_bullet_point(doc, 'Mengandung singkatan (bgt, kak, dll)')

    doc.add_page_break()

    # ==================== 4. PIPELINE PREPROCESSING ====================
    add_heading_with_style(doc, '4. PIPELINE PREPROCESSING', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc,
        'Pipeline preprocessing adalah serangkaian tahapan yang dilakukan untuk membersihkan '
        'dan mengolah teks mentah menjadi format yang siap dianalisis. Berikut adalah tahapan '
        'yang diterapkan dalam aplikasi ini:')

    # Diagram alur
    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Alur Pipeline:', bold=True)
    add_code_block(doc, '''INPUT TEKS
    ↓
TEXT CLEANING
    ↓
TOKENISASI
    ↓
STOPWORD REMOVAL
    ↓
OUTPUT''')

    # 4.1 Input Teks
    doc.add_paragraph()
    add_heading_with_style(doc, '4.1 Input Teks', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Tahap pertama adalah menerima input teks yang akan diproses. Input dapat berasal dari:')

    add_bullet_point(doc, 'Dataset CSV (batch processing)')
    add_bullet_point(doc, 'Input manual dari user (single text processing)')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh input:', bold=True)
    add_code_block(doc, 'Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️')

    # 4.2 Text Cleaning
    doc.add_paragraph()
    add_heading_with_style(doc, '4.2 Text Cleaning', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Tahap pembersihan teks dari elemen-elemen yang tidak diperlukan. Proses yang dilakukan:')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'a) Konversi ke Lowercase', bold=True)
    add_paragraph_with_style(doc,
        'Mengubah semua huruf menjadi huruf kecil untuk standarisasi.')
    add_code_block(doc, '''Sebelum: "Semoga Tahun Ini Lulus UI"
Sesudah: "semoga tahun ini lulus ui"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'b) Penghapusan Emoji', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus semua emoji dari teks menggunakan library emoji.')
    add_code_block(doc, '''Sebelum: "love it! ❤️😍🔥"
Sesudah: "love it!"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'c) Penghapusan URL', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus semua URL (http://, https://, www.) dari teks.')
    add_code_block(doc, '''Sebelum: "Cek https://ui.ac.id untuk info"
Sesudah: "Cek untuk info"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'd) Penghapusan Mention dan Hashtag', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus mention (@username) dan hashtag (#tag).')
    add_code_block(doc, '''Sebelum: "Follow @ui_official #UniversitasIndonesia"
Sesudah: "Follow"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'e) Penghapusan Angka', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus semua karakter numerik.')
    add_code_block(doc, '''Sebelum: "UI ranking 1 di Indonesia"
Sesudah: "UI ranking di Indonesia"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'f) Penghapusan Tanda Baca', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus semua tanda baca dan karakter spesial.')
    add_code_block(doc, '''Sebelum: "Keren banget, sih!"
Sesudah: "Keren banget sih"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'g) Normalisasi Whitespace', bold=True)
    add_paragraph_with_style(doc,
        'Menghapus spasi berlebih dan trim di awal/akhir.')
    add_code_block(doc, '''Sebelum: "  keren    banget  "
Sesudah: "keren banget"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Hasil Text Cleaning:', bold=True)
    add_code_block(doc, '''Input: "Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️"
Output: "semoga tahun ini lulus ui aamiin love it"''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Implementasi (Python):', bold=True)
    add_code_block(doc, '''def clean_text(self, text):
    # Konversi ke lowercase
    text = text.lower()

    # Hapus emoji
    text = self.remove_emoji(text)

    # Hapus URL
    text = re.sub(r'http\\S+|www\\S+|https\\S+', '', text)

    # Hapus mentions dan hashtags
    text = re.sub(r'@\\w+|#\\w+', '', text)

    # Hapus angka
    text = re.sub(r'\\d+', '', text)

    # Hapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Hapus whitespace berlebih
    text = ' '.join(text.split())

    return text.strip()''')

    # 4.3 Tokenisasi
    doc.add_page_break()
    add_heading_with_style(doc, '4.3 Tokenisasi', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Tokenisasi adalah proses memecah teks menjadi unit-unit kecil yang disebut token '
        '(biasanya kata). Aplikasi ini menggunakan NLTK word_tokenize.')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Proses:', bold=True)
    add_bullet_point(doc, 'Memisahkan teks berdasarkan spasi dan tanda baca')
    add_bullet_point(doc, 'Menghasilkan list of tokens (kata-kata)')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh:', bold=True)
    add_code_block(doc, '''Input: "semoga tahun ini lulus ui aamiin love it"
Output: ["semoga", "tahun", "ini", "lulus", "ui", "aamiin", "love", "it"]''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Implementasi (Python):', bold=True)
    add_code_block(doc, '''def tokenize(self, text):
    try:
        tokens = word_tokenize(text)
        return tokens
    except:
        # Fallback ke simple split
        return text.split()''')

    # 4.4 Stopword Removal
    doc.add_paragraph()
    add_heading_with_style(doc, '4.4 Stopword Removal', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Stopword removal adalah proses menghapus kata-kata umum yang tidak membawa makna '
        'signifikan dalam analisis. Aplikasi ini menggunakan kombinasi stopwords Indonesia '
        'dari NLTK dan custom stopwords.')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Daftar Stopwords:', bold=True)
    add_paragraph_with_style(doc, 'NLTK Indonesian Stopwords:')
    add_bullet_point(doc, 'yang, dan, di, dari, ke, untuk, pada, dengan, ini, itu, akan, adalah, atau, oleh, dalam, juga')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Custom Stopwords (Bahasa Gaul):')
    add_bullet_point(doc, 'sih, nih, dong, deh, yah, lah, kah, banget, bgt')
    add_bullet_point(doc, 'gw, gue, lu, lo, aku, kamu, dia, mereka, kita')
    add_bullet_point(doc, 'nya, ku, mu, kak, ka')
    add_bullet_point(doc, 'yg, dgn, utk, pd, tdk, tapi, tp')
    add_bullet_point(doc, 'ga, gak, ngga, nggak, udah, sudah, aja, saja')
    add_bullet_point(doc, 'kok, wkwk, wkwkwk, haha, hehe, hihi, huhu')
    add_bullet_point(doc, 'the, a, an, of, to, in, for, on (Inggris umum)')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Filter Tambahan:', bold=True)
    add_bullet_point(doc, 'Token dengan panjang ≤ 2 karakter dihapus')
    add_bullet_point(doc, 'Case insensitive matching')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh:', bold=True)
    add_code_block(doc, '''Input tokens: ["semoga", "tahun", "ini", "lulus", "ui", "aamiin", "love", "it"]
Filtered: ["semoga", "tahun", "lulus", "aamiin", "love"]

Dihapus: "ini" (stopword), "ui" (≤2 char), "it" (stopword)''')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Implementasi (Python):', bold=True)
    add_code_block(doc, '''def remove_stopwords(self, tokens):
    filtered_tokens = [
        token for token in tokens
        if token.lower() not in self.stopwords_id
        and len(token) > 2
    ]
    return filtered_tokens''')

    # 4.5 Output
    doc.add_paragraph()
    add_heading_with_style(doc, '4.5 Output', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc,
        'Hasil akhir dari pipeline preprocessing disimpan dalam format dictionary/object yang berisi:')

    doc.add_paragraph()
    add_bullet_point(doc, 'original: Teks asli sebelum preprocessing')
    add_bullet_point(doc, 'cleaned: Teks setelah cleaning')
    add_bullet_point(doc, 'tokens: Semua token hasil tokenisasi')
    add_bullet_point(doc, 'filtered_tokens: Token setelah stopword removal')
    add_bullet_point(doc, 'token_count: Jumlah token sebelum filtering')
    add_bullet_point(doc, 'filtered_count: Jumlah token setelah filtering')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh Output Lengkap:', bold=True)
    add_code_block(doc, '''{
    "original": "Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️",
    "cleaned": "semoga tahun ini lulus ui aamiin love it",
    "tokens": ["semoga", "tahun", "ini", "lulus", "ui", "aamiin", "love", "it"],
    "filtered_tokens": ["semoga", "tahun", "lulus", "aamiin", "love"],
    "token_count": 8,
    "filtered_count": 5
}''')

    doc.add_page_break()

    # ==================== 5. ARSITEKTUR APLIKASI ====================
    add_heading_with_style(doc, '5. ARSITEKTUR APLIKASI', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc,
        'Aplikasi menggunakan arsitektur client-server dengan pemisahan yang jelas antara '
        'backend dan frontend.')

    # 5.1 Backend
    doc.add_paragraph()
    add_heading_with_style(doc, '5.1 Backend (Python Flask)', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc, 'Komponen:', bold=True)
    add_bullet_point(doc, 'app.py - Main Flask application dengan API endpoints')
    add_bullet_point(doc, 'nlp_processor.py - NLP preprocessing pipeline class')
    add_bullet_point(doc, 'requirements.txt - Python dependencies')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Fungsi Utama:', bold=True)
    add_bullet_point(doc, 'Menyediakan REST API untuk frontend')
    add_bullet_point(doc, 'Membaca dan memproses file CSV')
    add_bullet_point(doc, 'Melakukan text preprocessing')
    add_bullet_point(doc, 'Mengelola NLTK resources')
    add_bullet_point(doc, 'Error handling dan logging')

    # 5.2 Frontend
    doc.add_paragraph()
    add_heading_with_style(doc, '5.2 Frontend (Vue.js)', 2, RGBColor(0, 0, 255))

    add_paragraph_with_style(doc, 'Komponen:', bold=True)
    add_bullet_point(doc, 'App.vue - Main component')
    add_bullet_point(doc, 'DatasetProcessor.vue - Component untuk proses dataset')
    add_bullet_point(doc, 'CustomTextProcessor.vue - Component untuk custom text')
    add_bullet_point(doc, 'style.css - Styling aplikasi')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Fungsi Utama:', bold=True)
    add_bullet_point(doc, 'Interface user untuk input data')
    add_bullet_point(doc, 'Komunikasi dengan backend via API')
    add_bullet_point(doc, 'Visualisasi hasil preprocessing')
    add_bullet_point(doc, 'Tabel interaktif untuk display data')

    # 5.3 API Endpoints
    doc.add_paragraph()
    add_heading_with_style(doc, '5.3 API Endpoints', 2, RGBColor(0, 0, 255))

    # Create table
    table = doc.add_table(rows=6, cols=3)
    table.style = 'Light Grid Accent 1'

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Endpoint'
    header_cells[1].text = 'Method'
    header_cells[2].text = 'Deskripsi'

    endpoints = [
        ('/api/health', 'GET', 'Health check backend'),
        ('/api/datasets', 'GET', 'List available datasets'),
        ('/api/load-dataset', 'POST', 'Load dan preview dataset'),
        ('/api/preprocess', 'POST', 'Preprocess dataset'),
        ('/api/preprocess-custom', 'POST', 'Preprocess custom text'),
    ]

    for i, (endpoint, method, desc) in enumerate(endpoints, 1):
        cells = table.rows[i].cells
        cells[0].text = endpoint
        cells[1].text = method
        cells[2].text = desc

    doc.add_page_break()

    # ==================== 6. FITUR APLIKASI ====================
    add_heading_with_style(doc, '6. FITUR APLIKASI', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc, '1. Dataset Processing Mode', bold=True)
    add_bullet_point(doc, 'Upload atau pilih dataset CSV dari folder')
    add_bullet_point(doc, 'Preview dataset sebelum diproses')
    add_bullet_point(doc, 'Pilih kolom teks yang akan diproses')
    add_bullet_point(doc, 'Atur jumlah data yang akan diproses (batch processing)')
    add_bullet_point(doc, 'Otomatis mendeteksi kolom teks (comment_text, video_caption)')

    doc.add_paragraph()
    add_paragraph_with_style(doc, '2. Custom Text Processing Mode', bold=True)
    add_bullet_point(doc, 'Input teks manual untuk preprocessing')
    add_bullet_point(doc, 'Contoh teks bawaan untuk testing')
    add_bullet_point(doc, 'Real-time processing')

    doc.add_paragraph()
    add_paragraph_with_style(doc, '3. Visualisasi Hasil', bold=True)
    add_bullet_point(doc, 'Tabel perbandingan teks asli vs hasil preprocessing')
    add_bullet_point(doc, 'Badge visual untuk tokens')
    add_bullet_point(doc, 'Color coding: tokens (biru), filtered tokens (hijau)')
    add_bullet_point(doc, 'Counter jumlah tokens')
    add_bullet_point(doc, 'Scrollable content untuk tokens yang banyak')

    doc.add_paragraph()
    add_paragraph_with_style(doc, '4. Error Handling', bold=True)
    add_bullet_point(doc, 'Validasi input')
    add_bullet_point(doc, 'Pesan error yang informatif')
    add_bullet_point(doc, 'Connection status monitoring')
    add_bullet_point(doc, 'Fallback mechanism untuk tokenizer')

    doc.add_paragraph()
    add_paragraph_with_style(doc, '5. User Experience', bold=True)
    add_bullet_point(doc, 'Interface yang clean dan modern')
    add_bullet_point(doc, 'Responsive design')
    add_bullet_point(doc, 'Loading indicators')
    add_bullet_point(doc, 'Tab navigation')

    doc.add_page_break()

    # ==================== 7. CONTOH PENGGUNAAN ====================
    add_heading_with_style(doc, '7. CONTOH PENGGUNAAN', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc, 'Contoh 1: Dataset Processing', bold=True, size=12)

    add_paragraph_with_style(doc, 'Langkah-langkah:')
    add_bullet_point(doc, '1. Buka aplikasi di http://localhost:3000')
    add_bullet_point(doc, '2. Pastikan tab "Dataset Processing" aktif')
    add_bullet_point(doc, '3. Pilih dataset: "dataset_ui_nlp - Sheet1.csv"')
    add_bullet_point(doc, '4. Pilih kolom: "comment_text"')
    add_bullet_point(doc, '5. Set jumlah data: 50')
    add_bullet_point(doc, '6. Klik "Proses Dataset"')
    add_bullet_point(doc, '7. Lihat hasil dalam tabel')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Hasil yang ditampilkan:', bold=True)
    add_bullet_point(doc, '50 baris data komentar yang sudah diproses')
    add_bullet_point(doc, 'Setiap baris menampilkan: original, cleaned, tokens, filtered_tokens')
    add_bullet_point(doc, 'Total waktu proses: ~2-3 detik untuk 50 data')

    doc.add_paragraph()
    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh 2: Custom Text Processing', bold=True, size=12)

    add_paragraph_with_style(doc, 'Langkah-langkah:')
    add_bullet_point(doc, '1. Klik tab "Custom Text"')
    add_bullet_point(doc, '2. Input teks atau pilih contoh')
    add_bullet_point(doc, '3. Klik "Proses Teks"')
    add_bullet_point(doc, '4. Lihat hasil preprocessing')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Contoh input dan output:', bold=True)

    add_code_block(doc, '''INPUT:
"Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️"

OUTPUT:
- Original: "Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️"
- Cleaned: "semoga tahun ini lulus ui aamiin love it"
- Tokens: ["semoga", "tahun", "ini", "lulus", "ui", "aamiin", "love", "it"]
- Filtered: ["semoga", "tahun", "lulus", "aamiin", "love"]
- Count: 8 → 5''')

    doc.add_page_break()

    # ==================== 8. TROUBLESHOOTING ====================
    add_heading_with_style(doc, '8. TROUBLESHOOTING', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc, 'Problem: Backend tidak terhubung', bold=True)
    add_paragraph_with_style(doc, 'Solusi:')
    add_bullet_point(doc, 'Pastikan Python backend berjalan di port 5000')
    add_bullet_point(doc, 'Check dengan: curl http://localhost:5000/api/health')
    add_bullet_point(doc, 'Restart backend jika perlu')
    add_bullet_point(doc, 'Periksa firewall atau port yang digunakan')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Problem: NLTK Resource Error', bold=True)
    add_paragraph_with_style(doc, 'Solusi:')
    add_bullet_point(doc, 'NLTK akan otomatis download resources saat pertama kali')
    add_bullet_point(doc, 'Tunggu proses download selesai')
    add_bullet_point(doc, 'Jika error, download manual: python -c "import nltk; nltk.download(\'punkt\'); nltk.download(\'stopwords\')"')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Problem: Dataset tidak muncul', bold=True)
    add_paragraph_with_style(doc, 'Solusi:')
    add_bullet_point(doc, 'Pastikan file CSV ada di folder datasets/')
    add_bullet_point(doc, 'Periksa format file (harus .csv)')
    add_bullet_point(doc, 'Restart backend untuk reload datasets')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Problem: Port sudah digunakan', bold=True)
    add_paragraph_with_style(doc, 'Solusi:')
    add_bullet_point(doc, 'Backend: Ubah port di app.py (app.run(..., port=5000))')
    add_bullet_point(doc, 'Frontend: Ubah port di vite.config.js (server.port)')
    add_bullet_point(doc, 'Atau kill process yang menggunakan port: lsof -ti:5000 | xargs kill')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Problem: Preprocessing lambat', bold=True)
    add_paragraph_with_style(doc, 'Solusi:')
    add_bullet_point(doc, 'Kurangi jumlah data yang diproses (default 50)')
    add_bullet_point(doc, 'Gunakan Custom Text untuk testing cepat')
    add_bullet_point(doc, 'Periksa spesifikasi komputer (RAM, CPU)')

    doc.add_page_break()

    # ==================== PENUTUP ====================
    add_heading_with_style(doc, 'PENUTUP', 1, RGBColor(0, 0, 128))

    add_paragraph_with_style(doc,
        'Aplikasi Analisis Data Teks dengan NLP ini menyediakan solusi lengkap untuk '
        'preprocessing teks Bahasa Indonesia. Dengan pipeline yang terstruktur dan interface '
        'yang user-friendly, aplikasi ini dapat digunakan untuk berbagai keperluan analisis teks.')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Keunggulan:', bold=True)
    add_bullet_point(doc, 'Pipeline preprocessing yang lengkap dan terstandarisasi')
    add_bullet_point(doc, 'Support untuk Bahasa Indonesia dan bahasa gaul')
    add_bullet_point(doc, 'Interface yang mudah digunakan')
    add_bullet_point(doc, 'Batch processing untuk dataset besar')
    add_bullet_point(doc, 'Visualisasi hasil yang jelas')
    add_bullet_point(doc, 'Open source dan dapat dikembangkan lebih lanjut')

    doc.add_paragraph()
    add_paragraph_with_style(doc, 'Pengembangan Selanjutnya:', bold=True)
    add_bullet_point(doc, 'Tambahan fitur stemming/lemmatization')
    add_bullet_point(doc, 'Analisis sentimen')
    add_bullet_point(doc, 'Word cloud visualization')
    add_bullet_point(doc, 'Export hasil preprocessing ke CSV/Excel')
    add_bullet_point(doc, 'Support untuk bahasa lain')
    add_bullet_point(doc, 'Machine learning integration')

    doc.add_paragraph()
    doc.add_paragraph()

    add_paragraph_with_style(doc,
        'Terima kasih telah menggunakan aplikasi ini. Untuk pertanyaan atau kontribusi, '
        'silakan lihat dokumentasi di README.md atau QUICKSTART.md.')

    # Save document
    output_path = os.path.join(os.path.dirname(__file__), 'DOKUMENTASI_APLIKASI_NLP.docx')
    doc.save(output_path)

    return output_path

if __name__ == '__main__':
    print("Generating dokumentasi...")
    output_file = create_dokumentasi()
    print(f"Dokumentasi berhasil dibuat: {output_file}")
    print("\nFile tersimpan di:")
    print(f"  {output_file}")
