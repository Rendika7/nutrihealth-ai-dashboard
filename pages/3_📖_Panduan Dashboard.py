# app.py — NutriHealth AI • Coming Soon (fix img, centered, auto height)
import streamlit as st
import streamlit.components.v1 as components
import os, base64
import os
import pathlib
from datetime import datetime
import base64
from textwrap import dedent

import streamlit as st
from PIL import Image

web_icon = Image.open('icon\\Only LOGO.png')  # konsisten dengan file lain
st.set_page_config(
    page_title="Panduan NutriHealth AI",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=web_icon
)

# ------------------------------- | ------------------------------- | -------------------------------
# 3_📖_Panduan Dashboard.py — NutriHealth AI: User Guide
# ------------------------------- | ------------------------------- | -------------------------------
# Util: style kecil & helper
# ------------------------------- | ------------------------------- | -------------------------------
def _safe_page_link(path: str, label: str, icon: str = ""):
    """Render st.page_link jika file ada; kalau tidak, tampilkan placeholder."""
    p = pathlib.Path(path)
    if p.is_file():
        st.page_link(path, label=label, icon=icon)
    else:
        st.write(f"_{label} (coming soon)_")

@st.cache_data
def _b64(path: str) -> str:
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

# CSS halus buat konsistensi & simetri
st.markdown(dedent("""
<style>
/* center section headings in green chips */
.chip-title{
  text-align:center; font-size:22px; font-weight:700;
  padding:10px 14px; background:#88CD33; color:white;
  border-radius:8px; margin:12px 0 14px 0;
}
/* grid-like paragraphs */
p { line-height:1.55; }
/* badges */
.badge{display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; margin-right:6px;}
.badge-green{background:#E8F5E9; color:#2E7D32; border:1px solid #C8E6C9;}
.badge-blue{background:#E3F2FD; color:#1565C0; border:1px solid #BBDEFB;}
.badge-amber{background:#FFF8E1; color:#B26A00; border:1px solid #FFE0B2;}
.badge-red{background:#FFEBEE; color:#C62828; border:1px solid #FFCDD2;}
/* cards equal height */
.equal-card{background:white; border:1px solid #EEE; border-radius:10px; padding:16px; height:100%;}
/* table-like keypoints */
.kp{display:flex; gap:10px; align-items:flex-start;}
.kp .bullet{width:8px; height:8px; margin-top:8px; border-radius:2px; background:#0F172A;}
/* center tab-list (if any used here later) */
div[data-baseweb="tab-list"]{display:flex; justify-content:center;}
/* small hr spacing */
hr{margin:10px 0;}
</style>
"""), unsafe_allow_html=True)

# ------------------------------- | ------------------------------- | -------------------------------
# Header
# ------------------------------- | ------------------------------- | -------------------------------
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown("<h2 style='text-align:center; margin:6px 0 2px 0;'>📖 Panduan Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.85;'>NutriHealth AI — Generasi Emas 2045</p>", unsafe_allow_html=True)

st.divider()

# ------------------------------- | ------------------------------- | -------------------------------
# TOC (Sidebar)
# ------------------------------- | ------------------------------- | -------------------------------
with st.sidebar:
    st.header("📚 Navigasi Panduan")
    st.markdown("- ▶️ **Ringkas & Tujuan**")
    st.markdown("- 🔮 **Forecasting & Kontrol**")
    st.markdown("- 🏷️ **Definisi Indikator**")
    st.markdown("- 🗂️ **Sumber Data & Versi**")
    st.markdown("- 🛠️ **Troubleshooting & FAQ**")
    st.markdown("- 🔗 **Navigasi Halaman**")

# ------------------------------- | ------------------------------- | -------------------------------
# 1) Ringkas & Tujuan
# ------------------------------- | ------------------------------- | -------------------------------

st.markdown('<div class="chip-title">▶️ Ringkas & Tujuan</div>', unsafe_allow_html=True)

with st.expander("Apa ini?", expanded=True):
    st.write(
        "Dashboard analitik untuk **Kesehatan Ibu–Anak (MNCH)** dan **Kapasitas RS** di Jawa Timur, "
        "menggabungkan **EDA** dan **statistical forecasting** untuk memantau tren dan proyeksi 18 bulan ke depan."
    )

with st.expander("Untuk siapa?", expanded=False):
    st.write(
        "Pengambil kebijakan, analis kesehatan, dan tenaga program (gizi, maternal-neonatal) yang butuh insight ringkas "
        "namun dapat ditelusuri (traceable) ke metrik dan grafik sumber."
    )

with st.expander("Apa outputnya?", expanded=False):
    st.markdown(
        "- Ringkasan **kapasitas & mutu layanan** (BOR/TOI/AVLOS/GDR/NDR)\n"
        "- Outcome **MNCH** (ASI/AKI/AKB/BBLR)\n"
        "- **Forecast** dengan 95% CI dan model terbaik (S-Naïve/ETS/SARIMAX)\n"
        "- **Cluster peta** kab/kota untuk prioritisasi"
    )

# ------------------------------- | ------------------------------- | -------------------------------
# 4) Forecasting & Kontrol
# ------------------------------- | ------------------------------- | -------------------------------
st.markdown('<div class="chip-title">🔮 Forecasting & Kontrol</div>', unsafe_allow_html=True)

colL, colR = st.columns(2)
with colL:
    st.markdown("**Model yang digunakan**")
    st.write(
        "- **S-Naïve**: musiman sederhana (baseline kuat untuk data musiman)\n"
        "- **ETS**: Error–Trend–Seasonal (eksponensial smoothing; adaptif pada pola level/tren/musim)\n"
        "- **SARIMAX**: ARIMA musiman + exogenous (jika ada feature luar; di sini difungsikan sebagai kandidat kuat pola musiman)"
    )
    st.markdown("**Pemilihan model terbaik**")
    st.write(
        "Otomatis memilih model dengan performa validasi terbaik (mis. **MASE**/**sMAPE**) per target. "
        "Plot menampilkan **actual vs forecast** dan **95% CI**."
    )

with colR:
    st.markdown("**Kontrol UI (di tab Forecasting Result)**")
    st.write(
        "- **Pilih indikator**: ganti target (BOR, AVLOS, GDR/NDR, TOI, AKI, AKB, BBLR)\n"
        "- **Window (bulan terakhir)**: fokus periode 12/24/36/48 bulan atau **Semua**\n"
        "- **Toggle 95% CI**: tampil/sembunyikan ketidakpastian\n"
        "- **Ringkasan kartu**: *Last Actual*, *First/Last Forecast*, dan *Model Terbaik*"
    )
    st.markdown('<span class="badge badge-green">Interpretasi</span> Hindari keputusan dari 1 titik; baca **tren** + **CI** + **konteks program**.', unsafe_allow_html=True)

st.markdown("---")

st.markdown("**Aturan praktis interpretasi CI**")
st.write(
    "- Jika **band CI sempit** → model relatif yakin; **lebar** → ketidakpastian tinggi (perlu data tambahan/penyebab variabilitas).\n"
    "- Perhatikan **pergeseran regime** (kebijakan/kejadian luar biasa) yang dapat membuat proyeksi kurang akurat."
)

# ------------------------------- | ------------------------------- | -------------------------------
# 5) Definisi Indikator (Glossary)
# ------------------------------- | ------------------------------- | -------------------------------
st.markdown('<div class="chip-title">🏷️ Definisi Indikator</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2)
with g1:
    st.subheader("Kapasitas & Mutu RS")
    st.write("- **BOR (%)** — Bed Occupancy Rate: persentase keterisian tempat tidur (target operasional **60–80%** optimal; >85% **saturated**).")
    st.write("- **TOI (Day)** — Turnover Interval: jeda antar pasien; **<1 hari** sangat cepat (indikasi penuh), 1–3 **sehat**.")
    st.write("- **AVLOS (Day)** — Rata-rata lama dirawat; lebih tinggi bisa sinyal **kasus berat**/bottleneck discharge.")
    st.write("- **GDR (/K)** — Gross Death Rate; **NDR (/K)** — Net Death Rate; bedakan kematian <48 jam (**EDR ~ GDR–NDR**).")
    st.write("- **HI = AVLOS + TOI** (siklus 1 tempat tidur); **BTO = days_in_month / HI** (perputaran bed/bln).")
    st.write("- **IdleShare = 1 − BOR/100** (porsi bed menganggur).")
    st.markdown('<span class="badge badge-red">Capacity alert</span> aktif jika **BOR > 80% & TOI < 1 hari** (operasional).', unsafe_allow_html=True)

with g2:
    st.subheader("Outcome MNCH")
    st.write("- **ASI (proporsi)** — target operasional **≥ 80%**.")
    st.write("- **BBLR** — Bayi Berat Lahir Rendah (proporsi/rasio).")
    st.write("- **AKI/AKB** — Angka Kematian Ibu/Bayi (rasio).")
    st.write("- **ASI_gap_target = ASI − 0.80** → positif berarti on-track.")
    st.markdown('<span class="badge badge-amber">Catatan</span> Lakukan *triangulation* dengan program (imunisasi, rujukan, gizi).', unsafe_allow_html=True)

# ------------------------------- | ------------------------------- | -------------------------------
# 6) Sumber Data & Versi
# ------------------------------- | ------------------------------- | -------------------------------
st.markdown('<div class="chip-title">🗂️ Sumber Data & Versi</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns([1.2, 1, 1.2])
with d1:
    st.markdown("**Sumber**")
    st.write("- Open Data Jawa Timur — **opendata.jatimprov.go.id**")
    st.write("- Data spatial kab/kota — **GeoJSON Jatim**")
with d2:
    st.markdown("**Data Product**")
    st.write("- `data/ABT_Master.csv` (analytical base table)")
    st.write("- `data/forecast_results.csv` (hasil model per target)")
    st.write("- `data/df_merged_after_forecast.csv` (merge actual+forecast)")
with d3:
    st.markdown("**Dokumen Rujukan**")
    st.write("- Data Dictionary (tautan di footer Home)")
    st.write("- Catatan pemrosesan (pre-processing & feature opsional)")

st.caption(f"Versi halaman: {datetime.now():%Y-%m-%d}. Untuk analitik & edukasi; bukan sistem peringatan dini real-time.")

# ------------------------------- | ------------------------------- | -------------------------------
# 7) Troubleshooting & FAQ
# ------------------------------- | ------------------------------- | -------------------------------
st.markdown('<div class="chip-title">🛠️ Troubleshooting & FAQ</div>', unsafe_allow_html=True)

with st.expander("Grafik tidak muncul atau kosong"):
    st.write(
        "Periksa apakah file data tersedia pada path yang benar dan tidak kosong. "
        "Jika menggunakan filter **Window**, coba set ke **Semua** untuk memastikan indeks tanggal tersedia."
    )

with st.expander("Forecast tidak menampilkan 95% CI"):
    st.write(
        "Pastikan kolom CI tersedia (`*_fc_lower`/`*_fc_upper`) di `df_merged_after_forecast.csv` atau tersedia di `forecast_results.csv`. "
        "Aktifkan toggle **Tampilkan 95% CI**."
    )

with st.expander("Peta klaster tidak tampil lebar"):
    st.write(
        "Pastikan file `data/jatim_kabkota.geojson` ada, dan nama kab/kota sudah ternormalisasi. "
        "Rasio lebar peta sudah diatur via bounding box; gunakan **use_container_width=True**."
    )

with st.expander("Apa arti model terbaik di kartu ringkasan?"):
    st.write(
        "Itu adalah model dengan metrik validasi paling baik (mis. MASE/sMAPE) pada target terpilih, "
        "diambil dari `forecast_results.csv`."
    )

with st.expander("Bagaimana membaca **Capacity alert**?"):
    st.write(
        "Itu **indikator operasional** (bukan sirene real-time). Jika **BOR > 80%** dan **TOI < 1 hari**, "
        "kapasitas bed padat dan turnover sangat cepat → evaluasi alur discharge, alokasi bed, dan rujukan."
    )

# ------------------------------- | ------------------------------- | -------------------------------
# 8) Navigasi Halaman
# ------------------------------- | ------------------------------- | -------------------------------
st.markdown('<div class="chip-title">🔗 Navigasi Halaman</div>', unsafe_allow_html=True)

with st.expander("🏠 Home", expanded=True):
    st.write("Hero banner, ringkasan, **EDA & Tren**, **Forecasting Result**, dan **Clustering Maps**.")
    _safe_page_link("1_🏠_Home.py", "Buka Home", "🏠")

with st.expander("🤖 JAWIR", expanded=False):
    st.write("Chatbot kesehatan berbasis Jawa Timur Open Data untuk tanya-jawab cepat & edukasi publik.")
    _safe_page_link("pages/2_🤖_JAWIR.py", "Buka JAWIR", "🤖")

with st.expander("📘 Panduan", expanded=False):
    st.write("Dokumentasi ringkas cara baca dan pakai dashboard (halaman ini).")
    _safe_page_link("pages/3_📖_Panduan Dashboard.py", "Muat Ulang Panduan", "📘")

# ------------------------------- | ------------------------------- | -------------------------------
# Footer mini (konsisten)
# ------------------------------- | ------------------------------- | -------------------------------
st.divider()
year = datetime.now().year
st.markdown(
    f"""
    <div style="text-align:center; margin-top: 6px;">
        <span style="opacity:0.85; font-size:0.9rem;">
            © {year} <strong>NutriHealth AI</strong> • Data: 
            <a href="https://opendata.jatimprov.go.id/" target="_blank" style="color:inherit; text-decoration:underline;">
                opendata.jatimprov.go.id
            </a> • Untuk tujuan analitik & edukasi.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
