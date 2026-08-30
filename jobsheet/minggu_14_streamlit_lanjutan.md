# Job Sheet 13 — Streamlit Lanjutan: Upload Excel, Database Cloud, dan Optimasi

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengembangkan aplikasi bisnis tingkat lanjut
**Bahan Kajian:** Upload data Excel (st.file_uploader); koneksi database cloud Turso; pengelolaan kredensial aplikasi; cache

## A. Tujuan Praktik

1. Mahasiswa menerima **data Excel dari pengguna** dan mengimpornya ke database (kebutuhan administrasi yang sangat umum).
2. Mahasiswa memindahkan database dari file lokal ke **database cloud Turso** agar data aplikasi online bersifat permanen.
3. Mahasiswa memakai `st.cache_data` agar aplikasi tidak membebani database berulang-ulang.

## B. Alat dan Bahan

- Aplikasi yang sudah ter-deploy (Job Sheet 12)
- Akun [turso.tech](https://turso.tech) (gratis) + `pip install libsql-experimental`
- Satu file Excel berisi kolom: `tanggal, pelanggan, produk, jumlah, harga` (buat contohnya dari hasil ekspor Job Sheet 10)

## C. Langkah Kerja Terpandu

### Bagian 1 — Import Excel ke database (60 menit)

```python
import streamlit as st
import pandas as pd
import sqlite3

st.subheader("Import Transaksi dari Excel")
file = st.file_uploader("Pilih file Excel", type=["xlsx"])

if file is not None:
    df = pd.read_excel(file)
    st.dataframe(df.head(10))   # pratinjau dulu, jangan langsung simpan!

    if st.button("Import ke Database"):
        con = sqlite3.connect("toko.db")
        n = 0
        for _, b in df.iterrows():
            if str(b["pelanggan"]).strip() == "" or int(b["jumlah"]) <= 0:
                continue   # lewati baris tidak valid
            con.execute(
                "INSERT INTO penjualan (tanggal, pelanggan, produk, jumlah, harga) VALUES (?, ?, ?, ?, ?)",
                (str(b["tanggal"])[:10], str(b["pelanggan"]), str(b["produk"]),
                 int(b["jumlah"]), int(b["harga"])),
            )
            n += 1
        con.commit(); con.close()
        st.success(f"{n} baris berhasil diimport.")
```

Prinsip: **pratinjau → validasi → import**, dan selalu laporkan berapa baris yang masuk.

### Bagian 2 — Database cloud Turso (90 menit)

1. Daftar di turso.tech → buat database, mis. `toko-cloud`.
2. Dari dashboard, salin **URL** database dan **token** autentikasi.
3. Pasang pustaka klien: `pip install libsql-experimental`, lalu uji lokal:

```python
import libsql_experimental as libsql

koneksi = libsql.connect(
    "libsql://nama-database-anda.turso.io",
    auth_token="TOKEN_ANDA",
)
print(koneksi.execute("SELECT 1").fetchall())
```

4. Buat tabel yang sama seperti lokal (`CREATE TABLE ...`) — **SQL-nya identik**, karena Turso kompatibel SQLite.
5. Pindahkan kredensial ke `.streamlit/secrets.toml` (dan Secrets di Streamlit Cloud):

```toml
TURSO_URL = "libsql://nama-database-anda.turso.io"
TURSO_TOKEN = "TOKEN_ANDA"
```

6. Refaktor fungsi `koneksi()` aplikasi agar berubah sumber hanya di satu tempat:

```python
import streamlit as st

def koneksi():
    import libsql_experimental as libsql
    return libsql.connect(st.secrets["TURSO_URL"], auth_token=st.secrets["TURSO_TOKEN"])
```

7. Deploy ulang → input transaksi di aplikasi online → tutup browser → buka lagi: **data tetap ada**. Masalah "data hilang saat redeploy" dari Job Sheet 12 selesai.

### Bagian 3 — Cache (45 menit)

```python
import streamlit as st
import pandas as pd

@st.cache_data(ttl=60)          # simpan hasil 60 detik
def ambil_laporan():
    con = koneksi()
    df = pd.read_sql("SELECT * FROM penjualan", con)
    con.close()
    return df
```

Setiap pengunjung halaman laporan tidak lagi membebani database; cache pecah otomatis setelah `ttl` atau saat data berubah (`ambil_laporan.clear()` setelah operasi INSERT/UPDATE/DELETE).

## D. Tugas Mandiri

1. Fitur import Excel berjalan dengan pratinjau, validasi, dan laporan jumlah baris.
2. Aplikasi online Anda kini tersambung ke Turso: buktikan dengan input data dari HP, lalu cek datanya dari komputer lain.
3. Terapkan cache pada halaman laporan dan amati perbedaan kecepatan saat dibuka ulang.
4. Siapkan rencana **tugas akhir** (minggu 15): pilih kasus UKM, daftar tabel, dan halaman aplikasi — presentasikan singkat di akhir pertemuan.

## E. Kriteria Selesai

- [ ] File Excel nyata berhasil diimport dengan validasi dan tidak menggandakan data saat tombol ditekan dua kali
- [ ] Aplikasi lokal dan online memakai fungsi koneksi yang sama (Turso), kredensial ada di secrets
- [ ] Data transaksi di aplikasi online bertahan setelah redeploy
- [ ] Rencana tugas akhir (kasus, tabel, halaman) sudah tertulis

## F. Pertanyaan Refleksi

1. Mengapa SQL yang Anda tulis sejak minggu 3 tetap berlaku di database cloud Turso?
2. Untuk tugas akhir Anda: data apa yang paling berisiko hilang jika masih memakai file SQLite lokal di hosting gratis?
