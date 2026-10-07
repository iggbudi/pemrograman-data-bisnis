from contextlib import closing
from datetime import date
from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).with_name("penjualan_m6.db")
SEED_PRODUCTS = [
    ("Kopi Susu", "Minuman", 15000),
    ("Teh Lemon", "Minuman", 12000),
    ("Es Cokelat", "Minuman", 18000),
    ("Roti Cokelat", "Makanan", 10000),
    ("Nasi Goreng", "Makanan", 22000),
    ("Pisang Goreng", "Camilan", 8000),
]
# (tanggal, nama produk, harga per unit saat transaksi, jumlah unit)
SEED_SALES = [
    ("2026-08-03", "Kopi Susu", 15000, 3),
    ("2026-08-03", "Roti Cokelat", 10000, 2),
    ("2026-08-05", "Nasi Goreng", 22000, 2),
    ("2026-08-07", "Teh Lemon", 12000, 4),
    ("2026-08-10", "Pisang Goreng", 8000, 5),
    ("2026-08-12", "Es Cokelat", 18000, 2),
    ("2026-08-14", "Kopi Susu", 15000, 5),
    ("2026-08-17", "Kopi Susu", 13000, 6),
    ("2026-08-17", "Pisang Goreng", 8000, 6),
    ("2026-08-19", "Nasi Goreng", 22000, 3),
    ("2026-08-21", "Roti Cokelat", 10000, 3),
    ("2026-08-24", "Teh Lemon", 12000, 2),
    ("2026-08-26", "Es Cokelat", 18000, 3),
    ("2026-08-28", "Kopi Susu", 15000, 4),
    ("2026-08-31", "Nasi Goreng", 22000, 1),
    ("2026-09-01", "Kopi Susu", 15000, 4),
    ("2026-09-02", "Pisang Goreng", 8000, 4),
    ("2026-09-04", "Nasi Goreng", 22000, 4),
    ("2026-09-07", "Teh Lemon", 12000, 5),
    ("2026-09-09", "Roti Cokelat", 10000, 4),
    ("2026-09-11", "Es Cokelat", 18000, 3),
    ("2026-09-14", "Kopi Susu", 15000, 6),
    ("2026-09-16", "Nasi Goreng", 22000, 2),
    ("2026-09-18", "Pisang Goreng", 8000, 3),
    ("2026-09-21", "Es Cokelat", 16000, 5),
    ("2026-09-23", "Teh Lemon", 12000, 3),
    ("2026-09-25", "Kopi Susu", 15000, 5),
    ("2026-09-28", "Roti Cokelat", 10000, 2),
    ("2026-09-30", "Nasi Goreng", 22000, 3),
    ("2026-09-30", "Kopi Susu", 15000, 2),
]
JOIN_SQL = "FROM sales JOIN products ON products.id = sales.product_id"


def get_connection():
    """Buka koneksi SQLite dan aktifkan pemeriksaan foreign key."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Buat tabel, isi katalog, dan isi transaksi simulasi jika masih kosong."""
    with closing(get_connection()) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                catalog_price INTEGER NOT NULL CHECK (catalog_price > 0)
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                unit_price INTEGER NOT NULL CHECK (unit_price > 0),
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                total INTEGER NOT NULL CHECK (total = unit_price * quantity),
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
        sales_count = connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if sales_count == 0:
            product_ids = dict(
                connection.execute("SELECT name, id FROM products").fetchall()
            )
            connection.executemany(
                """
                INSERT INTO sales
                    (sale_date, product_id, unit_price, quantity, total)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (sale_date, product_ids[name], price, quantity, price * quantity)
                    for sale_date, name, price, quantity in SEED_SALES
                ],
            )
        connection.commit()


def run_query(sql, params=()):
    """Jalankan query SELECT dan kembalikan hasilnya sebagai tabel DataFrame."""
    with closing(get_connection()) as connection:
        return pd.read_sql_query(sql, connection, params=list(params))


def get_categories():
    """Ambil daftar kategori untuk pilihan filter."""
    result = run_query("SELECT DISTINCT category FROM products ORDER BY category")
    return result["category"].tolist()


def get_date_bounds():
    """Ambil tanggal transaksi pertama dan terakhir sebagai periode bawaan."""
    result = run_query(
        "SELECT MIN(sale_date) AS first_date, MAX(sale_date) AS last_date FROM sales"
    )
    first_date, last_date = result.iloc[0]
    if first_date is None:
        return date.today(), date.today()
    return date.fromisoformat(first_date), date.fromisoformat(last_date)


def build_filter(start_date, end_date, categories):
    """Susun bagian WHERE dan nilai parameternya dari pilihan filter."""
    placeholders = ", ".join("?" for _ in categories)
    where_sql = (
        "WHERE sales.sale_date BETWEEN ? AND ? "
        f"AND products.category IN ({placeholders})"
    )
    params = [start_date.isoformat(), end_date.isoformat(), *categories]
    return where_sql, params


def get_summary(where_sql, params):
    """Hitung angka ringkasan untuk semua transaksi yang lolos filter."""
    result = run_query(
        f"""
        SELECT
            COUNT(*) AS jumlah_transaksi,
            COALESCE(SUM(sales.quantity), 0) AS unit_terjual,
            COALESCE(SUM(sales.total), 0) AS omzet,
            COALESCE(AVG(sales.total), 0) AS rata_rata,
            COALESCE(MAX(sales.total), 0) AS transaksi_terbesar
        {JOIN_SQL}
        {where_sql}
        """,
        params,
    )
    return result.iloc[0]


def get_report_by_product(where_sql, params, min_revenue):
    """Laporan per produk; HAVING menyaring produk dengan omzet kecil."""
    return run_query(
        f"""
        SELECT
            products.name AS produk,
            products.category AS kategori,
            COUNT(*) AS jumlah_transaksi,
            SUM(sales.quantity) AS unit_terjual,
            SUM(sales.total) AS omzet
        {JOIN_SQL}
        {where_sql}
        GROUP BY products.id, products.name, products.category
        HAVING SUM(sales.total) >= ?
        ORDER BY omzet DESC, produk
        """,
        [*params, min_revenue],
    )


def get_sales_detail(where_sql, params):
    """Data detail (baris per transaksi) untuk menelusuri angka laporan."""
    return run_query(
        f"""
        SELECT
            sales.id AS nomor,
            sales.sale_date AS tanggal,
            products.name AS produk,
            products.category AS kategori,
            sales.unit_price AS harga_satuan,
            sales.quantity AS jumlah,
            sales.total AS total
        {JOIN_SQL}
        {where_sql}
        ORDER BY sales.sale_date, sales.id
        """,
        params,
    )


def format_rupiah(value):
    """Ubah angka menjadi teks rupiah, misalnya 1500000 -> Rp1.500.000."""
    return f"Rp{round(value):,}".replace(",", ".")


COLUMN_CONFIG = {
    "nomor": st.column_config.NumberColumn("No."),
    "tanggal": st.column_config.TextColumn("Tanggal"),
    "produk": st.column_config.TextColumn("Produk"),
    "kategori": st.column_config.TextColumn("Kategori"),
    "jumlah_transaksi": st.column_config.NumberColumn("Jumlah transaksi"),
    "unit_terjual": st.column_config.NumberColumn("Unit terjual"),
    "jumlah": st.column_config.NumberColumn("Jumlah unit"),
    "harga_satuan": st.column_config.NumberColumn(
        "Harga satuan (Rp)", format="localized"
    ),
    "total": st.column_config.NumberColumn("Total (Rp)", format="localized"),
    "omzet": st.column_config.NumberColumn("Omzet (Rp)", format="localized"),
}


def main():
    st.set_page_config(page_title="Kedai Rasa — Minggu 6", layout="wide")
    st.title("Laporan Penjualan Kedai Rasa")
    st.caption("Latihan Minggu 6 tahap 6.1. Semua angka berasal dari data simulasi.")

    initialize_database()
    first_date, last_date = get_date_bounds()
    categories = get_categories()

    with st.sidebar:
        st.header("Filter laporan")
        period = st.date_input(
            "Periode",
            value=(first_date, last_date),
            format="DD/MM/YYYY",
        )
        selected_categories = st.multiselect(
            "Kategori", options=categories, default=categories
        )
        min_revenue = st.slider(
            "Omzet minimum per produk (Rp)",
            min_value=0,
            max_value=500000,
            value=0,
            step=25000,
        )

    if len(period) != 2:
        st.info("Pilih tanggal awal dan tanggal akhir periode di sidebar.")
        st.stop()
    if not selected_categories:
        st.warning("Pilih minimal satu kategori di sidebar.")
        st.stop()

    start_date, end_date = period
    where_sql, params = build_filter(start_date, end_date, selected_categories)
    summary = get_summary(where_sql, params)

    st.subheader(f"Ringkasan {start_date:%d/%m/%Y} – {end_date:%d/%m/%Y}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Omzet", format_rupiah(summary["omzet"]))
    col2.metric("Jumlah transaksi", int(summary["jumlah_transaksi"]))
    col3.metric("Rata-rata per transaksi", format_rupiah(summary["rata_rata"]))
    col4.metric("Transaksi terbesar", format_rupiah(summary["transaksi_terbesar"]))

    if summary["jumlah_transaksi"] == 0:
        st.info("Tidak ada transaksi pada periode dan kategori ini.")
        st.stop()

    st.subheader("Laporan per produk")
    st.caption(f"Produk dengan omzet minimal {format_rupiah(min_revenue)}.")
    by_product = get_report_by_product(where_sql, params, min_revenue)
    if by_product.empty:
        st.info("Tidak ada produk yang mencapai omzet minimum tersebut.")
    else:
        st.dataframe(
            by_product,
            column_config=COLUMN_CONFIG,
            hide_index=True,
            width="stretch",
        )

    st.subheader("Detail transaksi sesuai filter")
    st.dataframe(
        get_sales_detail(where_sql, params),
        column_config=COLUMN_CONFIG,
        hide_index=True,
        width="stretch",
    )

    st.info(
        "Checkpoint 6.1: ubah filter di sidebar, lalu pastikan kartu ringkasan, "
        "laporan per produk, dan detail transaksi berubah bersama."
    )

if __name__ == "__main__":
    main()
