# Job Sheet 1 — Mengenal Data dan Aplikasi Bisnis

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat menjelaskan tentang data dan database
**Bahan Kajian:** Pengertian data, manajemen data, desain database

## A. Tujuan Praktik

1. Mahasiswa mampu membedakan **data**, **informasi**, dan **database** dengan contoh nyata.
2. Mahasiswa berhasil memasang Python dan Streamlit di komputernya sendiri.
3. Mahasiswa menjalankan aplikasi Streamlit pertamanya dan memahami bahwa aplikasi web dibuat dari sebuah file teks (kode).

## B. Alat dan Bahan

- Komputer dengan Windows/macOS/Linux
- Python 3.10+ dari [python.org](https://www.python.org/downloads/) (saat install, centang *Add Python to PATH*)
- Koneksi internet untuk `pip install`
- Editor teks: Visual Studio Code (disarankan)

## C. Langkah Kerja Terpandu

### Bagian 1 — Diskusi: data di sekitar kita (30 menit)

Dengan dosen, jawab bersama: transaksi apa saja yang dicatat sebuah toko kelontong?
Tuliskan minimal 5 jenis datanya (contoh: tanggal, nama pelanggan, produk, jumlah, harga).
Pisahkan mana yang berubah-ubah (transaksi) dan mana yang relatif tetap (produk).

### Bagian 2 — Instalasi (60 menit)

```bash
python --version        # pastikan Python terpasang
pip install streamlit   # pasang Streamlit
streamlit hello         # aplikasi contoh bawaan; ketik Ctrl+C untuk berhenti
```

Jika `pip` tidak dikenali, coba `python -m pip install streamlit`.

### Bagian 3 — Aplikasi pertama (60 menit)

Buat file baru bernama `kartu_toko.py`, isi dengan:

```python
import streamlit as st

st.title("Toko Sembako Berkah")
st.write("Selamat datang di aplikasi pencatatan penjualan kami.")

c1, c2, c3 = st.columns(3)
c1.metric("Produk Terdaftar", 42)
c2.metric("Transaksi Hari Ini", 17)
c3.metric("Omzet Hari Ini", "Rp 985.000")

st.caption("Aplikasi latihan mata kuliah Pemrograman Komputer Bisnis")
```

Jalankan:

```bash
streamlit run kartu_toko.py
```

Amati: buka `http://localhost:8501` di browser, ubah angka di kode, simpan file, lalu klik **Rerun** di browser. Ulangi sampai terbiasa siklus *edit → simpan → rerun*.

## D. Tugas Mandiri

1. Kunjungi satu usaha kecil di sekitar kampus/rumah (warung, koperasi, photocopier).
2. Catat: jenis data apa saja yang mereka catat, dan dengan alat apa (buku, Excel, HP).
3. Rancang **satu tabel** untuk usaha tersebut: tulis nama kolom dan isi contohnya di kertas/tabel.
4. Modifikasi `kartu_toko.py`: ganti nama toko, ganti 3 metric dengan data dari usaha yang Anda amati.

## E. Kriteria Selesai

- [ ] `streamlit hello` berhasil dijalankan
- [ ] `kartu_toko.py` tampil di browser tanpa error
- [ ] Metric menampilkan data hasil observasi usaha nyata
- [ ] Rancangan tabel usaha (min. 5 kolom) siap didiskusikan di pertemuan berikutnya

## F. Pertanyaan Refleksi

1. Apa bedanya *data* (angka mentah transaksi) dengan *informasi* (metric "Omzet Hari Ini")?
2. Mengapa data sebaiknya disimpan di database, bukan di dalam kode aplikasi?
