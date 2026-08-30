# Job Sheet 6 — Query Lanjutan: Agregasi, Pencarian, dan Filter

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengelola record dengan query
**Bahan Kajian:** Query agregasi (SUM, AVG, COUNT); pencarian data (LIKE); filter dan pengelompokan data

## A. Tujuan Praktik

1. Mahasiswa menguasai fungsi agregasi: `SUM`, `AVG`, `COUNT`, `MIN`, `MAX`.
2. Mahasiswa mampu mencari data dengan pola (`LIKE`) dan memfilter berdasarkan rentang nilai/tanggal.
3. Mahasiswa menghubungkan **input pengguna di Streamlit** dengan **parameter query** — titik sambung pertama antara UI dan database.

## B. Alat dan Bahan

- Database `toko.db` dengan tabel `produk` dan `penjualan` (Job Sheet 3–5)
- Untuk latihan filter tanggal, isi tabel `penjualan` dengan tanggal yang beragam (Job Sheet 5, ubah-ubah tanggalnya, atau pakai generator acak milik dosen)

## C. Langkah Kerja Terpandu

### Bagian 1 — Agregasi (45 menit)

Jalankan dan pahami hasil tiap query:

```python
import sqlite3
koneksi = sqlite3.connect("toko.db")

print("Total omzet          :", koneksi.execute(
    "SELECT SUM(harga * jumlah) FROM penjualan JOIN produk ON produk.id = penjualan.produk_id"
).fetchone()[0])

print("Jumlah transaksi     :", koneksi.execute("SELECT COUNT(*) FROM penjualan").fetchone()[0])
print("Rata-rata item/trx   :", koneksi.execute("SELECT AVG(jumlah) FROM penjualan").fetchone()[0])
print("Produk termahal      :", koneksi.execute(
    "SELECT nama, harga FROM produk ORDER BY harga DESC LIMIT 1").fetchone())
```

### Bagian 2 — Mencari dengan LIKE (45 menit)

```python
kata = "buk"   # coba juga kata yang tidak ada hasilnya
for baris in koneksi.execute(
    "SELECT nama, harga FROM produk WHERE nama LIKE ?", (f"%{kata}%",)
):
    print(baris)
```

`LIKE '%buk%'` berarti "mengandung kata 'buk' di posisi mana pun". Huruf besar/kecil diabaikan untuk teks latin.

### Bagian 3 — Menghubungkan input user ke query (90 menit)

Buat file `cari_produk.py`. Ini pola paling penting job sheet ini:

```python
import streamlit as st
import sqlite3

st.title("Pencarian Produk")

koneksi = sqlite3.connect("toko.db")
kata = st.text_input("Cari nama produk")

if kata:
    hasil = koneksi.execute(
        "SELECT nama, kategori, harga, stok FROM produk WHERE nama LIKE ? OR kategori LIKE ?",
        (f"%{kata}%", f"%{kata}%"),
    ).fetchall()
    st.write(f"Ditemukan {len(hasil)} produk:")
    st.dataframe(hasil, use_container_width=True)
else:
    st.info("Ketik kata kunci untuk mulai mencari.")
```

### Bagian 4 — Filter tanggal (30 menit)

```python
import streamlit as st
from datetime import date

koneksi = sqlite3.connect("toko.db")
dari = st.date_input("Dari tanggal", value=date(2026, 8, 1))
sampai = st.date_input("Sampai tanggal", value=date(2026, 8, 31))

total = koneksi.execute(
    "SELECT SUM(jumlah) FROM penjualan WHERE tanggal BETWEEN ? AND ?",
    (dari.isoformat(), sampai.isoformat()),
).fetchone()[0]
st.metric("Total item terjual pada periode itu", total or 0)
```

## D. Tugas Mandiri

1. Buat `laporan_kategori.py`: pilih kategori lewat `st.selectbox`, aplikasi menampilkan produk kategori tersebut beserta jumlah dan rata-rata harganya (`COUNT`, `AVG`).
2. Gabungkan pencarian nama **dan** filter rentang harga (dua `st.number_input` batas bawah/atas) dalam satu aplikasi.
3. Tuliskan query untuk menjawab: *"produk apa yang terjual paling banyak (jumlah terbesar) selama Agustus 2026?"* — dan tunjukkan hasilnya.

## E. Kriteria Selesai

- [ ] Kelima fungsi agregasi diuji dan hasilnya dicatat
- [ ] Pencarian `LIKE` bekerja: kata kunci sebagian pun menemukan hasil
- [ ] Aplikasi pencarian mengubah hasil secara langsung mengikuti input user
- [ ] Filter tanggal menghasilkan angka omzet/penjualan yang benar

## F. Pertanyaan Refleksi

1. Mengapa nilai dari `st.text_input` dikirim lewat parameter `?`, bukan ditempel ke string query?
2. Laporan bisnis apa di tempat kerja Anda kelak yang mirip dengan filter periode tanggal ini?
