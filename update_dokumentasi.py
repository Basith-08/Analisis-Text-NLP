#!/usr/bin/env python3
"""
Script untuk menambahkan section Upload Dataset ke dokumentasi
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def add_upload_section(doc_path):
    """Add upload feature section to existing documentation"""

    doc = Document(doc_path)

    # Add page break before new section
    doc.add_page_break()

    # Add new section header
    heading = doc.add_heading('FITUR UPLOAD DATASET (UPDATE)', 1)
    for run in heading.runs:
        run.font.color.rgb = RGBColor(0, 0, 128)

    # Introduction
    p = doc.add_paragraph()
    run = p.add_run(
        'Aplikasi telah dilengkapi dengan fitur upload dataset yang memungkinkan user untuk '
        'mengupload file CSV sendiri tanpa perlu menempatkan file secara manual ke folder datasets.')
    run.font.size = Pt(11)

    # Cara Upload
    doc.add_paragraph()
    heading2 = doc.add_heading('Cara Upload Dataset', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    doc.add_paragraph('1. Buka tab "Dataset Processing"')
    doc.add_paragraph('2. Pada bagian "Upload Dataset Baru", klik tombol "Choose File"')
    doc.add_paragraph('3. Pilih file CSV dari komputer (maks. 16MB)')
    doc.add_paragraph('4. Klik tombol "Upload"')
    doc.add_paragraph('5. Dataset akan otomatis tersimpan dan terpilih untuk diproses')

    # Validasi
    doc.add_paragraph()
    heading2 = doc.add_heading('Validasi File', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    p = doc.add_paragraph()
    run = p.add_run('Aplikasi akan memvalidasi file dengan kriteria:')
    run.font.size = Pt(11)
    run.font.bold = True

    doc.add_paragraph('Ekstensi file: Hanya .csv yang diperbolehkan', style='List Bullet')
    doc.add_paragraph('Ukuran file: Maksimal 16MB', style='List Bullet')
    doc.add_paragraph('Format CSV: Harus valid dan dapat dibaca oleh Pandas', style='List Bullet')
    doc.add_paragraph('Header: File harus memiliki baris header (nama kolom)', style='List Bullet')

    # Technical Implementation
    doc.add_paragraph()
    heading2 = doc.add_heading('Implementasi Teknis', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    p = doc.add_paragraph()
    run = p.add_run('Backend (Flask):')
    run.font.size = Pt(11)
    run.font.bold = True

    doc.add_paragraph('Endpoint: POST /api/upload-dataset', style='List Bullet')
    doc.add_paragraph('Menggunakan werkzeug.secure_filename untuk keamanan', style='List Bullet')
    doc.add_paragraph('Validasi file extension dan size', style='List Bullet')
    doc.add_paragraph('Auto-validate CSV dengan pandas.read_csv()', style='List Bullet')
    doc.add_paragraph('File disimpan ke folder datasets/', style='List Bullet')

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run('Frontend (Vue):')
    run.font.size = Pt(11)
    run.font.bold = True

    doc.add_paragraph('Input file dengan validasi client-side', style='List Bullet')
    doc.add_paragraph('FormData untuk multipart file upload', style='List Bullet')
    doc.add_paragraph('Loading indicator saat upload', style='List Bullet')
    doc.add_paragraph('Alert sukses/error dengan styling', style='List Bullet')
    doc.add_paragraph('Auto-refresh dataset list setelah upload', style='List Bullet')
    doc.add_paragraph('Auto-select dataset yang baru diupload', style='List Bullet')

    # UI Components
    doc.add_paragraph()
    heading2 = doc.add_heading('Komponen UI', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    doc.add_paragraph('Upload Section:', style='List Bullet')
    doc.add_paragraph('   - Border dashed untuk visual indicator', style='List Bullet')
    doc.add_paragraph('   - File input dengan accept=".csv"', style='List Bullet')
    doc.add_paragraph('   - Upload button dengan loading state', style='List Bullet')
    doc.add_paragraph('   - Alert message untuk feedback', style='List Bullet')

    doc.add_paragraph()
    doc.add_paragraph('Refresh Button:', style='List Bullet')
    doc.add_paragraph('   - Tombol refresh di samping dropdown dataset', style='List Bullet')
    doc.add_paragraph('   - Memperbarui daftar dataset tanpa reload page', style='List Bullet')

    # Keamanan
    doc.add_paragraph()
    heading2 = doc.add_heading('Keamanan', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    doc.add_paragraph('File extension whitelist (hanya .csv)', style='List Bullet')
    doc.add_paragraph('File size limit 16MB untuk prevent DoS', style='List Bullet')
    doc.add_paragraph('Filename sanitization dengan secure_filename()', style='List Bullet')
    doc.add_paragraph('CSV validation sebelum save', style='List Bullet')
    doc.add_paragraph('Auto-delete file jika validation gagal', style='List Bullet')

    # Error Handling
    doc.add_paragraph()
    heading2 = doc.add_heading('Error Handling', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    # Create error table
    table = doc.add_table(rows=5, cols=2)
    table.style = 'Light Grid Accent 1'

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Error'
    header_cells[1].text = 'Handling'

    errors = [
        ('File bukan CSV', 'Client & server validation, reject dengan message'),
        ('File > 16MB', 'Client & server validation, reject dengan message'),
        ('CSV invalid/corrupt', 'Server validation, auto-delete file, return error'),
        ('Upload gagal', 'Try-catch block, rollback, user-friendly error message'),
    ]

    for i, (error, handling) in enumerate(errors, 1):
        cells = table.rows[i].cells
        cells[0].text = error
        cells[1].text = handling

    # Benefits
    doc.add_paragraph()
    heading2 = doc.add_heading('Keuntungan Fitur Upload', 2)
    for run in heading2.runs:
        run.font.color.rgb = RGBColor(0, 0, 255)

    doc.add_paragraph('User tidak perlu akses langsung ke server', style='List Bullet')
    doc.add_paragraph('Upload langsung dari browser', style='List Bullet')
    doc.add_paragraph('Validasi otomatis untuk mencegah error', style='List Bullet')
    doc.add_paragraph('Auto-select dataset untuk kemudahan', style='List Bullet')
    doc.add_paragraph('Feedback real-time (loading, success, error)', style='List Bullet')
    doc.add_paragraph('File tersimpan permanen di server', style='List Bullet')

    # Save updated document
    output_path = doc_path.replace('.docx', '_UPDATED.docx')
    doc.save(output_path)

    return output_path

if __name__ == '__main__':
    doc_path = os.path.join(os.path.dirname(__file__), 'DOKUMENTASI_APLIKASI_NLP.docx')

    if not os.path.exists(doc_path):
        print(f"Error: File {doc_path} tidak ditemukan")
        exit(1)

    print("Updating dokumentasi...")
    output_file = add_upload_section(doc_path)
    print(f"Dokumentasi berhasil diupdate: {output_file}")
    print("\nFile tersimpan di:")
    print(f"  {output_file}")
