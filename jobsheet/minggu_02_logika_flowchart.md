# Job Sheet 2 — Logika Program dan Diagram Alir

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat membuat diagram alir suatu logika program
**Bahan Kajian:** Logika program, macam program tools, diagram alir

## A. Tujuan Praktik

1. Mahasiswa mampu menggambar flowchart untuk aturan bisnis sederhana.
2. Mahasiswa mampu menerjemahkan flowchart menjadi kode Python (percabangan, perulangan).
3. Mahasiswa mampu menampilkan hasil logika tersebut sebagai aplikasi web Streamlit.

## B. Alat dan Bahan

- Python + Streamlit (dari Job Sheet 1)
- Kertas atau [draw.io](https://app.diagrams.net) untuk menggambar flowchart
- Simbol yang dipakai: **oval** (mulai/selesai), **jajar genjang** (input/output), **belah ketupat** (keputusan), **persegi panjang** (proses)

## C. Langkah Kerja Terpandu

### Bagian 1 — Kasus: aturan diskon toko (45 menit)

Aturan bisnis:

- Total belanja ≥ Rp 1.000.000 → diskon 15%
- Total belanja ≥ Rp 500.000 → diskon 10%
- Selain itu → tanpa diskon

Gambar flowchart-nya terlebih dahulu (jangan menulis kode sebelum flowchart selesai!).

### Bagian 2 — Terjemahkan ke aplikasi Streamlit (90 menit)

Buat file `diskon.py`:

```python
import streamlit as st

st.title("Kalkulator Diskon Toko")

total = st.number_input("Total belanja (Rp)", min_value=0, value=500000, step=50000)

diskon = 0
if total >= 1_000_000:
    diskon = 0.15
elif total >= 500_000:
    diskon = 0.10

bayar = total - (total * diskon)

st.metric("Diskon", f"{diskon:.0%}")
st.metric("Total Bayar", f"Rp {bayar:,.0f}")
```

Jalankan `streamlit run diskon.py`, lalu uji dengan 3 nilai: 400.000, 750.000, dan 1.500.000.
Pastikan hasilnya sesuai flowchart. Jika tidak sama, perbaiki **kode-nya**, bukan ujiannya.

### Bagian 3 — Menambah perulangan (45 menit)

Tambahkan di bawahnya: simulasi menabung modal usaha.

```python
st.subheader("Simulasi Nabung Modal")
target = st.number_input("Target modal (Rp)", min_value=0, value=5_000_000, step=500_000)
setoran = st.number_input("Setoran per bulan (Rp)", min_value=0, value=500_000, step=100_000)

bulan = 0
saldo = 0
while saldo < target:
    saldo += setoran
    bulan += 1

st.success(f"Target tercapai dalam {bulan} bulan.")
```

Diskusikan: apa yang terjadi jika `setoran` diisi 0? (Kode macet selamanya — ini namanya *infinite loop*.) Perbaiki dengan syarat aman, misalnya `while saldo < target and bulan < 120:`.

## D. Tugas Mandiri

1. Buat flowchart untuk aturan stok: *"jika stok produk < 10, tampilkan peringatan RESTOCK; jika tidak, tampilkan AMAN"*.
2. Terjemahkan menjadi aplikasi `cek_stok.py` dengan `st.number_input` dan `st.error`/`st.success`.
3. Uji dengan minimal 3 nilai berbeda dan cocokkan dengan flowchart Anda.

## E. Kriteria Selesai

- [ ] Flowchart diskon digambar lengkap dengan simbol yang benar
- [ ] `diskon.py` menghasilkan diskon sesuai aturan pada 3 nilai uji
- [ ] `cek_stok.py` berjalan sesuai flowchart yang dibuat sendiri
- [ ] Mahasiswa dapat menjelaskan perbedaan `if/elif/else` dan `while`

## F. Pertanyaan Refleksi

1. Mengapa flowchart dibuat **sebelum** kode?
2. Di bagian mana aplikasi bisnis nyata membutuhkan percabangan? Sebutkan 3 contoh.
