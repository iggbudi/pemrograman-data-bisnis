# Job Sheet 9 — Laporan dan Grafik Penjualan

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mendesain dan membuat laporan
**Bahan Kajian:** Laporan agregasi dengan st.metric; grafik penjualan (st.bar_chart); statistik penjualan per produk

## A. Tujuan Praktik

1. Mahasiswa menyusun **laporan ringkasan**: angka kunci (metric) dan grafik dari data transaksi.
2. Mahasiswa mengolah data dengan pandas (`groupby`, `sum`) untuk keperluan laporan.
3. Mahasiswa memahami alur: *data mentah di database → agregasi → visual yang bisa dibaca pengelola toko*.

## B. Alat dan Bahan

- Aplikasi CRUD + database terisi data (Job Sheet 8; atau pakai `seed_data.py` milik dosen untuk data satu bulan)
- `pandas` (sudah terpasang bersama Streamlit)

## C. Langkah Kerja Terpandu

### Bagian 1 — Membaca data sebagai DataFrame pandas (30 menit)

```python
import streamlit as st
import sqlite3
import pandas as pd

koneksi = sqlite3.connect("toko.db")
df = pd.read_sql("SELECT * FROM penjualan", koneksi)
koneksi.close()
df["total"] = df["jumlah"] * df["harga"]
st.dataframe(df, use_container_width=True)
```

`pd.read_sql` langsung mengubah hasil query menjadi tabel pandas — fondasi semua laporan.

### Bagian 2 — Kartu angka kunci (45 menit)

```python
kiri, tengah, kanan = st.columns(3)
kiri.metric("Jumlah Transaksi", len(df))
tengah.metric("Total Omzet", f"Rp {df['total'].sum():,}")
kanan.metric("Rata-rata / Transaksi", f"Rp {df['total'].mean():,.0f}")
```

Pilih angka kunci dengan logika pembaca laporan: pemilik toko ingin tahu *omzet*, *jumlah transaksi*, dan *nilai rata-rata* — bukan 59 baris data mentah.

### Bagian 3 — Grafik (60 menit)

```python
st.subheader("Omzet per Produk")
st.bar_chart(df.groupby("produk")["total"].sum())

st.subheader("Tren Omzet Harian")
df["tanggal"] = pd.to_datetime(df["tanggal"])
st.line_chart(df.groupby("tanggal")["total"].sum())

st.subheader("Porsi per Produk")
st.dataframe(
    df.groupby("produk")["total"].sum().sort_values(ascending=False),
    use_container_width=True,
)
```

Panduan memilih grafik: **perbandingan kategori** → bar chart; **perkembangan waktu** → line chart; **angka tunggal** → metric.

### Bagian 4 — Filter pada laporan (45 menit)

Letakkan `st.selectbox("Pilih produk", ["Semua", ...])` di atas grafik, lalu filter DataFrame:

```python
pilihan = st.selectbox("Pilih produk", ["Semua"] + sorted(df["produk"].unique().tolist()))
df_laporan = df if pilihan == "Semua" else df[df["produk"] == pilihan]
```

Semua metric dan grafik di bawahnya otomatis mengikuti pilihan — satu baris filter, seluruh laporan berubah.

## D. Tugas Mandiri

1. Tambahkan metric keempat: **produk terlaris** (nama produk dengan `total` terbesar).
2. Buat bar chart kedua: **jumlah transaksi per produk** (bukan omzet) — perhatikan bedanya dengan `sum`.
3. Lengkapi laporan dengan filter rentang tanggal (`st.date_input` dua buah, gunakan `BETWEEN` atau filter pandas).
4. Tuliskan 2 kalimat **kesimpulan bisnis** dari laporan Anda (contoh: "Kertas HVS menyumbang omzet terbesar meski transaksinya paling sedikit").

## E. Kriteria Selesai

- [ ] Tiga metric utama (transaksi, omzet, rata-rata) tampil benar
- [ ] Bar chart per produk dan line chart harian tampil dari data nyata
- [ ] Filter produk mengubah seluruh laporan sekaligus
- [ ] Kesimpulan bisnis tertulis dan logis dengan angka di laporan

## F. Pertanyaan Refleksi

1. Mengapa laporan bisnis menampilkan agregat, bukan tabel mentah?
2. Grafik apa yang akan Anda pilih untuk melihat efek *diskon akhir bulan* terhadap omzet harian? Mengapa?
