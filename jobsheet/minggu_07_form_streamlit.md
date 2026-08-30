# Job Sheet 7 — Mendesain Form Aplikasi dengan Streamlit

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mendesain dan membuat tampilan form sesuai kebutuhan
**Bahan Kajian:** Dasar Streamlit: teks, tabel, metric; mendesain tampilan form; membuat form dengan st.form dan komponen input

## A. Tujuan Praktik

1. Mahasiswa mengenal komponen input Streamlit dan memilih komponen yang tepat untuk tiap jenis data.
2. Mahasiswa membangun form input transaksi dengan `st.form` dan memahami mengapa form mencegah "rerun" berlebihan.
3. Mahasiswa menyimpan data sementara di `st.session_state` (belum ke database — itu Job Sheet 8).

## B. Alat dan Bahan

- Python + Streamlit (Job Sheet 1)
- Tidak butuh database pada job sheet ini — fokus pada antarmuka

## C. Langkah Kerja Terpandu

### Bagian 1 — Mengenal komponen input (60 menit)

Buat `komponen.py` untuk mencoba semuanya sekaligus:

```python
import streamlit as st
from datetime import date

st.title("Pameran Komponen Input")

st.text_input("Nama pelanggan")
st.selectbox("Produk", ["Buku Tulis", "Pulpen", "Tas", "Kertas HVS"])
st.multiselect("Fasilitas", ["Dikemas", "Diantar", "Difakturkan"])
st.number_input("Jumlah", min_value=1, max_value=100)
st.slider("Diskon (%)", 0, 25)
st.date_input("Tanggal transaksi", value=date.today())
st.checkbox("Pelanggan member?")
st.text_area("Catatan pesanan")
st.radio("Metode bayar", ["Tunai", "Transfer", "QRIS"])
st.file_uploader("Unggah foto nota (latihan)")
if st.button("Tombol Uji"):
    st.balloons()
```

Diskusikan: untuk data **nama produk** mengapa `selectbox` lebih baik daripada `text_input`?
(Konsistensi ejaan — data tidak bisa "Buku tulis", "BUKU TULIS", "bukutulis" berantakan.)

### Bagian 2 — Form input transaksi dengan session_state (120 menit)

Buat file `form_penjualan.py`:

```python
import streamlit as st
from datetime import date

st.title("Input Penjualan — Mode Latihan")

# wadah data sementara (hilang saat aplikasi ditutup)
if "pesanan" not in st.session_state:
    st.session_state.pesanan = []

with st.form("form_transaksi"):
    st.subheader("Transaksi Baru")
    tanggal = st.date_input("Tanggal", value=date.today())
    pelanggan = st.text_input("Nama Pelanggan")
    produk = st.selectbox("Produk", ["Buku Tulis", "Pulpen", "Tas", "Kertas HVS"])
    jumlah = st.number_input("Jumlah", min_value=1, value=1)
    harga = st.number_input("Harga Satuan (Rp)", min_value=0, value=5000, step=500)
    simpan = st.form_submit_button("Simpan Transaksi")

if simpan:
    if pelanggan.strip() == "":
        st.error("Nama pelanggan tidak boleh kosong.")
    else:
        st.session_state.pesanan.append(
            {"tanggal": str(tanggal), "pelanggan": pelanggan.strip(),
             "produk": produk, "jumlah": jumlah, "total": jumlah * harga}
        )
        st.success(f"Transaksi {pelanggan} tersimpan. Total: Rp {jumlah * harga:,}")

st.subheader("Daftar Pesanan Sesi Ini")
st.dataframe(st.session_state.pesanan, use_container_width=True)
st.metric("Total Sesi Ini", sum(p["total"] for p in st.session_state.pesanan))
```

Perhatikan dua perilaku kunci:

1. **`st.form`** mengumpulkan semua input dan baru memproses saat `form_submit_button` ditekan — tanpa form, mengubah satu input memicu aplikasi berjalan ulang terus-menerus.
2. **`st.session_state`** adalah memori aplikasi: data bertahan saat pindah-pindah halaman, tapi hilang saat aplikasi ditutup. Di minggu berikutnya datanya dipindah ke database agar permanen.

## D. Tugas Mandiri

1. Tambahkan field `st.text_area` "Catatan" dan `st.checkbox` "Member?" ke form; keduanya ikut tersimpan ke daftar pesanan.
2. Tambahkan validasi kedua: tolak transaksi jika `jumlah * harga == 0`.
3. Tambahkan tombol "Kosongkan Daftar" yang menghapus `st.session_state.pesanan`.
4. Desain ulang tata letak: letakkan form di kolom kiri dan daftar pesanan di kolom kanan dengan `st.columns`.

## E. Kriteria Selesai

- [ ] Seluruh komponen input dicoba dan perilakunya dipahami
- [ ] Form hanya memproses data saat tombol Simpan ditekan
- [ ] Nama kosong ditolak dengan pesan `st.error`
- [ ] Daftar pesanan dan total bertahan setelah beberapa transaksi dimasukkan

## F. Pertanyaan Refleksi

1. Kapan memilih `selectbox`, kapan memilih `text_input`? Beri contoh data masing-masing.
2. Apa risiko jika data transaksi hanya disimpan di `session_state` untuk aplikasi bisnis sungguhan?
