# Job Sheet 3 — Dasar Python dan Membuat Tabel Database

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat membuat project Python dan mengelola tabel database
**Bahan Kajian:** Dasar Python (variabel, tipe data, percabangan, perulangan); membuat tabel dan index dengan SQLite

## A. Tujuan Praktik

1. Mahasiswa menguasai variabel, tipe data dasar (`str`, `int`, `float`), dan `list`/`dict` di Python.
2. Mahasiswa membuat database `toko.db` dan tabel `produk` dengan SQLite — tanpa menginstall apa pun, karena SQLite sudah bagian dari Python.
3. Mahasiswa memahami tipe kolom dan kunci utama (`PRIMARY KEY`).

## B. Alat dan Bahan

- Python + Streamlit + VS Code (dari Job Sheet 1–2)
- Modul `sqlite3` (bawaan Python — tidak perlu `pip install`)

## C. Langkah Kerja Terpandu

### Bagian 1 — Latihan dasar Python (60 menit)

Ketik dan jalankan skrip berikut (bisa lewat `python latihan.py` atau interaktif dengan `python`):

```python
nama_produk = "Buku Tulis"     # str  : teks
harga = 5000                   # int  : bilangan bulat
berat = 0.35                   # float: bilangan desimal
stok = True                    # bool : True/False

produk_list = ["Buku Tulis", "Pulpen", "Tas"]          # list : deretan nilai
produk_dict = {"nama": "Buku Tulis", "harga": 5000}    # dict : pasangan kunci-nilai

for p in produk_list:
    print("Kami menjual:", p)

if harga > 4000:
    print(nama_produk, "termasuk produk margin tinggi")
```

### Bagian 2 — Membuat database dan tabel (60 menit)

Buat file `buat_tabel.py`:

```python
import sqlite3

koneksi = sqlite3.connect("toko.db")   # membuat file toko.db bila belum ada
cursor = koneksi.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produk (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nama     TEXT NOT NULL,
        kategori TEXT,
        harga    INTEGER,
        stok     INTEGER DEFAULT 0
    )
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_nama ON produk(nama)")

koneksi.commit()
koneksi.close()
print("Database toko.db dan tabel produk siap.")
```

Jalankan, lalu cek: file `toko.db` muncul di folder yang sama. Database = **hanya satu file**, inilah keunggulan SQLite untuk latihan.

### Bagian 3 — Verifikasi lewat Streamlit (60 menit)

Buat file `cek_db.py`:

```python
import streamlit as st
import sqlite3

st.title("Cek Database Toko")

koneksi = sqlite3.connect("toko.db")
daftar_tabel = koneksi.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()
koneksi.close()

st.write("Tabel yang ada di database:", daftar_tabel)
st.success("Koneksi database berhasil!" if daftar_tabel else "Belum ada tabel.")
```

## D. Tugas Mandiri

1. Buat tabel kedua bernama `pelanggan` dengan kolom: `id`, `nama`, `telepon`, `alamat`, `tanggal_daftar` (semua `TEXT` selain `id`). Kumpulkan sebagai skrip `buat_tabel_pelanggan.py`.
2. Tuliskan di kertas: tipe data Python yang cocok untuk (a) nama produk, (b) harga, (c) status member.
3. Eksperimen: hapus file `toko.db`, jalankan ulang skrip, dan jelaskan apa yang terjadi.

## E. Kriteria Selesai

- [ ] Skrip latihan dasar Python berjalan tanpa error
- [ ] File `toko.db` berhasil dibuat dan tabel `produk` terdeteksi oleh `cek_db.py`
- [ ] Index `idx_nama` berhasil dibuat (cek lewat query `sqlite_master`)
- [ ] Tabel `pelanggan` dibuat oleh skrip mandiri mahasiswa

## F. Pertanyaan Refleksi

1. Apa fungsi `PRIMARY KEY` dan mengapa tabel transaksi hampir selalu memilikinya?
2. Apa bedanya menyimpan data di `toko.db` dengan menyimpannya di variabel Python biasa?
