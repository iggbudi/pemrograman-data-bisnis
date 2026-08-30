import streamlit as st
import sqlite3
import pandas as pd

# ============ FUNGSI DATABASE (materi minggu 3-6) ============

def koneksi():
    return sqlite3.connect("toko.db")

def buat_tabel():
    con = koneksi()
    con.execute("""
        CREATE TABLE IF NOT EXISTS penjualan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            pelanggan TEXT,
            produk TEXT,
            jumlah INTEGER,
            harga INTEGER
        )
    """)
    con.commit()
    con.close()

def tambah_data(tanggal, pelanggan, produk, jumlah, harga):
    con = koneksi()
    con.execute(
        "INSERT INTO penjualan (tanggal, pelanggan, produk, jumlah, harga) VALUES (?, ?, ?, ?, ?)",
        (tanggal, pelanggan, produk, jumlah, harga),
    )
    con.commit()
    con.close()

def ambil_semua():
    con = koneksi()
    df = pd.read_sql("SELECT * FROM penjualan ORDER BY tanggal DESC, id DESC", con)
    con.close()
    return df

def hapus_data(id):
    con = koneksi()
    con.execute("DELETE FROM penjualan WHERE id = ?", (id,))
    con.commit()
    con.close()

# ============ APLIKASI ============

buat_tabel()

st.title("Aplikasi Pencatatan Penjualan Toko")
st.caption("Contoh aplikasi bisnis: Python + Streamlit + SQLite")

menu = st.sidebar.radio("Menu", ["Input Penjualan", "Data Penjualan", "Statistik"])

if menu == "Input Penjualan":
    st.subheader("Tambah Transaksi Baru")

    with st.form("form_input"):
        tanggal = st.date_input("Tanggal")
        pelanggan = st.text_input("Nama Pelanggan")
        produk = st.selectbox("Produk", ["Buku Tulis", "Pulpen", "Tas", "Kertas HVS"])
        jumlah = st.number_input("Jumlah", min_value=1, value=1)
        harga = st.number_input("Harga Satuan (Rp)", min_value=0, value=5000, step=500)
        simpan = st.form_submit_button("Simpan")

    if simpan:
        if pelanggan.strip() == "":
            st.error("Nama pelanggan tidak boleh kosong.")
        else:
            tambah_data(str(tanggal), pelanggan.strip(), produk, jumlah, harga)
            st.success(f"Transaksi {pelanggan} tersimpan. Total: Rp {jumlah * harga:,}")

elif menu == "Data Penjualan":
    st.subheader("Semua Data Penjualan")

    df = ambil_semua()
    cari = st.text_input("Cari nama pelanggan / produk")
    if cari:
        pola = f"%{cari}%"
        con = koneksi()
        df = pd.read_sql(
            "SELECT * FROM penjualan WHERE pelanggan LIKE ? OR produk LIKE ? ORDER BY id DESC",
            con, params=(pola, pola),
        )
        con.close()

    df_tampil = df.copy()
    if not df_tampil.empty:
        df_tampil["total"] = df_tampil["jumlah"] * df_tampil["harga"]
    st.dataframe(df_tampil, use_container_width=True)

    st.subheader("Hapus Data")
    id_hapus = st.number_input("Ketik ID yang akan dihapus", min_value=0, value=0)
    if st.button("Hapus"):
        if id_hapus == 0:
            st.warning("Isi ID dulu.")
        else:
            hapus_data(int(id_hapus))
            st.success(f"Data dengan ID {id_hapus} sudah dihapus.")

else:
    st.subheader("Statistik Penjualan")

    df = ambil_semua()
    if df.empty:
        st.info("Belum ada data. Tambahkan lewat menu Input Penjualan.")
    else:
        df["total"] = df["jumlah"] * df["harga"]

        kiri, tengah, kanan = st.columns(3)
        kiri.metric("Jumlah Transaksi", len(df))
        tengah.metric("Total Omzet", f"Rp {df['total'].sum():,}")
        kanan.metric("Rata-rata / Transaksi", f"Rp {df['total'].mean():,.0f}")

        st.bar_chart(df.groupby("produk")["total"].sum())

        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Laporan")
        st.download_button(
            "Download laporan (Excel)",
            data=buffer.getvalue(),
            file_name="laporan_penjualan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
