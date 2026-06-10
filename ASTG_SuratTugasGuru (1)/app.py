import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import date, datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ASTG – SMA Islam Sultan Agung 2",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── School data ───────────────────────────────────────────────────────────────
SCHOOL = {
    "name":      "SMA ISLAM SULTAN AGUNG 2 KALINYAMATAN",
    "yayasan":   "YAYASAN BADAN WAKAF SULTAN AGUNG",
    "unit":      "SEKOLAH MENENGAH ATAS ISLAM",
    "brand":     "Sultan Agung 2 Kalinyamatan",
    "address":   "Jl. Gotri - Welahan, Kriyan, Kalinyamatan, Jepara, Indonesia 59462",
    "phone":     "0858-7541-9288",
    "email":     "humas.smasula2@gmail.com",
    "principal": "Ali Akhmad Setiyawan, M.Pd.",
}

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "astg.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS surat_tugas (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                nomor_surat     TEXT NOT NULL UNIQUE,
                nama_guru       TEXT NOT NULL,
                nip_nuptk       TEXT NOT NULL,
                mapel           TEXT NOT NULL,
                nama_kegiatan   TEXT NOT NULL,
                tempat_kegiatan TEXT NOT NULL,
                tanggal_mulai   TEXT NOT NULL,
                tanggal_selesai TEXT NOT NULL,
                keterangan      TEXT,
                created_at      TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        conn.commit()

init_db()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Palette ─────────────────────── */
:root {
    --navy:    #0f2d56;
    --blue:    #1e5fa8;
    --sky:     #3b82f6;
    --light:   #dbeafe;
    --gold:    #c9a227;
    --white:   #ffffff;
    --gray-50: #f8fafc;
    --gray-100:#f1f5f9;
    --gray-300:#cbd5e1;
    --gray-600:#475569;
    --gray-800:#1e293b;
}

/* ── Global ─────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--gray-50) !important;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* ── Sidebar ─────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, #163d70 100%) !important;
    border-right: 3px solid var(--gold);
}
[data-testid="stSidebar"] * { color: var(--white) !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Page header ─────────────────── */
.page-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
    color: var(--white);
    padding: 28px 36px;
    border-radius: 14px;
    margin-bottom: 28px;
    border-bottom: 4px solid var(--gold);
    box-shadow: 0 4px 20px rgba(15,45,86,.25);
}
.page-header h1 { margin: 0 0 4px; font-size: 1.7rem; font-weight: 700; }
.page-header p  { margin: 0; opacity: .85; font-size: .9rem; }

/* ── Cards ───────────────────────── */
.card {
    background: var(--white);
    border-radius: 12px;
    padding: 28px 32px;
    box-shadow: 0 2px 12px rgba(0,0,0,.07);
    border: 1px solid var(--gray-100);
    margin-bottom: 24px;
}
.card-title {
    font-size: 1.1rem; font-weight: 700;
    color: var(--navy);
    border-left: 4px solid var(--sky);
    padding-left: 10px; margin-bottom: 18px;
}

/* ── Metric tiles ────────────────── */
.metric-row { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
.metric-tile {
    flex: 1; min-width: 130px;
    background: var(--white);
    border-radius: 12px;
    padding: 18px 22px; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
    border-top: 4px solid var(--sky);
}
.metric-tile .val { font-size: 2rem; font-weight: 800; color: var(--navy); }
.metric-tile .lbl { font-size: .78rem; color: var(--gray-600); margin-top: 2px; }

/* ── Buttons ─────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, var(--blue), var(--sky)) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    transition: opacity .2s, transform .1s !important;
    box-shadow: 0 2px 8px rgba(30,95,168,.3) !important;
}
div.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }

/* ── Inputs ──────────────────────── */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 8px !important;
    border-color: var(--gray-300) !important;
}

/* ═══════════════════════════════════
   SURAT TUGAS — format resmi
═══════════════════════════════════ */
.surat-wrap {
    background: #fff;
    border: 1px solid #999;
    max-width: 750px;
    margin: 0 auto;
    font-family: 'Times New Roman', Times, serif;
    color: #000;
    box-shadow: 0 4px 28px rgba(0,0,0,.18);
}
/* KOP */
.kop-surat {
    display: flex;
    align-items: center;
    padding: 16px 36px 10px;
    gap: 14px;
}
.kop-logo-box {
    width: 84px; height: 84px;
    border: 2.5px solid #1a3a5c;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    color: #1a3a5c; font-weight: 900;
    font-size: .62rem; text-align: center; line-height: 1.3;
    font-family: 'Times New Roman', Times, serif;
}
.kop-tengah { flex: 1; text-align: center; }
.kop-yayasan {
    font-size: .83rem; font-weight: 400;
    font-family: 'Times New Roman', Times, serif;
    color: #000; line-height: 1.4; margin: 0;
}
.kop-unit {
    font-size: .98rem; font-weight: 700;
    text-transform: uppercase;
    font-family: 'Times New Roman', Times, serif;
    color: #000; margin: 0;
}
.kop-nama-sekolah {
    font-size: 1.55rem; font-weight: 900;
    text-transform: uppercase;
    font-family: 'Times New Roman', Times, serif;
    color: #000; line-height: 1.1; margin: 2px 0 4px;
}
.kop-alamat {
    font-size: .8rem; color: #000;
    font-family: 'Times New Roman', Times, serif; line-height: 1.5;
}
.kop-garis-tebal  { height: 4px;   background: #000; margin: 0; }
.kop-garis-tipis  { height: 1.5px; background: #000; margin-top: 2px; }

/* BADAN */
.badan-surat {
    padding: 18px 48px 42px;
    font-family: 'Times New Roman', Times, serif;
    font-size: .97rem; color: #000;
}
.judul-surat {
    text-align: center; margin: 10px 0 2px;
}
.judul-surat span {
    font-size: 1.1rem; font-weight: 900;
    text-decoration: underline;
    text-transform: uppercase;
    letter-spacing: 8px;
    font-family: 'Times New Roman', Times, serif;
}
.nomor-surat {
    text-align: center; font-size: .95rem;
    margin: 4px 0 18px; color: #000;
    font-family: 'Times New Roman', Times, serif;
}
.paragraf {
    font-size: .97rem; text-align: justify;
    line-height: 1.8; color: #000; margin: 0 0 8px;
    font-family: 'Times New Roman', Times, serif;
}
.tabel-surat {
    width: 100%; border-collapse: collapse;
    font-size: .97rem; margin: 4px 0 10px 28px;
    font-family: 'Times New Roman', Times, serif;
}
.tabel-surat td { padding: 2px 4px; vertical-align: top; color: #000; }
.tabel-surat td.col-label { width: 32%; }
.tabel-surat td.col-titik { width: 4%;  }
.blok-ttd {
    display: flex; justify-content: flex-end;
    margin-top: 28px;
}
.ttd-isi { text-align: center; min-width: 240px; }
.ttd-kota-tgl { font-size: .97rem; font-family: 'Times New Roman', Times, serif; }
.ttd-jabatan  { font-size: .97rem; font-family: 'Times New Roman', Times, serif; margin-bottom: 0; }
.ttd-ruang    { height: 76px; }
.ttd-nama {
    font-size: .97rem; font-weight: 700;
    text-decoration: underline;
    font-family: 'Times New Roman', Times, serif;
}
.ttd-nip { font-size: .9rem; font-family: 'Times New Roman', Times, serif; }

/* Print */
@media print {
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stButton, .no-print { display: none !important; }
    .surat-wrap { box-shadow: none !important; border: 1px solid #999 !important; max-width: 100% !important; }
    .badan-surat { padding: 14px 40px 36px !important; }
    body { background: white !important; }
}

/* ── Responsive ──────────────────── */
@media (max-width: 640px) {
    .metric-row { flex-direction: column; }
    .kop-surat { flex-direction: column; text-align: center; }
    .badan-surat { padding: 14px 20px 28px; }
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
MONTHS_ID = {
    "January":"Januari","February":"Februari","March":"Maret",
    "April":"April","May":"Mei","June":"Juni",
    "July":"Juli","August":"Agustus","September":"September",
    "October":"Oktober","November":"November","December":"Desember",
}

def fmt_date_id(d: str) -> str:
    try:
        raw = datetime.strptime(d, "%Y-%m-%d").strftime("%d %B %Y")
    except Exception:
        return d
    for en, idn in MONTHS_ID.items():
        raw = raw.replace(en, idn)
    return raw

def today_id() -> str:
    t = date.today().strftime("%d %B %Y")
    for en, idn in MONTHS_ID.items():
        t = t.replace(en, idn)
    return t

# ── DB helpers ────────────────────────────────────────────────────────────────
def get_all():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM surat_tugas ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]

def get_by_id(rid: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM surat_tugas WHERE id=?", (rid,)
        ).fetchone()
    return dict(row) if row else None

def insert(data: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO surat_tugas
            (nomor_surat,nama_guru,nip_nuptk,mapel,nama_kegiatan,
             tempat_kegiatan,tanggal_mulai,tanggal_selesai,keterangan)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            data["nomor_surat"], data["nama_guru"], data["nip_nuptk"],
            data["mapel"], data["nama_kegiatan"], data["tempat_kegiatan"],
            data["tanggal_mulai"], data["tanggal_selesai"],
            data.get("keterangan",""),
        ))
        conn.commit()

def delete_by_id(rid: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM surat_tugas WHERE id=?", (rid,))
        conn.commit()

def nomor_exists(nomor: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM surat_tugas WHERE nomor_surat=?", (nomor,)
        ).fetchone()
    return row is not None

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 24px'>
        <div style='width:64px;height:64px;background:#c9a227;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    margin:0 auto 10px;font-size:1.6rem;'>&#128203;</div>
        <div style='font-weight:800;font-size:1rem;letter-spacing:.5px;'>ASTG</div>
        <div style='font-size:.72rem;opacity:.7;margin-top:2px;'>
            SMA Islam Sultan Agung 2
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["🏠  Beranda", "✏️  Buat Surat Tugas", "📂  Daftar Surat Tugas"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-size:.72rem;opacity:.65;line-height:1.8;'>
        <b>SMA Islam Sultan Agung 2</b><br>
        Kalinyamatan, Jepara<br><br>
        &#128222; 0858-7541-9288<br>
        &#9993; humas.smasula2@gmail.com
    </div>
    """, unsafe_allow_html=True)

page = menu.split("  ", 1)[1]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Beranda
# ══════════════════════════════════════════════════════════════════════════════
if page == "Beranda":
    st.markdown("""
    <div class="page-header">
        <h1>&#127978; Selamat Datang di ASTG</h1>
        <p>Aplikasi Surat Tugas Guru &mdash; SMA Islam Sultan Agung 2 Kalinyamatan</p>
    </div>
    """, unsafe_allow_html=True)

    records = get_all()
    total    = len(records)
    bulan_ini = sum(1 for r in records if r["tanggal_mulai"][:7] == date.today().strftime("%Y-%m"))
    terbaru   = records[0]["created_at"][:10] if records else "-"

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-tile">
            <div class="val">{total}</div>
            <div class="lbl">Total Surat Tugas</div>
        </div>
        <div class="metric-tile">
            <div class="val">{bulan_ini}</div>
            <div class="lbl">Bulan Ini</div>
        </div>
        <div class="metric-tile">
            <div class="val">{terbaru}</div>
            <div class="lbl">Surat Terbaru</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Tentang Aplikasi</div>
        <p style="color:#475569;line-height:1.8;margin:0">
            ASTG membantu administrasi penerbitan <strong>Surat Tugas Guru</strong> secara
            digital. Anda dapat membuat, melihat, mencetak, dan menghapus surat tugas
            dengan mudah.<br><br>
            Gunakan menu di sebelah kiri:
            <ul style="margin-top:8px">
                <li><strong>Buat Surat Tugas</strong> &ndash; isi formulir dan simpan</li>
                <li><strong>Daftar Surat Tugas</strong> &ndash; lihat semua data, cetak, atau hapus</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if records:
        st.markdown('<div class="card"><div class="card-title">5 Surat Tugas Terbaru</div>', unsafe_allow_html=True)
        df = pd.DataFrame(records[:5])[["nomor_surat","nama_guru","mapel","nama_kegiatan","tanggal_mulai"]]
        df.columns = ["Nomor Surat","Nama Guru","Mapel","Nama Kegiatan","Tanggal"]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Buat Surat Tugas
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Buat Surat Tugas":
    st.markdown("""
    <div class="page-header">
        <h1>&#9999;&#65039; Buat Surat Tugas</h1>
        <p>Isi formulir di bawah untuk menerbitkan surat tugas guru baru.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_surat", clear_on_submit=True):
        st.markdown('<div class="card"><div class="card-title">Data Surat</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            nomor_surat = st.text_input("Nomor Surat *", placeholder="Contoh: 001/SULAS2/VI/2025", help="Nomor surat harus unik")
        with col2:
            mapel = st.text_input("Mata Pelajaran *", placeholder="Contoh: Matematika")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Data Guru</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            nama_guru = st.text_input("Nama Guru *", placeholder="Nama lengkap guru")
        with col4:
            nip_nuptk = st.text_input("NIP / NUPTK *", placeholder="Nomor induk pegawai/tendik")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Data Kegiatan</div>', unsafe_allow_html=True)
        nama_kegiatan   = st.text_input("Nama Kegiatan *", placeholder="Contoh: Seminar Nasional Pendidikan 2025")
        col5, col6 = st.columns(2)
        with col5:
            tempat_kegiatan = st.text_input("Tempat Kegiatan *", placeholder="Contoh: Hotel Graha Santika, Semarang")
        with col6:
            pass
        col7, col8 = st.columns(2)
        with col7:
            tanggal_mulai   = st.date_input("Tanggal Mulai *",   value=date.today(), min_value=date(2020,1,1))
        with col8:
            tanggal_selesai = st.date_input("Tanggal Selesai *", value=date.today(), min_value=date(2020,1,1))
        keterangan = st.text_area("Keterangan Tambahan", placeholder="(Opsional) Catatan tambahan...", height=80)
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("&#128190;  Simpan Surat Tugas", use_container_width=True)

    if submitted:
        errors = []
        if not nomor_surat.strip():
            errors.append("Nomor Surat wajib diisi.")
        elif nomor_exists(nomor_surat.strip()):
            errors.append(f"Nomor Surat **{nomor_surat}** sudah digunakan.")
        if not nama_guru.strip():
            errors.append("Nama Guru wajib diisi.")
        if not nip_nuptk.strip():
            errors.append("NIP/NUPTK wajib diisi.")
        if not mapel.strip():
            errors.append("Mata Pelajaran wajib diisi.")
        if not nama_kegiatan.strip():
            errors.append("Nama Kegiatan wajib diisi.")
        if not tempat_kegiatan.strip():
            errors.append("Tempat Kegiatan wajib diisi.")
        if tanggal_selesai < tanggal_mulai:
            errors.append("Tanggal Selesai tidak boleh sebelum Tanggal Mulai.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            insert({
                "nomor_surat":     nomor_surat.strip(),
                "nama_guru":       nama_guru.strip(),
                "nip_nuptk":       nip_nuptk.strip(),
                "mapel":           mapel.strip(),
                "nama_kegiatan":   nama_kegiatan.strip(),
                "tempat_kegiatan": tempat_kegiatan.strip(),
                "tanggal_mulai":   str(tanggal_mulai),
                "tanggal_selesai": str(tanggal_selesai),
                "keterangan":      keterangan.strip(),
            })
            st.success(f"Surat Tugas **{nomor_surat}** berhasil disimpan!")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Daftar Surat Tugas
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Daftar Surat Tugas":
    st.markdown("""
    <div class="page-header">
        <h1>&#128194; Daftar Surat Tugas</h1>
        <p>Kelola semua surat tugas yang telah diterbitkan.</p>
    </div>
    """, unsafe_allow_html=True)

    records = get_all()

    # ── Preview / cetak surat ─────────────────────────────────────────────────
    if st.session_state.get("print_id"):
        rid = st.session_state.print_id
        r   = get_by_id(rid)
        if r:
            # tanggal range
            if r["tanggal_mulai"] == r["tanggal_selesai"]:
                tgl_range = fmt_date_id(r["tanggal_mulai"])
            else:
                tgl_range = fmt_date_id(r["tanggal_mulai"]) + " s.d. " + fmt_date_id(r["tanggal_selesai"])

            ket_row = ""
            if r.get("keterangan"):
                ket_row = "<tr><td class='col-label'>Keterangan</td><td class='col-titik'>:</td><td>" + r["keterangan"] + "</td></tr>"

            html_surat = (
                "<div class='surat-wrap'>"
                # KOP
                "<div class='kop-surat'>"
                "<div class='kop-logo-box'>LOGO<br>SEKOLAH</div>"
                "<div class='kop-tengah'>" 
                "<p class='kop-unit'>" + SCHOOL["unit"] + "</p>"
                "<p class='kop-nama-sekolah'>" + SCHOOL["brand"] + "</p>"
                "<p class='kop-alamat'>" + SCHOOL["address"] + "<br>"
                "Telp. " + SCHOOL["phone"] + " &nbsp;&bull;&nbsp; Email: " + SCHOOL["email"] + "</p>"
                "</div>"
                "</div>"
                "<div class='kop-garis-tebal'></div>"
                "<div class='kop-garis-tipis'></div>"
                # BADAN
                "<div class='badan-surat'>"
                "<div class='judul-surat'><span>S U R A T &nbsp; T U G A S</span></div>"
                "<div class='nomor-surat'>Nomor : " + r["nomor_surat"] + "</div>"
                "<p class='paragraf'>Kepala " + SCHOOL["name"] + " memberi tugas kepada:</p>"
                "<table class='tabel-surat'>"
                "<tr><td class='col-label'>Nama</td><td class='col-titik'>:</td><td>" + r["nama_guru"] + "</td></tr>"
                "<tr><td class='col-label'>NIP / NUPTK</td><td class='col-titik'>:</td><td>" + r["nip_nuptk"] + "</td></tr>"
                "<tr><td class='col-label'>Mata Pelajaran</td><td class='col-titik'>:</td><td>" + r["mapel"] + "</td></tr>"
                "<tr><td class='col-label'>Jabatan</td><td class='col-titik'>:</td><td>Guru</td></tr>"
                "</table>"
                "<p class='paragraf'>Untuk mengikuti / melaksanakan kegiatan <strong>" + r["nama_kegiatan"] + "</strong> yang dilaksanakan pada:</p>"
                "<table class='tabel-surat'>"
                "<tr><td class='col-label'>Hari / Tanggal</td><td class='col-titik'>:</td><td>" + tgl_range + "</td></tr>"
                "<tr><td class='col-label'>Tempat</td><td class='col-titik'>:</td><td>" + r["tempat_kegiatan"] + "</td></tr>"
                + ket_row +
                "</table>"
                "<p class='paragraf' style='margin-top:14px;'>Demikian surat tugas ini agar dilaksanakan dengan penuh tanggung jawab.</p>"
                "<div class='blok-ttd'><div class='ttd-isi'>"
                "<div class='ttd-kota-tgl'>Jepara, " + today_id() + "</div>"
                "<div class='ttd-jabatan'>Kepala Sekolah,</div>"
                "<div class='ttd-ruang'></div>"
                "<div class='ttd-nama'>" + SCHOOL["principal"] + "</div>"
                "<div class='ttd-nip'>NIP. &nbsp;&ndash;</div>"
                "</div></div>"
                "</div>"  # badan-surat
                "</div>"  # surat-wrap
            )

            st.markdown(html_surat, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            col_back, col_print = st.columns([1, 1])
            with col_back:
                if st.button("← Kembali ke Daftar", use_container_width=True):
                    st.session_state.print_id = None
                    st.rerun()
            with col_print:
                st.markdown(
                    "<div class='no-print'>"
                    "<button onclick='window.print()' "
                    "style='width:100%;padding:10px;background:linear-gradient(135deg,#1e5fa8,#3b82f6);"
                    "color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;"
                    "font-size:.95rem;box-shadow:0 2px 8px rgba(30,95,168,.3)'>"
                    "&#128424;&#65039; Cetak Surat"
                    "</button></div>",
                    unsafe_allow_html=True,
                )
            st.stop()

    # ── Konfirmasi hapus ──────────────────────────────────────────────────────
    if st.session_state.get("delete_id"):
        rid = st.session_state.delete_id
        r   = get_by_id(rid)
        if r:
            st.warning(
                f"Apakah Anda yakin ingin menghapus surat tugas "
                f"**{r['nomor_surat']}** atas nama **{r['nama_guru']}**?"
            )
            c1, c2, _ = st.columns([1, 1, 4])
            with c1:
                if st.button("🗑️ Ya, Hapus", type="primary", use_container_width=True):
                    delete_by_id(rid)
                    st.session_state.delete_id = None
                    st.success("Data berhasil dihapus.")
                    st.rerun()
            with c2:
                if st.button("Batal", use_container_width=True):
                    st.session_state.delete_id = None
                    st.rerun()
        st.markdown("---")

    # ── Pencarian ─────────────────────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">Filter &amp; Pencarian</div>', unsafe_allow_html=True)
    col_s, col_m = st.columns([3, 1])
    with col_s:
        search = st.text_input("Cari", placeholder="Cari nama guru, nomor surat, atau kegiatan...", label_visibility="collapsed")
    with col_m:
        sort_opt = st.selectbox("Urut", ["Terbaru","Terlama"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    if search:
        q = search.lower()
        records = [r for r in records if q in r["nama_guru"].lower() or q in r["nomor_surat"].lower() or q in r["nama_kegiatan"].lower()]
    if sort_opt == "Terlama":
        records = list(reversed(records))

    # ── Tabel data ────────────────────────────────────────────────────────────
    if not records:
        st.info("Belum ada surat tugas." if not search else "Tidak ada hasil yang cocok.")
    else:
        st.markdown(f"**{len(records)}** surat tugas ditemukan.")
        hdr = st.columns([1.3, 1.8, 1.3, 1.4, 2.0, 1.4, 0.65, 0.65])
        for h, l in zip(hdr, ["Nomor Surat","Nama Guru","NIP/NUPTK","Mapel","Nama Kegiatan","Tanggal","Cetak","Hapus"]):
            h.markdown(f"<small><b>{l}</b></small>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 6px;border-color:#e2e8f0'>", unsafe_allow_html=True)

        for r in records:
            cols = st.columns([1.3, 1.8, 1.3, 1.4, 2.0, 1.4, 0.65, 0.65])
            cols[0].markdown(f"<small>{r['nomor_surat']}</small>",     unsafe_allow_html=True)
            cols[1].markdown(f"<small>{r['nama_guru']}</small>",       unsafe_allow_html=True)
            cols[2].markdown(f"<small>{r['nip_nuptk']}</small>",       unsafe_allow_html=True)
            cols[3].markdown(f"<small>{r['mapel']}</small>",           unsafe_allow_html=True)
            cols[4].markdown(f"<small>{r['nama_kegiatan']}</small>",   unsafe_allow_html=True)
            cols[5].markdown(f"<small>{r['tanggal_mulai']}</small>",   unsafe_allow_html=True)
            if cols[6].button("🖨️", key=f"p_{r['id']}", help="Cetak"):
                st.session_state.print_id = r["id"]
                st.rerun()
            if cols[7].button("🗑️", key=f"d_{r['id']}", help="Hapus"):
                st.session_state.delete_id = r["id"]
                st.rerun()
            st.markdown("<hr style='margin:2px 0;border-color:#f1f5f9'>", unsafe_allow_html=True)
