# Job Sheet 5 — Relasi Antar Tabel: Foreign Key, JOIN, dan View

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat merelasikan data antar tabel pada sebuah database
**Bahan Kajian:** Foreign key dan relasi antar tabel; menggabungkan tabel (JOIN); membuat view data

## A. Tujuan Praktik

1. Mahasiswa memahami mengapa data dibagi ke beberapa tabel yang berelasi (bukan satu tabel raksasa).
2. Mahasiswa membuat relasi dengan **foreign key** dan menggabungkan tabel dengan **JOIN**.
3. Mahasiswa membuat **view** sebagai "query tersimpan" yang bisa dipakai berulang.

## B. Alat dan Bahan

- Database `toko.db` dengan tabel `produk` (Job Sheet 3–4)

## C. Langkah Kerja Terpandu

### Bagian 1 — Memahami masalah (30 menit)

Jika satu tabel penjualan menyimpan "Buku Tulis, Rp 5000" di setiap baris transaksi, lalu harga berubah — data lama ikut berubah, padahal tidak seharusnya. Solusi: transaksi hanya menyimpan **ID produk** (foreign key), detail produk tinggal satu tempat di tabel `produk`.

### Bagian 2 — Membuat tabel berelasi (60 menit)

Buat file `buat_relasi.py`:

```python
import sqlite3

koneksi = sqlite3.connect("toko.db")
cursor = koneksi.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS penjualan (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        produk_id INTEGER NOT NULL,
        jumlah    INTEGER NOT NULL,
        tanggal   TEXT NOT NULL,
        FOREIGN KEY (produk_id) REFERENCES produk(id)
    )
""")

# data contoh: angka pertama adalah produk_id dari tabel produk
contoh = [
    (1, 3, "2026-08-01"),
    (2, 2, "2026-08-01"),
    (1, 5, "2026-08-02"),
    (4, 1, "2026-08-03"),
]
cursor.executemany(
    "INSERT INTO penjualan (produk_id, jumlah, tanggal) VALUES (?, ?, ?)",
    contoh,
)

koneksi.commit()
koneksi.close()
print("Tabel penjualan (berelasi ke produk) siap.")
```

> Catatan: angka `produk_id` pada data contoh mengikuti ID di tabel `produk` milik Anda —
> cek dulu dengan `SELECT * FROM produk`, sesuaikan contohnya.

### Bagian 3 — JOIN: menggabungkan tabel (60 menit)

```python
query = """
    SELECT penjualan.id, produk.nama, produk.harga,
           penjualan.jumlah, penjualan.tanggal,
           produk.harga * penjualan.jumlah AS total
    FROM penjualan
    JOIN produk ON produk.id = penjualan.produk_id
    ORDER BY penjualan.tanggal
"""
for baris in koneksi.execute(query):
    print(baris)
```

Bacaannya: *"ambil transaksi, dan untuk tiap transaksi ambil detail produk yang cocok"*. Tanpa JOIN, kolom `nama` dan `harga` tidak ada di tabel `penjualan`.

### Bagian 4 — View: menyimpan query (30 menit)

```python
koneksi.execute("""
    CREATE VIEW IF NOT EXISTS laporan_penjualan AS
    SELECT penjualan.tanggal, produk.nama, produk.harga * penjualan.jumlah AS total
    FROM penjualan JOIN produk ON produk.id = penjualan.produk_id
""")
koneksi.commit()

# view dipakai seperti tabel biasa:
for baris in koneksi.execute("SELECT * FROM laporan_penjualan"):
    print(baris)
```

### Bagian 5 — Tampilkan JOIN di Streamlit (30 menit)

Salin query JOIN di atas ke aplikasi `relasi.py` dan tampilkan dengan `st.dataframe(..., use_container_width=True)`.

## D. Tugas Mandiri

1. Buat tabel `pelanggan` (`id`, `nama`, `telepon`) lalu tambahkan kolom `pelanggan_id` pada `penjualan` sebagai tabel baru `penjualan_v2` dengan **dua** foreign key (`produk_id`, `pelanggan_id`).
2. Buat query JOIN **tiga tabel** (pelanggan + penjualan_v2 + produk).
3. Buat view `omzet_per_produk` berisi nama produk dan total penjualannya.

## E. Kriteria Selesai

- [ ] Tabel `penjualan` memiliki foreign key ke `produk`
- [ ] Query JOIN menampilkan nama produk (bukan hanya ID) dan kolom `total`
- [ ] View `laporan_penjualan` dapat di-SELECT seperti tabel biasa
- [ ] Aplikasi `relasi.py` menampilkan hasil JOIN di Streamlit

## F. Pertanyaan Refleksi

1. Mengapa transaksi menyimpan `produk_id`, bukan nama produk?
2. Apa yang terjadi pada query JOIN jika `produk_id` menunjuk produk yang tidak ada?
