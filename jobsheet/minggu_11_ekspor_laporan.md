# Job Sheet 10 — Ekspor Laporan (Excel/PDF) dan Koreksi Data

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengelola laporan dalam aplikasi
**Bahan Kajian:** Link data dengan laporan; ekspor laporan ke Excel dan PDF; tombol download laporan (st.download_button)

## A. Tujuan Praktik

1. Mahasiswa membuat laporan yang **bisa diunduh** pengguna dalam format Excel — kebutuhan nyata dunia administrasi.
2. Mahasiswa mengoreksi data langsung dari aplikasi lewat `st.data_editor` (tabel yang bisa diedit).
3. Mahasiswa memahami pola "laporan = query + filter + tampilan + unduhan".

## B. Alat dan Bahan

- Aplikasi laporan dari Job Sheet 9
- `openpyxl` untuk ekspor Excel: `pip install openpyxl`

## C. Langkah Kerja Terpandu

### Bagian 1 — Tombol unduh Excel (60 menit)

Pola standarnya: tulis ke **buffer memori**, lalu sediakan ke tombol unduh.

```python
import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

koneksi = sqlite3.connect("toko.db")
df = pd.read_sql(
    "SELECT p.id, p.tanggal, p.pelanggan, p.produk, p.jumlah, p.harga, "
    "p.jumlah * p.harga AS total FROM penjualan p", koneksi)
koneksi.close()

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Laporan Penjualan")

st.download_button(
    "Download Laporan (Excel)",
    data=buffer.getvalue(),
    file_name="laporan_penjualan.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
```

Unduh filenya dan buka di Excel — periksa bahwa angkanya sama dengan yang tampil di aplikasi.

### Bagian 2 — Laporan yang mengikuti filter (45 menit)

Letakkan filter periode **sebelum** tombol unduh, dan buat Excel dari **data yang sudah difilter**:

```python
pilihan = st.selectbox("Produk", ["Semua"] + sorted(df["produk"].unique().tolist()))
df_laporan = df if pilihan == "Semua" else df[df["produk"] == pilihan]
st.dataframe(df_laporan, use_container_width=True)
# ... lalu to_excel(df_laporan, ...) — bukan df
```

Kesalahan klasik yang harus dihindari: tombol unduh mengunduh data **mentah** padahal layar menampilkan data **terfilter**.

### Bagian 3 — Koreksi data dengan st.data_editor (75 menit)

```python
st.subheader("Koreksi Cepat Data Transaksi")
df_edit = df[["id", "pelanggan", "jumlah", "harga"]].copy()

hasil = st.data_editor(df_edit, num_rows="dynamic", use_container_width=True, disabled=["id"])

if st.button("Simpan Perubahan"):
    con = sqlite3.connect("toko.db")
    n = 0
    for _, baris in hasil.iterrows():
        con.execute(
            "UPDATE penjualan SET pelanggan = ?, jumlah = ?, harga = ? WHERE id = ?",
            (baris["pelanggan"], int(baris["jumlah"]), int(baris["harga"]), int(baris["id"])),
        )
        n += 1
    con.commit(); con.close()
    st.success(f"{n} baris diproses.")
```

### Bagian 4 — Ekspor PDF sederhana (opsional, 30 menit)

Dengan `pip install fpdf2`:

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=11)
pdf.cell(0, 10, "Laporan Penjualan", ln=True)
for _, r in df_laporan.iterrows():
    pdf.cell(0, 8, f"{r['tanggal']} | {r['pelanggan']} | {r['produk']} | Rp {r['total']:,}", ln=True)

st.download_button("Download Laporan (PDF)", data=bytes(pdf.output()),
                   file_name="laporan.pdf", mime="application/pdf")
```

## D. Tugas Mandiri

1. Sempurnakan laporan Anda: filter produk + rentang tanggal → tabel → metric → **dua** tombol unduh (Excel & PDF) yang isinya sama persis dengan yang tampil.
2. Gunakan nama file yang informatif: `laporan_penjualan_2026-08.xlsx` (tanggal dinamis dari filter).
3. Uji `st.data_editor`: ubah satu nama pelanggan, simpan, lalu cek di laporan — perubahan harus ikut.

## E. Kriteria Selesai

- [ ] File Excel terunduh, terbuka di Excel, dan isinya sesuai tampilan aplikasi
- [ ] Tombol unduh mengikuti filter yang dipilih pengguna
- [ ] Edit lewat `data_editor` tersimpan permanen ke database
- [ ] Mahasiswa dapat menjelaskan alur buffer (`BytesIO`) secara sederhana

## F. Pertanyaan Refleksi

1. Siapa pengguna aplikasi Anda kelak yang membutuhkan laporan Excel, dan untuk apa?
2. Mengapa tombol "Simpan Perubahan" lebih aman daripada menyimpan otomatis setiap sel diedit?
