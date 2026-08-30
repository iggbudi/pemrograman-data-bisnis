"""Mengisi toko.db dengan data transaksi contoh selama 1 bulan (Agustus 2026).
Jalankan sekali:  python seed_data.py
Catatan: isi tabel penjualan yang lama akan dikosongkan dulu.
"""
import sqlite3
import random
from datetime import date, timedelta

random.seed(42)  # biar hasil random selalu sama setiap dijalankan

PRODUK = {
    "Buku Tulis": 5000,
    "Pulpen": 3000,
    "Tas": 25000,
    "Kertas HVS": 45000,
}
PELANGGAN = [
    "Andi Wijaya", "Siti Rahma", "Budi Santoso", "Dewi Lestari", "Eko Prasetyo",
    "Fitri Handayani", "Gilang Ramadhan", "Hani Puspita", "Indra Kusuma",
    "Joko Susilo", "Kartika Sari", "Lukman Hakim", "Maya Anggraini",
    "Nur Aini", "Oscar Pratama", "Putri Melati", "Rizki Amalia",
    "Sari Wulandari", "Teguh Saputra", "Utami Dewi", "Vina Oktaviani",
    "Wawan Setiawan", "Yuni Astuti", "Zahra Amelia", "Toko Berkah Jaya",
    "Koperasi Sekolah", "CV Maju Bersama", "Warung Bu Yanti",
]

koneksi = sqlite3.connect("toko.db")
koneksi.execute("DELETE FROM penjualan")  # kosongkan data lama

tgl_mulai = date(2026, 8, 1)
tgl_akhir = date(2026, 8, 30)
jumlah_hari = (tgl_akhir - tgl_mulai).days + 1

total_transaksi = 0
for i in range(jumlah_hari):
    tanggal = tgl_mulai + timedelta(days=i)
    # jumlah transaksi per hari bervariasi 1-3
    for _ in range(random.randint(1, 3)):
        produk = random.choice(list(PRODUK))
        koneksi.execute(
            "INSERT INTO penjualan (tanggal, pelanggan, produk, jumlah, harga) VALUES (?, ?, ?, ?, ?)",
            (
                tanggal.isoformat(),
                random.choice(PELANGGAN),
                produk,
                random.randint(1, 10),
                PRODUK[produk],
            ),
        )
        total_transaksi += 1

koneksi.commit()

df = __import__("pandas").read_sql(
    "SELECT COUNT(*) AS n, SUM(jumlah * harga) AS omzet FROM penjualan", koneksi
)
print(df.to_string(index=False))
koneksi.close()
