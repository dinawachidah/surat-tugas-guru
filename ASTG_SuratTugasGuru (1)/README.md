# ASTG – Aplikasi Surat Tugas Guru
## SMA Islam Sultan Agung 2 Kalinyamatan

### Cara Menjalankan

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

3. Buka browser di `http://localhost:8501`

### Fitur
- ✏️ **Buat Surat Tugas** – form dengan validasi lengkap
- 📂 **Daftar Surat Tugas** – tampilan tabel, pencarian, filter
- 🖨️ **Cetak Surat** – tampilan preview surat tugas siap cetak
- 🗑️ **Hapus** – konfirmasi sebelum menghapus data

### Struktur File
```
astg_app/
├── app.py           ← aplikasi utama
├── requirements.txt
├── README.md
└── astg.db          ← database SQLite (dibuat otomatis)
```

### Catatan
- Database menggunakan SQLite lokal (`astg.db`), dibuat otomatis saat pertama dijalankan.
- Untuk cetak surat, klik tombol 🖨️ lalu gunakan Ctrl+P / Cmd+P di browser.
