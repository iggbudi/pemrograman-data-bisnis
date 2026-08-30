# Job Sheet 11 — Menu dan Aplikasi Multi-Halaman

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mendesain dan membuat menu aplikasi
**Bahan Kajian:** Aplikasi multi-halaman; navigasi menu dengan st.sidebar; memodifikasi menu aplikasi

## A. Tujuan Praktik

1. Mahasiswa memecah satu aplikasi besar menjadi beberapa halaman dengan navigasi yang rapi.
2. Mahasiswa menguasai dua cara multi-halaman: `st.sidebar` (satu file) dan folder `pages/` (multi-file).
3. Mahasiswa menata identitas aplikasi: judul tab, ikon, dan logo.

## B. Alat dan Bahan

- Aplikasi CRUD (Job Sheet 8) dan laporan (Job Sheet 9–10) yang sudah jadi — keduanya akan dijadikan halaman terpisah

## C. Langkah Kerja Terpandu

### Bagian 1 — Cara 1: menu di satu file dengan st.sidebar (60 menit)

Ini pola yang dipakai aplikasi contoh dosen. Bungkus tiap bagian aplikasi menjadi fungsi, lalu pilih lewat sidebar:

```python
import streamlit as st

st.set_page_config(page_title="Toko Berkah", page_icon="🏪", layout="wide")

st.title("Aplikasi Toko Berkah")
menu = st.sidebar.radio("Menu", ["Beranda", "Input Penjualan", "Data Penjualan", "Laporan"])

if menu == "Beranda":
    st.subheader("Selamat datang")
    st.write("Gunakan menu di sebelah kiri untuk berpindah halaman.")

elif menu == "Input Penjualan":
    st.subheader("Transaksi Baru")
    # ... pindahkan form input dari Job Sheet 8 ke sini

elif menu == "Data Penjualan":
    st.subheader("Semua Data")
    # ... tabel + pencarian + hapus dari Job Sheet 8

elif menu == "Laporan":
    st.subheader("Laporan & Grafik")
    # ... metric + grafik + unduh dari Job Sheet 9-10
```

Keunggulan cara ini: satu file, mudah dibagikan. Kekurangan: file membesar. Untuk aplikasi kelas (±150 baris) ini masih nyaman.

### Bagian 2 — Cara 2: folder pages/ (60 menit)

```
proyek_toko/
├── beranda.py        ← dijalankan dengan: streamlit run beranda.py
└── pages/
    ├── 1_⃣_Input_Penjualan.py
    ├── 2_📋_Data_Penjualan.py
    └── 3_📈_Laporan.py
```

- Streamlit otomatis membuat menu di sidebar dari isi folder `pages/` — urutan mengikuti angka awalan, label mengikuti nama file.
- Tiap file halaman adalah aplikasi mandiri: cukup mulai dengan `import streamlit as st` lalu tulis kontennya.
- Untuk berbagi data/fungsi antar halaman, buat file `fungsi_db.py` dan panggil dengan `from fungsi_db import tambah, ambil_semua`.

### Bagian 3 — Pemilihan otomatis & polish (60 menit)

1. Ganti `st.sidebar.radio` dengan `st.navigation`/`st.Page` (versi terbaru) atau `st.sidebar.selectbox` — bandingkan nuansanya.
2. Tambahkan `st.set_page_config(...)` di setiap halaman (judul + ikon berbeda per halaman).
3. Tambahkan `st.logo("logo.png")` atau caption toko di sidebar.
4. Perhatikan **state antar halaman**: `st.session_state` masih berlaku lintas halaman — uji dengan counter sederhana di dua halaman.

## D. Tugas Mandiri

1. Jadikan aplikasi penjualan Anda aplikasi 4 halaman: **Beranda** (sambutan + metric singkat), **Input**, **Data**, **Laporan**.
2. Pilih salah satu cara (satu file vs `pages/`) dan tuliskan alasannya di komentar kode paling atas.
3. Beri setiap halaman judul tab browser yang berbeda (`set_page_config`).
4. Uji: input transaksi di halaman Input → data langsung muncul di halaman Data dan Laporan.

## E. Kriteria Selesai

- [ ] Aplikasi memiliki minimal 4 halaman yang bisa dinavigasi
- [ ] Formulir, tabel, dan laporan tidak lagi menumpuk dalam satu layar
- [ ] Data yang diinput di satu halaman langsung terlihat di halaman lain
- [ ] Judul dan ikon aplikasi tampil di tab browser

## F. Pertanyaan Refleksi

1. Kapan satu file cukup, dan kapan lebih baik dipecah ke folder `pages/`?
2. Kenapa aplikasi bisnis nyata hampir selalu punya halaman beranda/menu, bukan langsung form?
