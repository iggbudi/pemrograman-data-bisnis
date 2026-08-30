# Job Sheet 12 — Mengamankan dan Men-deploy Aplikasi ke Internet

**Mata Kuliah:** Pemrograman Komputer Bisnis (351-221-302) · **Semester:** III
**Alokasi Waktu:** Terstruktur 4 × 45' · Mandiri 2 × 45'
**KAD:** Mahasiswa dapat mengamankan dan men-deploy aplikasi ke internet
**Bahan Kajian:** Login sederhana dengan st.secrets; dasar Git dan GitHub; deploy ke Streamlit Community Cloud

## A. Tujuan Praktik

1. Mahasiswa memahami bahwa kode di internet bisa dibaca siapa saja, dan menerapkan login sederhana dengan kredensial yang **tidak ditulis di kode**.
2. Mahasiswa mengunggah proyeknya ke GitHub (repositori publik kode, bukan data).
3. Mahasiswa men-deploy aplikasinya ke Streamlit Community Cloud sehingga bisa diakses siapa pun lewat URL.

## B. Alat dan Bahan

- Akun GitHub (github.com) dan akun share.streamlit.io (login dengan GitHub)
- Aplikasi multi-halaman dari Job Sheet 11
- File `requirements.txt` di root proyek berisi: `streamlit`, `pandas`, `openpyxl`

## C. Langkah Kerja Terpandu

### Bagian 1 — Login sederhana dengan st.secrets (60 menit)

Buat folder `.streamlit` di proyek, isi file `secrets.toml`:

```toml
ADMIN_PASSWORD = "rahasia123"
```

Di awal aplikasi utama:

```python
import streamlit as st

st.set_page_config(page_title="Toko Berkah", page_icon="🏪")

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    password = st.text_input("Password admin", type="password")
    if st.button("Masuk"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Password salah.")
    st.stop()   # hentikan sisa aplikasi sampai berhasil login

# --- aplikasi asli dimulai di sini ---
st.title("Aplikasi Toko Berkah")
```

File `secrets.toml` **wajib** masuk `.gitignore` (jangan pernah diunggah ke GitHub):

```
.streamlit/secrets.toml
toko.db
```

Di Streamlit Cloud nanti, nilai yang sama diisi lewat menu **Manage app → Settings → Secrets**.

### Bagian 2 — Unggah ke GitHub (60 menit)

```bash
git init -b main
git add .
git commit -m "Aplikasi penjualan toko berkah"
git remote add origin https://github.com/USERNAME/nama-repo.git
git push -u origin main
```

Konsep yang harus dipahami: **commit** = rekaman kondisi proyek pada satu titik; **push** = mengirim rekaman itu ke GitHub. Jika tak sempat memasang Git, GitHub web juga menerima *Add file → Upload files* — cara sah untuk mahasiswa dan cukup untuk minggu ini.

### Bagian 3 — Deploy ke Streamlit Community Cloud (60 menit)

1. Buka **share.streamlit.io** → login dengan GitHub → **Create app** → *Deploy a public app from GitHub*.
2. Isi: **Repository** = `USERNAME/nama-repo`, **Branch** = `main`, **Main file** = nama file aplikasi utama (mis. `aplikasi_penjualan.py`).
3. Klik **Deploy** — tunggu 1–2 menit hingga URL `https://...streamlit.app` aktif.
4. Jika aplikasi error saat online, buka **Manage app → Logs** — pesan error di sana persis seperti di terminal lokal.
5. Isi Secrets di Streamlit Cloud (sama seperti `secrets.toml`) agar fitur login bekerja.

### Bagian 4 — Alur kerja pembaruan (30 menit)

Ubah sesuatu kecil (mis. teks beranda) → `git add . && git commit -m "ubah teks beranda" && git push` → amati aplikasi online ter-update sendiri dalam ±1 menit. **Inilah alur kerja profesional: edit → commit → push → otomatis tayang.**

## D. Tugas Mandiri

1. Pasang login password di aplikasi Anda (kredensial via secrets, bukan di kode).
2. Deploy aplikasi Anda dan pastikan URL hidup.
3. Uji dari HP: buka URL aplikasi, lakukan satu transaksi.
4. Catat: apa yang terjadi pada data transaksi yang Anda buat di aplikasi online setelah Anda **redeploy**? (Petunjuk: filesystem cloud bersifat sementara — jawabannya jadi bahan diskusi minggu 14 tentang database cloud.)

## E. Kriteria Selesai

- [ ] Password tidak tertulis di file kode apa pun yang terunggah
- [ ] Repositori GitHub berisi kode + `requirements.txt`, tetapi **tidak** berisi `toko.db` dan `secrets.toml`
- [ ] Aplikasi online dengan URL `streamlit.app` dan bisa diakses dosen/teman
- [ ] Satu perubahan kecil berhasil diterapkan lewat alur commit-push

## F. Pertanyaan Refleksi

1. Mengapa password tidak boleh ditulis langsung di kode yang di-push ke GitHub?
2. Apa bedanya aplikasi Anda sekarang (URL publik, siapa pun bisa buka) dengan aplikasi minggu lalu (localhost)?
