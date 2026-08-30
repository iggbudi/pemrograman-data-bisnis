# Job Sheet 4 — Mengelola Data Record dalam Tabel

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengelola data record dalam tabel
**Bahan Kajian:** INSERT, SELECT, UPDATE, DELETE; mengurutkan (ORDER BY) dan mengelompokkan (GROUP BY) data record

## A. Tujuan Praktik

1. Mahasiswa menguasai empat operasi dasar data: **tambah (INSERT)**, **tampil (SELECT)**, **ubah (UPDATE)**, **hapus (DELETE)**.
2. Mahasiswa mampu mengurutkan hasil query (`ORDER BY`) dan mengelompokkan data (`GROUP BY`).
3. Mahasiswa menampilkan tabel database secara interaktif di Streamlit.

## B. Alat dan Bahan

- Database `toko.db` + tabel `produk` (dari Job Sheet 3)

## C. Langkah Kerja Terpandu

### Bagian 1 — Operasi record lewat skrip (90 menit)

Buat file `operasi_record.py` dan jalankan bertahap (`python operasi_record.py`):

```python
import sqlite3

koneksi = sqlite3.connect("toko.db")
cursor = koneksi.cursor()

# 1. INSERT - menambah data
produk_baru = [
    ("Buku Tulis",  "Alat Tulis", 5000,  100),
    ("Pulpen",      "Alat Tulis", 3000,  150),
    ("Tas",         "Tas",       25000,   40),
    ("Kertas HVS",  "Kertas",    45000,   60),
    ("Penghapus",   "Alat Tulis", 2000,  200),
]
cursor.executemany(
    "INSERT INTO produk (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)",
    produk_baru,
)

# 2. SELECT - menampilkan data
print("--- Semua produk ---")
for baris in cursor.execute("SELECT * FROM produk"):
    print(baris)

# 3. UPDATE - mengubah data (selalu dengan WHERE!)
cursor.execute("UPDATE produk SET harga = 5500 WHERE nama = 'Buku Tulis'")

# 4. DELETE - menghapus data (selalu dengan WHERE!)
cursor.execute("DELETE FROM produk WHERE nama = 'Penghapus'")

# 5. ORDER BY - mengurutkan
print("--- Urut harga termahal ---")
for baris in cursor.execute("SELECT nama, harga FROM produk ORDER BY harga DESC"):
    print(baris)

# 6. GROUP BY - mengelompokkan + agregasi
print("--- Jumlah produk per kategori ---")
for baris in cursor.execute(
    "SELECT kategori, COUNT(*) FROM produk GROUP BY kategori"
):
    print(baris)

koneksi.commit()
koneksi.close()
```

**Peringatan penting:** `UPDATE`/`DELETE` tanpa `WHERE` mengubah/menghapus **semua baris**. Biasakan menulis `WHERE` sebelum menulis perintahnya.

### Bagian 2 — Menampilkan & menambah data lewat aplikasi (90 menit)

Buat file `kelola_produk.py`:

```python
import streamlit as st
import sqlite3

st.title("Kelola Produk Toko")

koneksi = sqlite3.connect("toko.db")

# menampilkan semua produk
df = st.dataframe(
    koneksi.execute("SELECT * FROM produk ORDER BY nama").fetchall(),
    column_config={"0": "ID", "1": "Nama", "2": "Kategori", "3": "Harga", "4": "Stok"},
    use_container_width=True,
)

# form sederhana untuk menambah produk
nama = st.text_input("Nama produk")
kategori = st.selectbox("Kategori", ["Alat Tulis", "Tas", "Kertas", "Lainnya"])
harga = st.number_input("Harga", min_value=0)
stok = st.number_input("Stok", min_value=0)

if st.button("Simpan Produk"):
    if nama.strip() == "":
        st.error("Nama produk wajib diisi.")
    else:
        koneksi.execute(
            "INSERT INTO produk (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)",
            (nama, kategori, harga, stok),
        )
        koneksi.commit()
        st.success(f"Produk '{nama}' tersimpan.")
```

Perhatikan tanda `?` pada query — itu **parameter binding**, cara aman mengirim nilai dari user ke database (mencegah SQL injection). **Jangan pernah** menggabungkan string input user langsung ke query.

## D. Tugas Mandiri

1. Tambahkan ke `kelola_produk.py`: tombol dan input untuk **menghapus** produk berdasarkan ID.
2. Buat tampilan kedua yang menampilkan produk **urut stok paling sedikit** (`ORDER BY stok ASC`).
3. Tuliskan hasil query `GROUP BY kategori` (jumlah produk + rata-rata harga `AVG(harga)`) sebagai tabel mandiri.

## E. Kriteria Selesai

- [ ] `operasi_record.py` menjalankan INSERT, SELECT, UPDATE, DELETE, ORDER BY, GROUP BY
- [ ] Aplikasi dapat menambah produk baru dan produk langsung muncul setelah Rerun
- [ ] Fitur hapus berdasarkan ID berfungsi (uji: hapus lalu cek tabel)
- [ ] Mahasiswa dapat menjelaskan mengapa `WHERE` wajib pada UPDATE/DELETE

## F. Pertanyaan Refleksi

1. Apa yang terjadi jika tombol Simpan ditekan dua kali? Bagaimana mencegah data ganda?
2. Kapan `GROUP BY` berguna dalam laporan bisnis? Beri 2 contoh laporan.
