import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Rekod Bilangan Token & Wristband",
    page_icon="🎟️",
    layout="wide"
)

# Inisialisasi Session State (Simpan Rekod Bilangan)
if "sales_log" not in st.session_state:
    st.session_state.sales_log = []

if "token_count" not in st.session_state:
    st.session_state.token_count = 0

if "wristband_count" not in st.session_state:
    st.session_state.wristband_count = 0

# Fungsi Tambah Rekod
def add_entry(item_type, quantity=1):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.session_state.sales_log.append({
        "Masa": timestamp,
        "Item": item_type,
        "Kuantiti": quantity
    })
    
    if item_type == "Token":
        st.session_state.token_count += quantity
    elif item_type == "Wristband":
        st.session_state.wristband_count += quantity

# Tajuk Utama
st.title("🎟️ Kaunter Rekod Token & Wristband STEM")
st.caption("Tekan butang di bawah mengikut jumlah unit yang dibeli.")

st.markdown("---")

# --------------------------
# PANEL REKOD BILANGAN
# --------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🪙 Panel Token")
    
    # Butang Tekan Cepat Token
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("+1 Token", use_container_width=True, type="primary"):
            add_entry("Token", 1)
            st.toast("✅ 1 Token direkodkan!")
    with c2:
        if st.button("+3 Token", use_container_width=True):
            add_entry("Token", 3)
            st.toast("✅ 3 Token direkodkan!")
    with c3:
        if st.button("+6 Token", use_container_width=True):
            add_entry("Token", 6)
            st.toast("✅ 6 Token direkodkan!")

with col2:
    st.subheader("🏷️ Panel Wristband (Pass Percuma)")
    
    # Butang Tekan Cepat Wristband
    w1, w2, w3 = st.columns(3)
    with w1:
        if st.button("+1 Wristband", use_container_width=True, type="primary"):
            add_entry("Wristband", 1)
            st.toast("✅ 1 Wristband direkodkan!")
    with w2:
        if st.button("+2 Wristband", use_container_width=True):
            add_entry("Wristband", 2)
            st.toast("✅ 2 Wristband direkodkan!")
    with w3:
        if st.button("+5 Wristband", use_container_width=True):
            add_entry("Wristband", 5)
            st.toast("✅ 5 Wristband direkodkan!")

st.markdown("---")

# --------------------------
# RINGKASAN BILANGAN TERKUMPUL
# --------------------------
st.subheader("📊 Ringkasan Jumlah Unit Terjual")

m1, m2, m3 = st.columns(3)
m1.metric(label="Jumlah Token", value=f"{st.session_state.token_count} unit")
m2.metric(label="Jumlah Wristband", value=f"{st.session_state.wristband_count} unit")
m3.metric(label="Jumlah Keseluruhan (Item)", value=f"{st.session_state.token_count + st.session_state.wristband_count} unit")

st.markdown("---")

# --------------------------
# JADUAL TRANSAKSI & RESET
# --------------------------
st.subheader("📋 Log Rekod Pembelian")

if len(st.session_state.sales_log) > 0:
    df = pd.DataFrame(st.session_state.sales_log)
    
    # Paparkan jadual dari rekod paling terkini
    st.dataframe(df.iloc[::-1], use_container_width=True)
    
    # Butang Muat Turun CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Muat Turun Data (CSV)",
        data=csv_data,
        file_name=f"rekod_bilangan_stem_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )
else:
    st.info("Belum ada sebarang rekod kemasukan.")

# Butang Reset Data di bahagian bawah
st.markdown("---")
if st.button("🗑️ Reset Bilangan (Padam Semua Data)", type="secondary"):
    st.session_state.sales_log = []
    st.session_state.token_count = 0
    st.session_state.wristband_count = 0
    st.rerun()
