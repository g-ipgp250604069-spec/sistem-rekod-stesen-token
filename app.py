import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Rekod Bilangan Token & Wristband",
    page_icon="🎟️",
    layout="wide"
)

# Inisialisasi Session State
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

# Fungsi Padam Rekod Terakhir (Undo)
def undo_last_entry():
    if len(st.session_state.sales_log) > 0:
        last_entry = st.session_state.sales_log.pop()
        item_type = last_entry["Item"]
        quantity = last_entry["Kuantiti"]
        
        if item_type == "Token":
            st.session_state.token_count -= quantity
        elif item_type == "Wristband":
            st.session_state.wristband_count -= quantity
            
        st.toast(f"⚠️ Rekod terakhir dipadam: {quantity} {item_type}")
    else:
        st.warning("Tiada rekod untuk dipadam.")

# Styling CSS untuk Warna Butang Berperingkat (Token Gradient & Butang Padam)
st.markdown("""
<style>
    /* Styling untuk Butang Token: Pudar ke Terang berdasarkan kuantiti */
    div.stButton > button[kind="secondary"]:nth-of-type(1) {
        background-color: #e8f4fd;
        color: #0b5ed7;
        border-color: #b6effb;
    }
    div.stButton > button[kind="secondary"]:nth-of-type(2) {
        background-color: #cfe2ff;
        color: #084298;
        border-color: #9ec5fe;
    }
    /* Warna Am untuk butang biasa */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Tajuk Utama
st.title("🎟️ Kaunter Rekod Token & Wristband STEM")
st.caption("Tekan butang di bawah untuk merekod atau gunakan fungsi Undo jika berlaku kesilapan.")

st.markdown("---")

# --------------------------
# PANEL REKOD BILANGAN
# --------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🪙 Panel Token")
    st.caption("Skala warna: Semakin banyak kuantiti, semakin terang tona warna.")
    
    # Butang Tekan Cepat Token (Dari pudar ke terang)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("+1 Token", use_container_width=True):
            add_entry("Token", 1)
            st.toast("✅ +1 Token")
    with c2:
        if st.button("+3 Token", use_container_width=True):
            add_entry("Token", 3)
            st.toast("✅ +3 Token")
    with c3:
        if st.button("+6 Token", use_container_width=True, type="primary"):
            add_entry("Token", 6)
            st.toast("✅ +6 Token")

with col2:
    st.subheader("🏷️ Panel Wristband (Pass Percuma)")
    st.caption("Kategori pas lawatan semua stesen.")
    
    # Butang Tekan Cepat Wristband
    w1, w2, w3 = st.columns(3)
    with w1:
        if st.button("+1 Wristband", use_container_width=True):
            add_entry("Wristband", 1)
            st.toast("✅ +1 Wristband")
    with w2:
        if st.button("+2 Wristband", use_container_width=True):
            add_entry("Wristband", 2)
            st.toast("✅ +2 Wristband")
    with w3:
        if st.button("+5 Wristband", use_container_width=True, type="primary"):
            add_entry("Wristband", 5)
            st.toast("✅ +5 Wristband")

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
# KAWALAN & JADUAL LOG
# --------------------------
col_action1, col_action2 = st.columns([1, 3])

with col_action1:
    # Butang Undo untuk batalkan rekod terakhir
    if st.button("↩️ Undo Rekod Terakhir", use_container_width=True, type="secondary"):
        undo_last_entry()
        st.rerun()

st.subheader("📋 Log Rekod Pembelian")

if len(st.session_state.sales_log) > 0:
    df = pd.DataFrame(st.session_state.sales_log)
    
    # Paparkan jadual dari rekod paling terkini
    st.dataframe(df.iloc[::-1], use_container_width=True)
    
    # Muat Turun CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Muat Turun Data (CSV)",
        data=csv_data,
        file_name=f"rekod_bilangan_stem_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )
else:
    st.info("Belum ada sebarang rekod kemasukan.")

# Butang Reset Data Penuh di bahagian bawah
st.markdown("---")
if st.button("🗑️ Reset Semua Data (Padam Habis)", type="secondary"):
    st.session_state.sales_log = []
    st.session_state.token_count = 0
    st.session_state.wristband_count = 0
    st.rerun()
