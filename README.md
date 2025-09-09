# 🩺 NutriHealth AI Dashboard

**NutriHealth AI Dashboard** adalah platform analitik interaktif berbasis **Streamlit** untuk memantau **Kesehatan Ibu–Anak (Maternal and Child Health/MNCH)** dan **kapasitas Rumah Sakit** di Jawa Timur.  
Dashboard ini mengintegrasikan **Eksplorasi Data (EDA)**, **Statistical Forecasting (ETS, SARIMA)**, serta **Clustering berbasis wilayah** untuk memberikan insight berbasis data dalam mendukung visi *Generasi Emas 2045*.

---

## ✨ Fitur Utama

- 📊 **Exploratory Data Analysis (EDA)**
  - Boxplot, tren tahunan/bulanan, heatmap musiman OBGYN
  - Korelasi variabel numerik & kategorikal
- 🔮 **Statistical Forecasting**
  - Prediksi 18 bulan ke depan menggunakan ETS & SARIMA
  - Interval kepercayaan 95% untuk estimasi ketidakpastian
  - Ringkasan performa model (MASE, sMAPE)
- 🗺️ **Clustering Maps**
  - Peta kabupaten/kota di Jawa Timur dengan kategori cluster
  - Label: *Perlu Diperhatikan*, *Warning*, *Cukup*, *Baik*
  - Ringkasan jumlah kabupaten/kota per cluster
- ⚡ **Interaktivitas Tinggi**
  - Filter indikator, rentang waktu, toggle interval kepercayaan
  - Sidebar navigasi dan kontrol analisis
- 🎨 **UI/UX Custom**
  - Hero banner, tema warna utama `#88CD33`
  - Sub-section title dengan ikon kategori

---

## 🏗️ Arsitektur & Teknologi

- **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) + custom CSS
- **Visualisasi**: Plotly Express, Plotly Graph Objects, Seaborn, Matplotlib
- **Data Processing**: Pandas, NumPy
- **Forecasting Models**: ETS, SARIMA (via `statsmodels`)
- **Geospatial**: GeoPandas + Plotly Choropleth
- **Deployment Ready**: dapat dijalankan di lokal atau di-deploy ke [Streamlit Cloud](https://streamlit.io/cloud) / [Heroku](https://www.heroku.com/) / [Railway](https://railway.app/)

---

## 📂 Struktur Direktori

```bash
nutrihealth-ai-dashboard/
│
├── data/                  # Dataset CSV & GeoJSON
│   ├── ABT_Master.csv
│   ├── df_merged_after_forecast.csv
│   ├── forecast_results.csv
│   └── jatim_kabkota.geojson
│
├── icon/                  # Logo & assets grafis
├── source/                # Banner & media pendukung
│
├── pages/                 # Multipage Streamlit
│   ├── 2_🤖_JAWIR.py
│   └── 3_📖_Panduan Dashboard.py
│
├── 1_🏠_Home.py                # Entrypoint utama Streamlit
├── README.md              # Dokumentasi proyek
└── requirements.txt       # Dependency Python
````

---

## ⚙️ Instalasi & Menjalankan

1. **Clone repo**

   ```bash
   git clone https://github.com/username/nutrihealth-ai-dashboard.git
   cd nutrihealth-ai-dashboard
   ```

2. **Buat virtual environment & install requirements**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows

   pip install -r requirements.txt
   ```

3. **Jalankan Streamlit**

   ```bash
   streamlit run home.py
   ```

4. Buka di browser → [http://localhost:8501](http://localhost:8501)

---

## 📊 Data Sources

* [Open Data Jawa Timur](https://opendata.jatimprov.go.id/)
* Kementerian Kesehatan RI
* Dataset internal hasil preprocessing (`data/ABT_Master.csv`, dsb.)

---

## 🚀 Roadmap

* [ ] Integrasi **machine learning classifier** untuk prediksi cluster kesehatan
* [ ] Penambahan **simulasi kebijakan** (what-if analysis)
* [ ] Modul **export laporan otomatis** (PDF/Excel)
* [ ] Integrasi **user authentication** untuk dashboard multi-user

---

## 🤝 Kontribusi

Kontribusi sangat terbuka!
Silakan fork repo ini, buat branch baru (`feature/fitur-baru`), lalu ajukan pull request.
Untuk laporan bug atau saran, gunakan [Issues](../../issues).

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
Silakan gunakan, modifikasi, dan distribusikan dengan atribusi yang sesuai.

---

## 👨‍💻 Author

**Rendika Nurhartanto Suharto**

* 🎓 Data Science, Telkom University Surabaya
* 🌐 [LinkedIn](https://linkedin.com/in/rendikanurhartanto) | [GitHub](https://github.com/rendikanurhartanto)

```
