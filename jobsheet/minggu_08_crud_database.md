# Job Sheet 8 — Aplikasi CRUD Lengkap: Form Terhubung Database

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengelola form aplikasi terhubung database
**Bahan Kajian:** Konektivitas data dengan form; aplikasi CRUD lengkap (tambah, lihat, ubah, hapus); validasi data input

## A. Tujuan Praktik

1. Mahasiswa merangkai semua materi sebelumnya menjadi satu aplikasi utuh: form input yang **menyimpan permanen** ke SQLite.
2. Mahasiswa mengimplementasikan CRUD lengkap: **C**reate, **R**ead, **U**pdate, **D**elete.
3. Mahasiswa memasang validasi agar data rusak tidak masuk ke database.

## B. Alat dan Bahan

- Database `toko.db` + tabel `produk`, `penjualan` (Job Sheet 3–5)
- Kemampuan Job Sheet 4 (INSERT/SELECT/UPDATE/DELETE) dan Job Sheet 7 (form)

## C. Langkah Kerja Terpandu

### Bagian 1 — Pola arsitektur (30 menit)

Struktur file yang dianjurkan — **fungsi database di atas, tampilan di bawah**:

```
aplikasi_penjualan.py
├── FUNGSI DATABASE : koneksi(), tambah(), ambil_semua(), ubah(), hapus()
└── TAMPILAN        : form input, tabel data, aksi hapus/ubah
```

### Bagian 2 — Tulis fungsi database (45 menit)

```python
import sqlite3

def koneksi():
    return sqlite3.connect("toko.db")

def tambah(tanggal, pelanggan, produk, jumlah, harga):
    con = koneksi()
    con.execute(
        "INSERT INTO penjualan (tanggal, pelanggan, produk, jumlah, harga) VALUES (?, ?, ?, ?, ?)",
        (tanggal, pelanggan, produk, jumlah, harga),
    )
    con.commit(); con.close()

def ambil_semua(cari=""):
    con = koneksi()
    if cari:
        df = con.execute(
            "SELECT * FROM penjualan WHERE pelanggan LIKE ? OR produk LIKE ? ORDER BY id DESC",
            (f"%{cari}%", f"%{cari}%"),
        ).fetchall()
    else:
        df = con.execute("SELECT * FROM penjualan ORDER BY id DESC").fetchall()
    con.close()
    return df

def hapus(id_trx):
    con = koneksi()
    con.execute("DELETE FROM penjualan WHERE id = ?", (id_trx,))
    con.commit(); con.close()
```

### Bagian 3 — Rakit tampilan (90 menit)

```python
import streamlit as st

st.title("Aplikasi Pencatatan Penjualan")

# --- tambah data (Create) ---
with st.form("form_input"):
    tanggal    = st.date_input("Tanggal")
    pelanggan  = st.text_input("Nama Pelanggan")
    produk     = st.selectbox("Produk", ["Buku Tulis", "Pulpen", "Tas", "Kertas HVS"])
    jumlah     = st.number_input("Jumlah", min_value=1, value=1)
    harga      = st.number_input("Harga Satuan (Rp)", min_value=0, value=5000, step=500)
    simpan     = st.form_submit_button("Simpan")

if simpan:
    if pelanggan.strip() == "":
        st.error("Nama pelanggan tidak boleh kosong.")
    else:
        tambah(str(tanggal), pelanggan.strip(), produk, jumlah, harga)
        st.success("Transaksi tersimpan.")

# --- lihat + cari (Read) ---
cari = st.text_input("Cari pelanggan / produk")
st.dataframe(ambil_semua(cari), use_container_width=True)

# --- hapus (Delete) ---
id_hapus = st.number_input("ID yang dihapus", min_value=0, value=0)
if st.button("Hapus") and id_hapus > 0:
    hapus(int(id_hapus))
    st.warning(f"Data ID {id_hapus} dihapus.")
```

### Bagian 4 — Update (45 menit)

Tambahkan fungsi `ubah(id, kolom, nilai_baru)` dengan `UPDATE penjualan SET {kolom} = ? WHERE id = ?`
(diajarkan langsung oleh dosen; `kolom` **harus** dibatasi daftar putih seperti `["jumlah", "harga"]`
karena nama kolom tidak bisa dikirim lewat parameter `?`).

Uji fitur ubah lewat input ID + kolom + nilai baru.

## D. Tugas Mandiri

Gabungkan semuanya menjadi `aplikasi_penjualan.py` versi lengkap Anda:

1. Empat operasi CRUD bisa dijalankan dari satu aplikasi.
2. Validasi: nama wajib diisi, jumlah ≥ 1, harga ≥ 0.
3. Pencarian bekerja tanpa mengganggu form.
4. Bandingkan hasil akhir Anda dengan aplikasi contoh dosen (`demo_penjualan.py`) — tuliskan 2 perbedaan pendekatan yang Anda temukan.

## E. Kriteria Selesai

- [ ] Tambah, lihat, cari, ubah, hapus semuanya berfungsi pada satu aplikasi
- [ ] Data bertahan setelah aplikasi ditutup dan dijalankan lagi (cek file `toko.db`)
- [ ] Validasi menolak input kosong/negatif
- [ ] Kode tersusun rapi: fungsi database terpisah dari bagian tampilan

## F. Pertanyaan Refleksi

1. Apa bedanya menyimpan di `st.session_state` (minggu lalu) dengan menyimpan di SQLite sekarang?
2. Operasi CRUD mana yang paling berisiko jika tanpa konfirmasi? Bagaimana aplikasi nyata mengatasinya?
