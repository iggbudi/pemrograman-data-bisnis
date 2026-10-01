"""
MINGGU 5 - VALIDASI DATA DAN RELASI TABEL
Mata kuliah : Pemrograman Data Bisnis (Administrasi Bisnis, AB-2B)
Studi kasus : Catatan Penjualan Kedai Rasa (data simulasi)

MASALAH BISNIS
    Kalau kasir bisa mengetik harga 0, jumlah "dua", atau produk yang tidak
    ada di katalog, laporan omzet Kedai Rasa jadi salah. Data harus diperiksa
    SEBELUM disimpan.

YANG AKAN KITA BUAT
    Form "Tambah transaksi": pilih produk dari katalog, isi harga dan jumlah,
    lalu simpan. Data yang salah ditolak dengan pesan yang jelas.

TUJUAN: setelah praktik ini kamu mampu
    1. Memvalidasi input pengguna di Python (kosong, bukan angka, nol, negatif).
    2. Membuat aturan di database SQLite (NOT NULL, CHECK) sebagai pengaman kedua.
    3. Menghubungkan tabel products dan sales dengan FOREIGN KEY.

PETA ISI FILE (baca dari atas ke bawah)
    Bagian 1  Pengaturan dan data contoh
    Bagian 2  Database: tabel, aturan, dan relasi    <- inti materi
    Bagian 3  Validasi input di Python               <- inti materi
    Bagian 4  Menyimpan transaksi
    Bagian 5  Tampilan Streamlit (form)

Cara menjalankan:  streamlit run app.py
"""

from contextlib import closing
from pathlib import Path
import sqlite3

import streamlit as st

# =====================================================================
# BAGIAN 1 - PENGATURAN DAN DATA CONTOH
# =====================================================================
DB_PATH = Path(__file__).with_name("penjualan_m5.db")  # file database
SEED_PRODUCTS = [  # katalog awal: (nama, kategori, harga katalog)
    ("Kopi Susu", "Minuman", 15000),
    ("Roti Cokelat", "Makanan", 10000),
    ("Teh Lemon", "Minuman", 12000),
]

# =====================================================================
# BAGIAN 2 - DATABASE: TABEL, ATURAN, DAN RELASI
# =====================================================================
def get_connection():
    """Buka koneksi SQLite dan aktifkan pemeriksaan foreign key."""
    # Bagian teknis: cukup disalin, tidak perlu dipahami detailnya.
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # hasil query bisa dibaca per nama kolom
    # SQLite tidak memeriksa relasi kecuali diaktifkan dengan baris ini:
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_database():
    """Buat tabel products dan sales, lalu isi katalog contoh jika belum ada."""
    with closing(get_connection()) as connection:
        connection.executescript(
            """
            -- Tabel katalog: satu baris = satu produk
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- nomor unik produk
                name TEXT NOT NULL UNIQUE,             -- wajib diisi, tidak boleh kembar
                category TEXT NOT NULL,
                catalog_price INTEGER NOT NULL CHECK (catalog_price > 0)
            );
            -- Tabel transaksi: satu baris = satu penjualan
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                product_id INTEGER NOT NULL,           -- produk apa yang dijual
                unit_price INTEGER NOT NULL CHECK (unit_price > 0),  -- harga harus > 0
                quantity INTEGER NOT NULL CHECK (quantity > 0),      -- jumlah harus > 0
                -- total harus sama dengan harga x jumlah:
                total INTEGER NOT NULL CHECK (total = unit_price * quantity),
                -- RELASI: product_id wajib ada di tabel products
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO products (name, category, catalog_price)
            VALUES (?, ?, ?)
            """,
            SEED_PRODUCTS,
        )
        connection.commit()

def get_products():
    """Ambil katalog untuk pilihan produk di form."""
    with closing(get_connection()) as connection:
        return connection.execute(
            "SELECT id, name, category, catalog_price FROM products ORDER BY name"
        ).fetchall()

# =====================================================================
# BAGIAN 3 - VALIDASI INPUT DI PYTHON (penjaga pertama)
# =====================================================================
def validate_sale_inputs(price_text, quantity_text):
    """Kembalikan (harga, jumlah, pesan_error); pesan_error None jika valid."""
    price_text = price_text.strip()
    quantity_text = quantity_text.strip()

    if not price_text or not quantity_text:
        return None, None, "Harga dan jumlah wajib diisi."

    try:
        price = int(price_text)
        quantity = int(quantity_text)
    except ValueError:
        return None, None, "Harga dan jumlah harus bilangan bulat tanpa titik/koma."

    if price <= 0 or quantity <= 0:
        return None, None, "Harga dan jumlah harus lebih besar dari 0."
    return price, quantity, None

# =====================================================================
# BAGIAN 4 - MENYIMPAN TRANSAKSI (penjaga kedua: database)
# =====================================================================
def save_sale(sale_date, product_id, unit_price, quantity):
    """Simpan satu penjualan; database tetap memeriksa batasan nilainya."""
    total = unit_price * quantity
    with closing(get_connection()) as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO sales
                    (sale_date, product_id, unit_price, quantity, total)
                VALUES (?, ?, ?, ?, ?)
                """,
                (sale_date, product_id, unit_price, quantity, total),
            )
            connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Database menolak data yang melanggar aturan (CHECK/FOREIGN KEY).
            connection.rollback()  # batalkan penyimpanan
            raise  # teruskan error ke tampilan agar pesannya bisa ditampilkan

# =====================================================================
# BAGIAN 5 - TAMPILAN STREAMLIT
# =====================================================================
def main():
    st.set_page_config(page_title="Kedai Rasa — Minggu 5", layout="wide")
    st.title("Catatan Penjualan Kedai Rasa")
    st.caption(
        "Minggu 5: Validasi Data dan Relasi Tabel. "
        "Gunakan data simulasi, bukan transaksi nyata."
    )

    initialize_database()
    products = get_products()
    if not products:
        st.error("Katalog produk kosong. Minta bantuan dosen sebelum melanjutkan.")
        return

    product_by_id = {int(product["id"]): product for product in products}
    product_ids = list(product_by_id)

    st.subheader("Tambah transaksi")
    with st.form("sale_form"):
        sale_date = st.date_input("Tanggal transaksi")
        product_id = st.selectbox(
            "Pilih produk",
            options=product_ids,
            format_func=lambda item_id: (
                f"{product_by_id[item_id]['name']} — "
                f"{product_by_id[item_id]['category']}"
            ),
        )
        price_text = st.text_input(
            "Harga jual per unit (angka bulat rupiah, tanpa pemisah)",
            value="15000",
        )
        quantity_text = st.text_input("Jumlah unit (bilangan bulat)", value="1")
        submitted = st.form_submit_button("Simpan transaksi")

    if submitted:
        unit_price, quantity, error_message = validate_sale_inputs(
            price_text, quantity_text
        )
        if error_message:
            st.error(error_message)
        else:
            try:
                sale_id = save_sale(
                    sale_date.isoformat(), product_id, unit_price, quantity
                )
                st.success(
                    f"Transaksi nomor {sale_id} tersimpan. "
                    f"Total: Rp{unit_price * quantity:,}.".replace(",", ".")
                )
            except sqlite3.IntegrityError:
                st.error(
                    "Transaksi tidak tersimpan karena data tidak memenuhi "
                    "aturan database. Periksa kembali produk dan nilainya."
                )
    st.info(
        "Target minggu ini: transaksi valid tersimpan; input kosong, "
        "teks pada kolom angka, nol, dan nilai negatif ditolak."
    )


if __name__ == "__main__":
    main()