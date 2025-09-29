import streamlit as st
import joblib
import pandas as pd

# --- Konfigurasi Halaman ---
# Konfigurasi ini dipanggil sekali di awal
st.set_page_config(
    page_title="NFT Price Predictor",
    page_icon="💎",
    layout="centered"
)

# --- LANGKAH 1: BUAT KAMUS UNTUK SEMUA TEKS ---
# Di sini kita menyimpan semua teks untuk kedua bahasa
LANGUAGES = {
    "English 🇬🇧": {
        "title": "💎 Predictive Model for NFT Market Trends",
        "description": """
        This application demonstrates a simple Machine Learning model to predict NFT prices.
        The model is trained using historical sales data and utilizes Moving Average features (7-day and 30-day) to make predictions.
        """,
        "header": "Enter Data for Prediction",
        "ma7_label": "Enter the Last 7-Day Moving Average (MA7)",
        "ma30_label": "Enter the Last 30-Day Moving Average (MA30)",
        "button_text": "Predict NFT Price",
        "success_message": "The Predicted NFT Price is: ${:,.2f}",
        "disclaimer": "Disclaimer: This is a demonstration project and should not be used as financial advice."
    },
    "Indonesia 🇮🇩": {
        "title": "💎 Predictive Model for NFT Market Trends",
        "description": """
        Aplikasi ini mendemonstrasikan model Machine Learning sederhana untuk memprediksi harga NFT.
        Model ini dilatih menggunakan data historis penjualan dan menggunakan fitur Moving Average (7 hari dan 30 hari) untuk membuat prediksi.
        """,
        "header": "Masukkan Data untuk Prediksi",
        "ma7_label": "Masukkan Nilai Moving Average 7-Hari Terakhir (MA7)",
        "ma30_label": "Masukkan Nilai Moving Average 30-Hari Terakhir (MA30)",
        "button_text": "Prediksi Harga NFT",
        "success_message": "Prediksi Harga NFT adalah: Rp {:,.2f}", # Diubah ke format Rupiah
        "disclaimer": "Disclaimer: Ini adalah proyek demonstrasi dan tidak boleh digunakan sebagai saran finansial."
    }
}

# --- Fungsi untuk Memuat Model ---
# Menggunakan cache agar model tidak di-load ulang setiap kali ada interaksi
@st.cache_resource
def load_model():
    model = joblib.load('nft_price_predictor.pkl')
    return model

# Muat model di awal
model = load_model()


# --- LANGKAH 2: BUAT PEMILIH BAHASA DI SIDEBAR ---
st.sidebar.header("Settings")
selected_lang_key = st.sidebar.radio(
    'Language / Bahasa',
    options=LANGUAGES.keys() # Menggunakan kunci kamus sebagai pilihan
)

# Ambil kamus teks yang sesuai dengan bahasa yang dipilih
lang_texts = LANGUAGES[selected_lang_key]


# --- LANGKAH 3: GUNAKAN TEKS DARI KAMUS DI APLIKASI UTAMA ---
# Semua teks sekarang diambil dari variabel 'lang_texts'

st.title(lang_texts["title"])
st.write(lang_texts["description"])
st.header(lang_texts["header"])

# Buat input dari pengguna
ma7_input = st.number_input(
    label=lang_texts["ma7_label"],
    min_value=0.0,
    step=100.0,
    format="%.2f"
)

ma30_input = st.number_input(
    label=lang_texts["ma30_label"],
    min_value=0.0,
    step=100.0,
    format="%.2f"
)

# Tombol untuk prediksi
if st.button(lang_texts["button_text"]):
    # Buat dataframe dari input
    input_data = pd.DataFrame({
        'MA7': [ma7_input],
        'MA30': [ma30_input]
    })
    
    # Lakukan prediksi
    prediction = model.predict(input_data)
    
    # Tampilkan hasil
    # Untuk Rupiah, kita asumsikan 1 USD = 15,000 IDR (bisa disesuaikan)
    if selected_lang_key == "Indonesia 🇮🇩":
        prediction_value = prediction[0] * 15000
    else:
        prediction_value = prediction[0]

    st.success(lang_texts["success_message"].format(prediction_value))

st.info(lang_texts["disclaimer"])