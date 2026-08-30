# Aplikasi Pencatatan Penjualan (Streamlit + SQLite)

Contoh aplikasi bisnis sederhana untuk pembelajaran mata kuliah **Pemrograman Komputer Bisnis**
(Prodi Administrasi Bisnis): input transaksi, pencarian, hapus data, statistik, grafik,
dan unduh laporan Excel — dibangun dengan Python + Streamlit + SQLite tanpa konfigurasi server.

## Cara Menjalankan

```bash
pip install -r requirements.txt
python seed_data.py        # opsional: isi 1 bulan data transaksi contoh
streamlit run demo_penjualan.py
```

## Struktur

| File | Isi |
|---|---|
| `demo_penjualan.py` | Aplikasi utama: form input, tabel + pencarian, hapus, statistik & unduh Excel |
| `seed_data.py` | Mengisi `toko.db` dengan data contoh (Agustus 2026) |

Database `toko.db` dibuat otomatis saat aplikasi pertama dijalankan.
