import streamlit as st
import joblib
import pandas as pd

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="NFT Floor Price Estimator",
    page_icon="💎",
    layout="centered"
)

# --- Kamus Bahasa (Tetap sama, hanya ganti beberapa teks) ---
LANGUAGES = {
    "English 🇬🇧": {
        "title": "💎 NFT Floor Price Estimator",
        "description": """
        This application uses a Machine Learning model to estimate the floor price of an NFT collection based on its current market metrics. 
        Enter the metrics below to get an estimation.
        """,
        "header": "Enter Collection Metrics",
        "volume_label": "Total Volume (USD)",
        "sales_label": "Total Number of Sales",
        "owners_label": "Number of Unique Owners",
        "avg_price_label": "Average Sale Price (USD)",
        "button_text": "Estimate Floor Price",
        "success_message": "The Estimated Floor Price is: ${:,.2f}",
        "disclaimer": "Disclaimer: This is a demonstration project based on historical data and should not be used as financial advice."
    },
    "Indonesia 🇮🇩": {
        "title": "💎 Estimator Harga Dasar NFT",
        "description": """
        Aplikasi ini menggunakan model Machine Learning untuk mengestimasi harga dasar (floor price) sebuah koleksi NFT berdasarkan metrik pasarnya saat ini.
        Masukkan metrik di bawah untuk mendapatkan estimasi.
        """,
        "header": "Masukkan Metrik Koleksi",
        "volume_label": "Total Volume (USD)",
        "sales_label": "Jumlah Penjualan",
        "owners_label": "Jumlah Pemilik Unik",
        "avg_price_label": "Harga Rata-Rata Penjualan (USD)",
        "button_text": "Estimasi Harga Dasar",
        "success_message": "Estimasi Harga Dasar adalah: ${:,.2f}",
        "disclaimer": "Disclaimer: Ini adalah proyek demonstrasi berdasarkan data historis dan tidak boleh digunakan sebagai saran finansial."
    }
}

# --- Fungsi untuk Memuat Model ---
@st.cache_resource
def load_model():
    model = joblib.load('nft_price_predictor.pkl')
    return model

model = load_model()

# --- Sidebar dan Pilihan Bahasa ---
st.sidebar.header("Settings")
selected_lang_key = st.sidebar.radio(
    'Language / Bahasa',
    options=LANGUAGES.keys()
)
lang_texts = LANGUAGES[selected_lang_key]

# --- Tampilan Aplikasi Utama (Sudah Diperbarui) ---
st.title(lang_texts["title"])
st.write(lang_texts["description"])
st.header(lang_texts["header"])

# Input baru yang sesuai dengan model
volume_input = st.number_input(label=lang_texts["volume_label"], min_value=0.0, format="%.2f")
sales_input = st.number_input(label=lang_texts["sales_label"], min_value=0, step=1)
owners_input = st.number_input(label=lang_texts["owners_label"], min_value=0, step=1)
avg_price_input = st.number_input(label=lang_texts["avg_price_label"], min_value=0.0, format="%.2f")

# Tombol Prediksi
if st.button(lang_texts["button_text"]):
    # Buat dataframe dari input dengan nama kolom yang BENAR
    input_data = pd.DataFrame({
        'Volume_USD': [volume_input],
        'Sales': [sales_input],
        'Owners': [owners_input],
        'Average_Price_USD': [avg_price_input]
    })
    
    # Lakukan prediksi
    prediction = model.predict(input_data)
    
    # Tampilkan hasil
    st.success(lang_texts["success_message"].format(prediction[0]))

st.info(lang_texts["disclaimer"])
