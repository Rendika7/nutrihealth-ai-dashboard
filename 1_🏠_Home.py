# ------------------------------- | ------------------------------- | -------------------------------
# Import Library Needed
# ------------------------------- | ------------------------------- | -------------------------------
# Standard Library
import os
import time
import base64
import datetime
import json
import pathlib
from collections import Counter
import warnings

# Third-Party
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import dedent
import seaborn as sns
import geopandas as gpd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
import joblib

# Silence warnings
warnings.filterwarnings("ignore")

# Pandas display options
pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: f"{x:.4f}")

# Matplotlib defaults (optional)
plt.style.use("default")  # or another style if desired

# Seaborn defaults (optional)
sns.set_theme(context="notebook", style="whitegrid")


# ------------------------------- | ------------------------------- | -------------------------------
# Configuration Streamlit Web App
# ------------------------------- | ------------------------------- | -------------------------------

# Loading Image using PIL
web_icon = Image.open('icon/Only LOGO.png') # Adding Image to web app
st.set_page_config(page_title="NutriHealth AI Dashboard", layout="wide", initial_sidebar_state="auto", page_icon = web_icon)


# ------------------------------- | ------------------------------- | -------------------------------
# Popup Sambutan NutriHealth AI
# ------------------------------- | ------------------------------- | -------------------------------

# CSS: rapikan jarak vertikal <hr> di dalam st.dialog
st.markdown("""
<style>
div[data-testid="stDialog"] hr { margin: 0px 0 !important; }   /* default ~1rem */
</style>
""", unsafe_allow_html=True)

# Fungsi encode image ke base64 agar bisa di-embed di HTML <img>
def img_b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

# Dialog sambutan
@st.dialog(" ")
def welcome_dialog():
    
    img64 = img_b64("icon/Only LOGO.png")  # pakai slash, hindari spasi kalau bisa
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{img64}" width="250"/>
        </div>
        <h3 style='text-align:center; margin:0.5rem 0 0.75rem 0;'>
            NutriHealth AI: Generasi Emas 2045 Dashboard 🎉
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
**Misi singkat:** mempercepat penurunan stunting & menguatkan kesehatan ibu–anak menuju *Generasi Emas 2045*.

**Yang bisa kamu lihat di sini:**
- 🔮 **Hasil forecast bulanan** (ETS/SARIMA) dengan **95% CI** + ringkasan akurasi (MASE/sMAPE) — *kamu cukup membaca hasilnya; model sudah dijalankan.*
- 📈 **Insight EDA terkurasi**: ketimpangan tenaga (boxplot), tren tahunan/bulanan, **heatmap musiman OBGYN**, dan **korelasi**.
- 🏥 **Kapasitas RS**: **BOR, TOI, HI, BTO, IdleShare** + label **BOR_status/TOI_status** untuk interpretasi cepat.
- 👶 **MNCH**: **ASI (target ≥ 80%)**, **BBLR**, dan layanan **OBGYN** sebagai outcome.
- 🚩 **Capacity alert** sebagai **insight berbasis ambang** *(BOR > 85% & TOI < 1)* — **bukan** trigger real-time.
- 🤖 **JAWIR Chatbot** untuk tanya-jawab cepat berbasis Jawa Timur Open Data.
        """
    )
    st.divider()

    # CSS: cegah wrapping teks pada semua st.button
    st.markdown("""
    <style>
    .stButton > button { white-space: nowrap; }
    </style>
    """, unsafe_allow_html=True)

    st.caption("Pilih aksi cepat:")

    # Lebarin kolom tengah (tombol JAWIR)
    c1, c2, c3 = st.columns([1, 1.35, 1])  # tweak 1.3–1.5 sesuai lebar yang kamu mau

    with c1:
        start = st.button("🚀 Mulai Jelajah", use_container_width=True)
    with c2:
        # NBSP agar 'JAWIR' & 'Chatbot' nempel (nggak bisa di-break)
        chatbot = st.button("🤖 JAWIR Chatbot", use_container_width=True)
    with c3:
        helpme = st.button("📘 Panduan Dashboard", use_container_width=True)

    if start:
        st.session_state.welcomed = True
        st.toast("Selamat menjelajah! 🎯")
        st.rerun() # <= TUJUAN 1: hanya tutup dialog & tetap di halaman ini

    if chatbot:
        st.session_state.welcomed = True
        st.session_state.show_chatbot = True
        st.switch_page("pages/2_🤖_JAWIR.py")       # <= TUJUAN 2
        st.toast("Membuka JAWIR… 🤖")
        st.rerun()

    if helpme:
        st.session_state.welcomed = True
        st.session_state.show_help = True
        st.switch_page("pages/3_📖_Panduan Dashboard.py")       # <= TUJUAN 3
        st.toast("Membuka panduan singkat… 📘")
        st.rerun()

# Tampilkan dialog sekali saat pertama kali halaman dibuka
if "welcomed" not in st.session_state:
    welcome_dialog()
else:
    st.toast("Welcome back to NutriHealth AI!", icon="🎉")
    time.sleep(0.5)
    st.toast("Semoga harimu menyenangkan!" , icon="☀️")
    time.sleep(0.5)
    st.toast("Ayo jelajahi insight-nya!", icon="🚀")
    
# ------------------------------- | ------------------------------- | -------------------------------
# Sidebar Configuration — NutriHealth AI
# ------------------------------- | ------------------------------- | -------------------------------

with st.sidebar:
    # Logo / GIF (opsional)
    st.image("icon/Only LOGO.png", use_container_width=True)

    # Informasi Dashboard (Sidebar)
    with st.sidebar.expander("ℹ️ Dashboard"):
        st.markdown(
            """
    <strong>NutriHealth AI</strong> adalah dashboard analitik untuk <strong>Kesehatan Ibu–Anak & Kapasitas RS di Jawa Timur</strong>.
    Platform ini menggabungkan <em>EDA</em> (eksplorasi data) dan <em>statistical forecasting</em> (S-Naïve · ETS · SARIMAX)
    guna memantau tren, memproyeksikan 18 bulan ke depan, dan memberi sinyal area prioritas kebijakan.
            """,
            unsafe_allow_html=True
        )

    # Catatan di Sidebar
    with st.sidebar.expander("⚠️ Catatan Penting"):
        st.markdown(
            """
    Grafik yang ditampilkan menggunakan data yang sudah melalui **processing** dan siap dianalisis (EDA & Forecasting).
            """
        )

# ------------------------------- | ------------------------------- | -------------------------------
# banner gambar sebagai hero image
# ------------------------------- | ------------------------------- | -------------------------------

# Menampilkan banner gambar sebagai hero image  ========================================
st.image('source\Main Hero Banner.jpg', use_container_width=True)

# ------------------------------- | ------------------------------- | -------------------------------
# Isi dari Dashboard NutriHealth AI
# # ------------------------------- | ------------------------------- | -------------------------------

# CSS untuk memposisikan tabs di tengah
st.markdown("""
    <style>
        div[data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Membuat Tabs untuk membagi tampilan menjadi beberapa section
tab1, tab2, tab3 = st.tabs(["📈 EDA & Tren", "🔮 Forecasting Result", "🗺️ Clustering Maps"])

# -------------------------------------- Tab 1: EDA & Tren -------------------------------------- #
with tab1:
    # Custom CSS untuk sub-section title
    st.markdown("""
        <style>
            .sub-section-title {
                text-align: center;
                font-size: 24px;        /* lebih kecil dari sebelumnya */
                font-weight: 600;
                padding: 10px;          /* lebih tipis */
                background-color: #88CD33; 
                color: white;
                border-radius: 6px;
                margin-top: 15px;
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)


    # ------------------------------- >>> Sub-section: Profil Tenaga Kesehatan & Layanan OBGYN ------------------------------- #
    
    # Tampilkan sub-section title
    st.markdown('<div class="sub-section-title">🧑‍⚕️ Profil Tenaga Kesehatan & Layanan OBGYN</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Folder path
    dataPath = os.path.join('data', 'ABT_Master.csv')
    df = pd.read_csv(dataPath) # Load Data

    df_cluster1 = df[[
    "Date",
    "Jumlah Bidan",
    "Jumlah Perawat",
    "Jumlah Dokter Umum",
    "Jumlah Ahli Gizi",
    "Layanan OBGYN"]]  
    
    df_cluster1['Date'] = pd.to_datetime(df_cluster1['Date'])

    # Drop baris kosong tanpa overwrite df
    cleaned_df = df_cluster1.dropna(how="all")
    cleaned_df = cleaned_df.dropna(subset=["Jumlah Bidan", "Jumlah Perawat", "Jumlah Dokter Umum", "Jumlah Ahli Gizi"])
    # --- Tambah kolom Tahun ---
    cleaned_df["Year"] = pd.to_datetime(cleaned_df["Date"]).dt.year

    # Membuat dua kolom untuk menampilkan informasi
    col1, col2 = st.columns([5, 5])  # Kolom pertama lebih kecil (5) dan kolom kedua lebih besar (5)

    # Kolom Kiri: Informasi Data dan Metric
    with col1:
        # --- [1.] Boxplot (Outlier Detection) ---
        # Drop kolom Date biar hanya numerik yang diplot
        df_box = df_cluster1.drop(columns=["Date"], errors="ignore")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.boxplot(data=df_box, ax=ax)

        ax.set_title("Boxplot Variabel Tenaga Kesehatan & Layanan", fontsize=25, pad=22, fontweight="bold")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')

        st.pyplot(fig)
            
        
        
        # --- [3.] Tren Jumlah Tenaga Kesehatan ---
        
        # Tentukan kolom tenaga kesehatan
        cols = ["Jumlah Bidan", "Jumlah Perawat", "Jumlah Dokter Umum", "Jumlah Ahli Gizi"]

        # Ubah ke long format
        df_long = cleaned_df.melt(
            id_vars="Date",
            value_vars=cols,
            var_name="Tenaga Kesehatan",
            value_name="Jumlah"
        )

        # Buat line chart satu figure
        fig = px.line(
            df_long,
            x="Date",
            y="Jumlah",
            color="Tenaga Kesehatan",
            markers=True,
            title="Tren Jumlah Tenaga Kesehatan"
        )

        # Title & legend: center, no overlap
        fig.update_layout(
            title=dict(
                text="Tren Jumlah Tenaga Kesehatan",
                x=0.5, xanchor="center",
                y=1, yanchor="top",         # judul sedikit di bawah tepi atas
                font=dict(size=18)
            ),
            legend=dict(
                orientation="h",
                x=0.5, xanchor="center",
                y=1.00, yanchor="bottom"       # legend di atas area plot, di bawah judul
            ),
            margin=dict(t=90),                # ruang atas cukup
            xaxis_title="Tanggal",
            yaxis_title="Jumlah",
            xaxis=dict(tickangle=45),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # Tambahkan kolom Year dan Month
        df_cluster1["Year"] = df_cluster1["Date"].dt.year
        df_cluster1["Month"] = df_cluster1["Date"].dt.month

        # Pivot tabel
        pivot = df_cluster1.pivot_table(values="Layanan OBGYN", index="Year", columns="Month", aggfunc="mean")

        # Plot heatmap interaktif
        fig = px.imshow(
            pivot,
            text_auto=".0f",                  # tampilkan angka rata-rata
            aspect="auto",
            color_continuous_scale="YlOrRd",  # sama seperti seaborn
            title="Heatmap Rata-rata Layanan OBGYN (Tahun vs Bulan)"
        )

        # Styling title & axis
        fig.update_layout(
            title=dict(
                text="Heatmap Rata-rata Layanan OBGYN<br>(Tahun vs Bulan)",
                x=0.5, xanchor="center",
                y=0.97, yanchor="top",
                font=dict(size=18)
            ),
            xaxis_title="Bulan",
            yaxis_title="Tahun",
            margin=dict(t=60)
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig, use_container_width=True)
        

        
    # Kolom Kiri: Informasi Data dan Metric
    with col2:
        # --- [2.] Rata-rata Jumlah Tenaga Kesehatan per Tahun ---
        
        # --- Hitung rata-rata per tahun ---
        avg_yearly = (
            cleaned_df.groupby("Year")[["Jumlah Bidan", "Jumlah Perawat",
                                        "Jumlah Dokter Umum", "Jumlah Ahli Gizi"]]
            .mean()
            .reset_index()
        )

        # --- Ubah ke long format biar cocok untuk Plotly ---
        avg_long = avg_yearly.melt(
            id_vars="Year",
            value_vars=["Jumlah Bidan", "Jumlah Perawat", "Jumlah Dokter Umum", "Jumlah Ahli Gizi"],
            var_name="Tenaga Kesehatan",
            value_name="Rata-rata"
        )

        # --- Plot Barchart ---
        fig = px.bar(
            avg_long,
            x="Year",
            y="Rata-rata",
            color="Tenaga Kesehatan",
            barmode="group",
            text="Rata-rata",
            title="Rata-rata Jumlah Tenaga Kesehatan per Tahun"
        )

        # Atur tampilan teks & layout
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(
            title=dict(
                text="Rata-rata Jumlah Tenaga Kesehatan per Tahun",
                x=0.5,                # rata tengah
                xanchor="center",
                y=1,               # geser judul lebih ke bawah
                yanchor="top",
                font=dict(size=18)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.00,               # geser legend lebih ke atas
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=90)        # tambah ruang atas supaya gak tabrakan
        )
        # Tampilkan di Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # --- [4.] Tren Layanan OBGYN (Asli vs Rolling 3 Bulan) ---
        
        # Rolling Mean Layanan OBGYN 
        df_plot = df_cluster1[["Date", "Layanan OBGYN"]].copy()
        df_plot["Rolling 3 Bulan"] = df_plot["Layanan OBGYN"].rolling(window=3).mean()

        # Ubah ke long format supaya bisa multi-line di plotly express
        df_long = df_plot.melt(
            id_vars="Date",
            value_vars=["Layanan OBGYN", "Rolling 3 Bulan"],
            var_name="Series",
            value_name="Jumlah"
        )

        # Plot
        fig = px.line(
            df_long,
            x="Date",
            y="Jumlah",
            color="Series",
            markers=True,
            title="Tren Layanan OBGYN (Asli vs Rolling 3 Bulan)"
        )

        # Styling title & legend
        fig.update_layout(
            title=dict(
                text="Tren Layanan OBGYN (Asli vs Rolling 3 Bulan)",
                x=0.5, xanchor="center",
                y=1, yanchor="top",
                font=dict(size=18)
            ),
            legend=dict(
                orientation="h",
                x=0.5, xanchor="center",
                y=1.00, yanchor="bottom"   # legend di atas plot, tidak tabrakan dengan title
            ),
            margin=dict(t=80),            # kasih ruang supaya title & legend gak tabrakan
            xaxis_title="Tanggal",
            yaxis_title="Jumlah",
            height=500
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # --- [6.] Correlation Matrix Antar Variabel ---


        # Hitung korelasi (drop kolom Date)
        corr = df_cluster1.drop(columns=["Date"], errors="ignore").corr()

        # Plot heatmap interaktif
        fig = px.imshow(
            corr,
            text_auto=".2f",        # tampilkan nilai korelasi
            aspect="auto",
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1,
        )

        # Styling title
        fig.update_layout(
            title=dict(
                text="Correlation Matrix Antar Variabel",
                x=0.5, xanchor="center",
                y=0.97, yanchor="top",
                font=dict(size=18)
            ),
            margin=dict(t=60)
        )

        # Tampilkan di Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # ------------------------------- >>> Sub-section: Outcome Kesehatan Ibu & Anak ------------------------------- #
    st.markdown('<div class="sub-section-title">👩‍🍼 Outcome Kesehatan Ibu & Anak</div>', unsafe_allow_html=True)

    df_cluster2 = df[["Date","Persentase_ASI", "Rasio_BBLR", "Rasio_AKI", "Rasio_AKB"]] 
    df_cluster2['Date'] = pd.to_datetime(df_cluster2['Date'], errors="coerce") # --- 1. Tipe data datetime ---

    TARGET_ASI = 0.80 # operasional: ≥80% Realistis naik dari baseline 2024 (78,8%) → dorongan +1,2 pp masih “make sense”. “…cakupan ASI eksklusif… mencapai 78,8% (2024).”
    df_cluster2["ASI_gap_target"] = df_cluster2["Persentase_ASI"] - TARGET_ASI # seberapa jauh dari target ASI eksklusif (positif = on track)
    
    # --- [10.] Line Chart (Rasio AKI dan Rasio AKB) & (Persentase ASI dan Rasio BBLR) ---

    # --- Siapkan data ---
    df_plot = df_cluster2.copy()
    df_plot["Date"] = pd.to_datetime(df_plot["Date"], errors="coerce")

    # Long format untuk masing-masing figure
    long_asi_bblr = df_plot.melt(
        id_vars="Date",
        value_vars=["Persentase_ASI", "Rasio_BBLR"],
        var_name="Variabel",
        value_name="Nilai"
    )

    long_aki_akb = df_plot.melt(
        id_vars="Date",
        value_vars=["Rasio_AKI", "Rasio_AKB"],
        var_name="Variabel",
        value_name="Nilai"
    )

    # --- Figure 1: Persentase_ASI & Rasio_BBLR (warna biru-hijau) ---
    fig_asi_bblr = px.line(
        long_asi_bblr,
        x="Date", y="Nilai", color="Variabel",
        markers=True,
        title="Persentase ASI & Rasio BBLR",
        color_discrete_map={
        "Persentase_ASI": "#0b6aae",  # biru tua
        "Rasio_BBLR": "#78bbe1"       # biru muda
        }
    )
    fig_asi_bblr.update_layout(
        title=dict(text="Persentase ASI & Rasio BBLR", x=0.32, y=0.98, font=dict(size=20)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.10, yanchor="bottom"),
        margin=dict(t=110, l=40, r=20, b=40),
        xaxis_title="Tanggal",
        yaxis_title="Nilai",
        hovermode="x unified",
        height=500
    )
    fig_asi_bblr.update_xaxes(tickangle=45)

    # --- Figure 2: Rasio_AKI & Rasio_AKB (warna oranye-merah) ---
    fig_aki_akb = px.line(
        long_aki_akb,
        x="Date", y="Nilai", color="Variabel",
        markers=True,
        title="Rasio AKI & Rasio AKB",
        color_discrete_map={
        "Rasio_AKI": "#ff7f0e",  # oranye tua
        "Rasio_AKB": "#fdae6b"   # oranye muda
        }
    )
    fig_aki_akb.update_layout(
        title=dict(text="Rasio AKI & Rasio AKB", x=0.32, y=0.98, font=dict(size=20)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.10, yanchor="bottom"),
        margin=dict(t=110, l=40, r=20, b=40),
        xaxis_title="Tanggal",
        yaxis_title="Nilai",
        hovermode="x unified",
        height=500
    )
    fig_aki_akb.update_xaxes(tickangle=45)

    # --- Tampilkan berdampingan di Streamlit ---
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_asi_bblr, use_container_width=True)
    with c2:
        st.plotly_chart(fig_aki_akb, use_container_width=True)


    # --- [11.] Scatter (Persentase_ASI vs Rasio_AKI) & (Persentase_ASI vs Rasio_AKB) ---
    
    # Ambil min dan max Persentase_ASI
    x_min = 0.65
    x_max = df_cluster2["Persentase_ASI"].max()

    # --- Scatter Persentase_ASI vs Rasio_AKI ---
    fig1 = px.scatter(
        df_cluster2, x="Persentase_ASI", y="Rasio_AKI",
        trendline="ols", trendline_color_override="red",
        title="Persentase ASI vs Rasio AKI"
    )
    fig1.update_layout(
        title=dict(text="Persentase ASI vs Rasio AKI", x=0.4, font=dict(size=20)),
        xaxis_title="Persentase ASI", yaxis_title="Rasio AKI", height=400
    )
    fig1.update_xaxes(range=[x_min * 0.98, x_max * 1.02])  # kasih padding 2%

    # --- Scatter Persentase_ASI vs Rasio_AKB ---
    fig2 = px.scatter(
        df_cluster2, x="Persentase_ASI", y="Rasio_AKB",
        trendline="ols", trendline_color_override="red",
        title="Persentase ASI vs Rasio AKB"
    )
    fig2.update_layout(
        title=dict(text="Persentase ASI vs Rasio AKB", x=0.4, font=dict(size=20)),
        xaxis_title="Persentase ASI", yaxis_title="Rasio AKB", height=400
    )
    fig2.update_xaxes(range=[x_min * 0.98, x_max * 1.02])  # sama padding

    # --- Tampilkan di Streamlit ---
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.plotly_chart(fig2, use_container_width=True)



    fig_gap = px.histogram(
        df_cluster2,
        x="ASI_gap_target",
        nbins=20,
        title="Distribusi ASI_gap_target (ASI − 0.80)"
    )
    fig_gap.add_shape(
        type="line",
        x0=0, x1=0, y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="red", width=2, dash="dash")
    )
    fig_gap.add_annotation(x=0, y=1, yref="paper", text="On target (gap=0)", showarrow=False, yshift=12, font=dict(color="red"))
    fig_gap.update_layout(title=dict(text="Distribusi ASI_gap_target (ASI − 0.80)", x=0.35, font=dict(size=18)),
                        xaxis_title="Gap terhadap Target", yaxis_title="Frekuensi", margin=dict(t=90))

    st.plotly_chart(fig_gap, use_container_width=True)

    # ------------------------------- >>> Sub-section: Kapasitas & Mutu Layanan Rumah Sakit ------------------------------- #
    st.markdown('<div class="sub-section-title">🏨 Kapasitas & Mutu Layanan Rumah Sakit</div>', unsafe_allow_html=True)

    df_cluster3 = df[["Date","AVLOS (Day)", "BOR (%)", "GDR (/K)", "NDR (/K)", "TOI (Day)"]] 
    df_cluster3['Date'] = pd.to_datetime(df_cluster3['Date'], errors="coerce") # --- 1. Tipe data datetime ---
    df_cluster3 = df_cluster3.dropna() # --- 2. Drop baris kosong ---
    df_cluster3 = df_cluster3.reset_index(drop=True) # --- 3. Reset indeks ---
    df_cluster3["Year"] = df_cluster3["Date"].dt.year # --- 4. Tambah kolom Tahun ---
    
    # # Feature Engineering: bikin fitur-fitur bulanan yang bermakna untuk analisis/monitoring RS (tanpa lag/rolling)
    df_cluster3['days_in_month'] = df_cluster3['Date'].dt.days_in_month # panjang bulan (28–31) untuk normalisasi/perbandingan adil
    # # --- Operasional bed / aliran pasien ---
    df_cluster3['HI'] = df_cluster3['AVLOS (Day)'] + df_cluster3['TOI (Day)'] # Hospitalization Interval: lama siklus bed (dirawat + jeda)
    # NOTE: jika ada risiko pembagian nol, tambahkan epsilon kecil di penyebut (opsional)
    df_cluster3['BTO_month'] = df_cluster3['days_in_month'] / (df_cluster3['HI']) # Bed Turnover per bulan: berapa kali 1 bed “berputar”/bulan
    df_cluster3['IdleShare'] = 1 - df_cluster3['BOR (%)']/100.0 # porsi bed menganggur (1 - occupancy)
    # --- Mortalitas rawat inap ---
    df_cluster3['EDR'] = np.maximum(0, df_cluster3['GDR (/K)'] - df_cluster3['NDR (/K)']) # Early-Death Component ≈ kematian <48 jam (triase/emergency)

    # --- Kategori manajerial ---
    def bor_status(x):
        # Kategori utilisasi bed: <60% under, 60–85% optimal, >85% saturated
        if np.isnan(x): return np.nan
        if x < 60: return 'under-utilized'
        if x <= 80: return 'optimal'
        return 'saturated'

    def toi_status(x):
        # Kategori interval jeda antar pasien: <1 hari cepat, 1–3 sehat, >3 lambat
        if np.isnan(x): return np.nan
        if x < 1: return 'cepat'
        if x <= 3: return 'sehat'
        return 'lambat'

    df_cluster3['BOR_status'] = df_cluster3['BOR (%)'].apply(bor_status)      # label utilisasi tempat tidur
    df_cluster3['TOI_status'] = df_cluster3['TOI (Day)'].apply(toi_status)    # label kecepatan turnover bed
    df_cluster3['Capacity_alert'] = ((df_cluster3['BOR (%)'] > 80) &          # alert kapasitas: bed padat + jeda sangat cepat
                            (df_cluster3['TOI (Day)'] < 1)).astype(int)


    # --- [7.] Distribusi Kategori (BOR_status, TOI_status, Capacity_alert) ---
    cat_cols = ["BOR_status", "TOI_status", "Capacity_alert"]

    # Siapkan figure: 1 baris, 3 kolom
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[f"Distribusi {c}" for c in cat_cols]
    )

    # Tambahkan bar chart per kolom kategori
    for i, col in enumerate(cat_cols, start=1):
        counts = df_cluster3[col].value_counts(dropna=False).sort_index()
        x_vals = [str(x) for x in counts.index]  # pastikan string (termasuk NaN -> 'nan')
        y_vals = counts.values

        fig.add_trace(
            go.Bar(
                x=x_vals,
                y=y_vals,
                text=y_vals,
                textposition="outside",
                hovertemplate=col + ": %{x}<br>Count: %{y}<extra></extra>",
                showlegend=False
            ),
            row=1, col=i
        )

        # Estetika sumbu X tiap subplot
        fig.update_xaxes(
            title_text=col,
            tickangle=0,
            categoryorder="array",
            categoryarray=x_vals,   # urut sesuai index sort
            row=1, col=i
        )

    # Layout umum
    fig.update_layout(
        title=dict(
            text="Distribusi Kategori (BOR_status, TOI_status, Capacity_alert)",
            x=0.5, xanchor="center",
            y=0.95, yanchor="top",
            font=dict(size=20)
        ),
        height=450,
        margin=dict(t=90, l=40, r=20, b=40),
        bargap=0.25,
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # --- [8.] Korelasi Variabel Numerik Kapasitas RS ---
    
    numeric_cols = ["AVLOS (Day)", "BOR (%)", "GDR (/K)", "NDR (/K)",
                "TOI (Day)", "HI", "BTO_month", "IdleShare", "EDR"]
    
    # Hitung korelasi
    corr = df_cluster3[numeric_cols].corr()

    # Plot heatmap dengan Plotly Express
    fig = px.imshow(
        corr,
        text_auto=".2f",                 # tampilkan nilai korelasi
        aspect="auto",
        color_continuous_scale="RdYlBu", # sama seperti seaborn
        zmin=-1, zmax=1
    )

    # Styling title & layout
    fig.update_layout(
        title=dict(
            text="Heatmap Korelasi Variabel Numerik",
            x=0.5, xanchor="center",
            y=0.95, yanchor="top",
            font=dict(size=20)
        ),
        margin=dict(t=50)  # ruang atas supaya title & colorbar tidak tabrakan
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)


    # --- Data siap plot ---
    df_plot = df_cluster3.copy()
    df_plot["Date"] = pd.to_datetime(df_plot["Date"], errors="coerce")

    group1 = ["BOR (%)", "GDR (/K)", "EDR", "NDR (/K)"]
    group2 = ["AVLOS (Day)", "TOI (Day)", "HI", "BTO_month", "IdleShare"]

    # =========================
    # Figure 1 (kiri): group1
    # =========================
    fig1 = go.Figure()
    for c in group1:
        fig1.add_trace(
            go.Scatter(
                x=df_plot["Date"], y=df_plot[c],
                mode="lines+markers",
                name=c,
                hovertemplate=c + ": %{y:.2f}<br>Tanggal: %{x|%Y-%m-%d}<extra></extra>"
            )
        )

    fig1.update_layout(
        title=dict(text="Tren Waktu: BOR, GDR, EDR, NDR", x=0.20, y=0.98, font=dict(size=20)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.10, yanchor="bottom"),
        hovermode="x unified",
        height=520,
        xaxis_title="Tanggal",
        yaxis_title="Nilai"
    )
    fig1.update_xaxes(tickangle=45)

    # =========================
    # Figure 2 (kanan): group2
    # =========================
    fig2 = go.Figure()
    for c in group2:
        fig2.add_trace(
            go.Scatter(
                x=df_plot["Date"], y=df_plot[c],
                mode="lines+markers",
                name=c,
                hovertemplate=c + ": %{y:.2f}<br>Tanggal: %{x|%Y-%m-%d}<extra></extra>"
            )
        )

    fig2.update_layout(
        title=dict(text="Tren Waktu: AVLOS, TOI, HI, BTO, IdleShare", x=0.32, y=0.98, font=dict(size=20)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.10, yanchor="bottom"),
        hovermode="x unified",
        height=520,
        xaxis_title="Tanggal",
        yaxis_title="Nilai"
    )
    fig2.update_xaxes(tickangle=45)

    # =========================
    # Tampilkan berdampingan
    # =========================
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(fig1, use_container_width=True)
    with col_right:
        st.plotly_chart(fig2, use_container_width=True)



    # --- [9.] Korelasi Variabel Numerik Kapasitas RS ---

    # Ubah ke long format untuk Plotly
    df_long = df_cluster3[numeric_cols].melt(var_name="Variabel", value_name="Nilai")

    # Plot boxplot interaktif
    fig = px.box(
        df_long,
        x="Variabel",
        y="Nilai",
        color="Variabel",
        points="outliers",   # tampilkan outlier
        title="Boxplot Variabel Numerik",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    # Styling
    fig.update_layout(
        title=dict(
            text="Boxplot Variabel Numerik",
            x=0.5, xanchor="center",
            font=dict(size=20)
        ),
        xaxis=dict(title="Variabel", tickangle=45),
        yaxis_title="Nilai",
        showlegend=False,
        margin=dict(t=80, l=40, r=20, b=40),
        height=600
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)



# -------------------------------------- Tab 2: Hasil Forecasting -------------------------------------- #
with tab2:
    st.markdown(
        '<div class="sub-section-title">📈 Hasil Forecasting Kapasitas RS & Outcome Kesehatan Ibu–Anak</div>',
        unsafe_allow_html=True
    )
        
    st.markdown(
        """
        Hasil di bawah menampilkan **riwayat aktual** dan **prediksi ke depan** untuk indikator terpilih. Area berwarna menunjukkan **95% confidence interval** (ketidakpastian prediksi). ***Gunakan kontrol di bawah untuk mengganti indikator, membatasi periode tampil, atau menonaktifkan CI.***
        """
    )

    # ---- Load hasil (kamu sudah punya file ini)
    fr   = pd.read_csv("data/forecast_results.csv")
    df_f = pd.read_csv("data/df_merged_after_forecast.csv")
    df_f["Date"] = pd.to_datetime(df_f["Date"], errors="coerce")
    df_f = df_f.sort_values("Date").set_index("Date")
    fr["date"] = pd.to_datetime(fr["date"], errors="coerce")

    # ---- Daftar indikator
    target_cols = [
        "BOR (%)", "AVLOS (Day)", "NDR (/K)", "GDR (/K)", "TOI (Day)",
        "Rasio_AKI", "Rasio_AKB", "Rasio_BBLR"
    ]

    # ========= UI Kontrol =========
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        target = st.selectbox("Pilih indikator", target_cols, index=0)
    with c2:
        window_opt = st.selectbox("Window (bulan terakhir)", ["Semua", 12, 24, 36, 48], index=0)
        window_months = None if window_opt == "Semua" else int(window_opt)
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_ci = st.toggle("Tampilkan 95% CI", value=True)  # <<-- toggle 


    # ========= Ambil series aktual & forecast =========
    if target not in df_f.columns:
        st.error(f"Kolom '{target}' tidak ditemukan di data.")
        st.stop()

    y = df_f[target]

    # coba ambil CI langsung dari df_f; kalau tidak ada → fallback ke fr
    low_col = f"{target}_fc_lower"
    up_col  = f"{target}_fc_upper"
    if low_col in df_f.columns and up_col in df_f.columns:
        lower = df_f[low_col]
        upper = df_f[up_col]
    else:
        fr_t   = fr[fr["target"] == target].set_index("date").sort_index()
        lower  = fr_t["yhat_lower"].rename(low_col).reindex(y.index)
        upper  = fr_t["yhat_upper"].rename(up_col).reindex(y.index)

    # periode forecast ditandai oleh keberadaan CI
    fc_mask = ~lower.isna()

    # ========= Window opsional =========
    if window_months is not None:
        end   = y.index.max()
        start = end - pd.DateOffset(months=window_months - 1)
        y     = y.loc[start:end]
        lower = lower.reindex(y.index)
        upper = upper.reindex(y.index)
        fc_mask = ~lower.isna()

    # pisahkan actual vs forecast
    y_actual   = y[~fc_mask]
    y_forecast = y[fc_mask]
    bridge = pd.concat([y_actual.tail(1), y_forecast]) if (len(y_actual) and len(y_forecast)) else y_forecast.copy()

    # ========= Ringkasan angka (kartu) =========
    last_actual_txt = y_actual.index.max().strftime("%Y-%m") if len(y_actual) else "–"
    first_fc_txt    = y_forecast.index.min().strftime("%Y-%m") if len(y_forecast) else "–"
    last_fc_txt     = y_forecast.index.max().strftime("%Y-%m") if len(y_forecast) else "–"

    # cari nama model dari forecast_results (jika tersedia)
    model_name = "-"
    if len(fr[fr["target"] == target]):
        model_name = fr.loc[fr["target"] == target, "model"].dropna().iloc[0]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Last Actual", last_actual_txt)
    k2.metric("First Forecast", first_fc_txt)
    k3.metric("Last Forecast", last_fc_txt)
    k4.metric("Model Terbaik", model_name)

    # ========= Plotly: Actual vs Forecast =========
    fig = go.Figure()

    if len(y_actual):
        fig.add_trace(go.Scatter(
            x=y_actual.index, y=y_actual.values,
            mode="lines+markers",
            name="Actual",
            hovertemplate="Tanggal: %{x|%Y-%m}<br>Nilai: %{y:.2f}<extra></extra>"
        ))

    if len(bridge):
        fig.add_trace(go.Scatter(
            x=bridge.index, y=bridge.values,
            mode="lines+markers",
            name="Forecast",
            line=dict(dash="solid"),
            hovertemplate="Tanggal: %{x|%Y-%m}<br>Nilai: %{y:.2f}<extra></extra>"
        ))

    if show_ci and len(y_forecast):
        idx_fc = y_forecast.index
        fig.add_trace(go.Scatter(
            x=idx_fc, y=upper.loc[idx_fc].values,
            line=dict(width=0), showlegend=False, hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=idx_fc, y=lower.loc[idx_fc].values,
            fill="tonexty", name="95% CI", line=dict(width=0),
            opacity=0.2, hovertemplate="Lower: %{y:.2f}<extra></extra>"
        ))

    subtitle = (
        f"last actual: {last_actual_txt} · forecast: {first_fc_txt} → {last_fc_txt}"
        if len(y_forecast) else f"last actual: {last_actual_txt}"
    )

    fig.update_layout(
        title=dict(text=f"{target} — Actual & Forecast<br><sup>{subtitle}</sup>",
                   x=0.02, font=dict(size=18)),
        xaxis_title="Tanggal", yaxis_title=target,
        hovermode="x unified",
        margin=dict(t=90, l=40, r=20, b=40),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=1.10, yanchor="bottom"),
        height=430
    )
    fig.update_xaxes(tickformat="%Y-%m", ticks="outside")

    st.plotly_chart(fig, use_container_width=True)

    # # (Opsional) tabel kecil contoh 10 baris forecast_res untuk indikator terpilih
    # with st.expander("Lihat tabel ringkas hasil forecast (top 10)"):
    #     tmp = fr[fr["target"] == target].sort_values("date").head(10)
    #     st.dataframe(tmp, use_container_width=True)
    
    with st.expander("Lihat tabel ringkas hasil forecast"):
        # opsi jumlah baris
        row_opt = st.selectbox(
            "Tampilkan berapa baris?",
            options=["5", "10", "20", "50", "Full"],
            index=1  # default ke 10
        )

        tmp = fr[fr["target"] == target].sort_values("date")

        if row_opt != "Full":
            n = int(row_opt)
            tmp = tmp.head(n)  # ambil n baris teratas

        st.dataframe(tmp, use_container_width=True)



# -------------------------------------- Tab 3: Clustering Maps -------------------------------------- #
with tab3:
    def clean_nama_daerah(name: str) -> str:
        name = name.strip().upper()
        if name.startswith("KABUPATEN"):
            daerah = name.replace("KABUPATEN", "").strip().title()
            return daerah
        elif name.startswith("KOTA"):
            daerah = name.replace("KOTA", "").strip().title()
            return daerah
        else:
            return name.title()
        
    


    # ------------------------------- >>> Sub-section: Peta Cluster Kesehatan Kabupaten/Kota di Jawa Timur ------------------------------- #
    st.markdown('<div class="sub-section-title">🗺️ Peta Cluster Kesehatan Kabupaten/Kota di Jawa Timur</div>', unsafe_allow_html=True)

    # ===== 1) Data =====
    df_cl = pd.read_csv("data/Cluster-ABT-v2.csv")
    df_cl = df_cl.drop_duplicates(subset=["nama_kabupaten_kota"], keep="first")
    df_cl["nama_norm"] = df_cl["nama_kabupaten_kota"].apply(clean_nama_daerah)

    gdf = gpd.read_file("data/jatim_kabkota.geojson")
    gdf["nama_norm"] = gdf["NAME_2"].apply(lambda x: x.strip() if isinstance(x, str) else x)

    merged = gdf.merge(df_cl, on="nama_norm", how="left")

    # Label & warna
    cluster_label_map = {0: "Perlu Diperhatikan", 1: "Baik", 2: "Warning", 3: "Cukup"}
    merged["Cluster_label"] = merged["Cluster"].map(cluster_label_map).fillna("Lainnya")

    color_map = {
        "Perlu Diperhatikan": "#d00000",  # merah terang
        "Warning":             "#f1c40f",  # kuning
        "Cukup":               "#74c69d",  # hijau muda
        "Baik":                "#2d6a4f",  # hijau tua
        "Lainnya":             "#bdbdbd"   # abu (missing)
    }
    legend_order = ["Perlu Diperhatikan", "Warning", "Cukup", "Baik", "Lainnya"]

    # ===== 2) Siapkan GeoJSON untuk Plotly =====
    merged = merged.reset_index().rename(columns={"index": "fid"})   # id unik
    geojson_obj = json.loads(merged.to_json())
    feature_key = "properties.fid"

    # ===== 3) Choropleth =====
    fig = px.choropleth(
        merged,
        geojson=geojson_obj,
        locations="fid",
        featureidkey=feature_key,
        color="Cluster_label",
        category_orders={"Cluster_label": legend_order},
        color_discrete_map=color_map,
        hover_name="nama_norm",
        hover_data={
            "Cluster_label": True,
            "indeks_kesehatan": True,
            "jumlah_bayi_bblr": True,
            "jumlah_kematian_ibu": True,
            "fid": False
        },
        title=" "
    )

    # Garis batas & hovertemplate rapi
    fig.update_traces(
        marker_line_width=0.8,
        marker_line_color="#FFFFFF",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Cluster: %{z}<br>"
            "Indeks Kesehatan: %{customdata[1]:.2f}<br>"
            "BBLR (jumlah): %{customdata[2]:,.0f}<br>"
            "Kematian Ibu (jumlah): %{customdata[3]:,.0f}<extra></extra>"
        )
    )

    # === KUNCI BIAR LEBAR ===
    # Hitung bounding box (EPSG:4326), lalu set lon/lat range agar rasio horizontal maksimal
    minx, miny, maxx, maxy = merged.to_crs(epsg=4326).geometry.total_bounds
    pad_x = (maxx - minx) * 0.08    # padding kanan-kiri
    pad_y = (maxy - miny) * 0.12    # padding atas-bawah

    fig.update_geos(
        projection_type="mercator",
        lonaxis_range=[minx - pad_x, maxx + pad_x],
        lataxis_range=[miny - pad_y, maxy + pad_y],
        visible=False
    )

    # Layout responsif (width ikut container Streamlit)
    fig.update_layout(
        title=dict(text=" ", x=0.5, font=dict(size=18)),
        legend=dict(title="Kategori Cluster", orientation="h",
                    x=0.5, xanchor="center", y=1.02, yanchor="bottom"),
        autosize=True,
        height=600,  # 480–560 ok; makin kecil → terasa lebih melebar
        margin=dict(t=70, l=10, r=10, b=10),
        hoverlabel=dict(bgcolor="white", font_size=12)
    )

    # (Opsional) Label centroid singkat
    centroids = merged.geometry.centroid.to_crs(epsg=4326)
    merged["lon"] = centroids.x
    merged["lat"] = centroids.y
    merged["label_short"] = (
        merged["nama_norm"].str.replace("Kabupaten ", "", case=False)
                            .str.replace("Kota ", "", case=False)
    )
    fig.add_trace(
        go.Scattergeo(
            lon=merged["lon"], lat=merged["lat"],
            text=merged["label_short"],
            mode="text",
            textfont=dict(size=10, color="black"),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    # Tampilkan peta
    st.plotly_chart(fig, use_container_width=True)

    # ===== 4) Ringkasan jumlah kab/kota per cluster (centered, flex) =====
    counts = merged["Cluster_label"].value_counts().reindex(legend_order, fill_value=0)

    badge_color = {
        "Perlu Diperhatikan": "#d00000",
        "Warning": "#f1c40f",
        "Cukup": "#74c69d",
        "Baik": "#2d6a4f",
        "Lainnya": "#bdbdbd",
    }

    # CSS + HTML (render sekali, anti code-block)
    st.markdown(dedent("""
    <style>
    .cluster-metrics{display:flex;justify-content:center;align-items:flex-start;flex-wrap:wrap;gap:48px;margin:12px 0 2px 0;}
    .metric-card{text-align:center;min-width:120px;}
    .metric-badge{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;transform:translateY(-1px);}
    .metric-title{font-weight:600;margin:0 0 6px 0;}
    .metric-value{font-size:26px;font-weight:700;margin:0;}
    </style>
    """), unsafe_allow_html=True)

    items_html = ""
    for name in legend_order:
        value = int(counts.get(name, 0))
        color = badge_color.get(name, "#bdbdbd")
        items_html += (
            f'<div class="metric-card">'
            f'  <div class="metric-title"><span class="metric-badge" style="background:{color};"></span>{name}</div>'
            f'  <div class="metric-value">{value}</div>'
            f'</div>'
        )

    st.markdown(f'<div class="cluster-metrics">{items_html}</div>', unsafe_allow_html=True)

































# =================== PURE STREAMLIT FOOTER (robust) ===================

def _safe_page_link(path: str, label: str, icon: str = ""):
    """Render st.page_link jika file ada; kalau tidak, tampilkan placeholder."""
    p = pathlib.Path(path)
    if p.is_file():
        st.page_link(path, label=label, icon=icon)
    else:
        st.write(f"_{label} (coming soon)_")
        # Debug opsional:
        # st.caption(f"Missing: {p.resolve()}")

def render_footer():
    st.divider()

    col1, col2, col3, col4 = st.columns([1.4, 1, 1, 1])

    # Brand & deskripsi
    with col1:
        st.image("icon/Only LOGO.png", width=100)
        st.markdown("**NutriHealth AI**")
        st.caption(
            "Insight KIA & kapasitas RS berbasis EDA dan hasil forecast (ETS/SARIMA). "
            "Fokus: BOR, TOI, HI, BTO, IdleShare, AVLOS, GDR/NDR, AKI/AKB, BBLR, ASI."
        )

    # Navigasi (multipage)
    with col2:
        st.markdown("**Navigasi**")
        _safe_page_link("1_🏠_Home.py", label="Home", icon="🏠")  # entrypoint
        _safe_page_link("pages/2_🤖_JAWIR.py", label="JAWIR Chatbot", icon="🤖")
        _safe_page_link("pages/3_📖_Panduan Dashboard.py", label="Panduan Dashboard", icon="📘")

    # Sumber Data & Informasi
    with col3:
        st.markdown("**Sumber Data & Informasi**")
        st.write("[Open Data Jatim](https://opendata.jatimprov.go.id/)")
        st.write("[Data Dictionary](https://drive.google.com/file/d/1WbAJ3dJS5oXP0HaBThRMwUxTfOfs_Hmf/view?usp=sharing)")

    # Kontak
    with col4:
        st.markdown("**Kontak**")
        st.write("[halo@nutrihealth.ai](mailto:rendikarendi96@gmail.com)")
        st.write("Surabaya, Jawa Timur, Indonesia")

    # ===== Legal kecil (CENTER) =====
    year = datetime.datetime.now().year
    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 6px;">
            <span style="opacity:0.8; font-size:0.9rem;">
                © {year} <strong>NutriHealth AI</strong> • Data: 
                <a href="https://opendata.jatimprov.go.id/" target="_blank" style="color:inherit; text-decoration:underline;">
                    opendata.jatimprov.go.id
                </a> • Untuk tujuan analitik & edukasi.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# panggil di paling bawah halaman
render_footer()

# ======================================================================
