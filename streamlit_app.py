import streamlit as st

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Lab Virtual - Sign In", page_icon="🧪", layout="centered")

# --- SIMULASI DATABASE USER (Bisa diganti sesuai keinginan) ---
USER_VALID = "admin_lab"
PASSWORD_VALID = "kimia2026"

# 2. Inisialisasi Session State untuk Status Login
if "login_sukses" not in st.session_state:
    st.session_state["login_sukses"] = False

# --- HALAMAN 1: FORM LOGIN ---
if not st.session_state["login_sukses"]:
    st.markdown("<h2 style='text-align: center; color: #0284C7;'>🔐 LOGIN SISTEM LABORATORIUM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Silakan masukkan kredensial analis Anda untuk mengakses rak reagen.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Kotak Form Login
    with st.form("form_login"):
        username = st.text_input("Username Analis", placeholder="Masukkan username...")
        password = st.text_input("Password", type="password", placeholder="Masukkan password...")
        tombol_login = st.form_submit_button("Masuk ke Laboratorium")
        
        if tombol_login:
            if username == USER_VALID and password == PASSWORD_VALID:
                st.session_state["login_sukses"] = True
                st.success("🔑 Login berhasil! Membuka gerbang lab...")
                st.rerun() # Refresh halaman untuk masuk ke lab
            else:
                st.error("❌ Username atau Password salah! Silakan periksa kembali.")

# --- HALAMAN 2: APLIKASI UTAMA (Jika Sudah Login) ---
else:
    # Tombol Logout di pojok kanan atas / sidebar
    with st.sidebar:
        st.markdown("### 👤 Profil Analis")
        st.write(f"Selamat Datang, *{USER_VALID}*")
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)"):
            st.session_state["login_sukses"] = False
            st.rerun()

    # Konten Utama Rak Reagen Virtual
    st.markdown("<h2 style='text-align: center; color: #0284C7; font-family: sans-serif;'>🧪 RAK REAGEN VIRTUAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Nyalakan sakelar reagen di bawah untuk menguji sampel misterius Anda!</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🎛️ Panel Sakelar Reagen (On / Off)")
    col_reg1, col_reg2, col_reg3 = st.columns(3)

    with col_reg1:
        st.markdown("*Uji Lakmus*")
        sakelar_lakmus = st.toggle("Celup Lakmus Biru")

    with col_reg2:
        st.markdown("*Uji Schiff*")
        sakelar_schiff = st.toggle("Tetes Reagen Schiff")

    with col_reg3:
        st.markdown("*Uji Bisulfit*")
        sakelar_bisulfit = st.toggle("Tambah NaHSO3")

    st.markdown("---")
    st.markdown("### 🔍 Kondisi Fisik Tabung Reaksi")

    sakelar_aktif = sum([sakelar_lakmus, sakelar_schiff, sakelar_bisulfit])

    if sakelar_aktif > 1:
        st.warning("⚠️ *Kontaminasi Reagen!* Harap hanya menyalakan satu sakelar reagen saja untuk menjaga akurasi analisis sampel.")

    elif sakelar_lakmus:
        st.markdown("""
            <div style='background-color: #FEE2E2; border-left: 8px solid #EF4444; padding: 20px; border-radius: 8px;'>
                <h3 style='color: #991B1B; margin: 0;'>🔴 Tabung Bereaksi: WARNA MERAH</h3>
                <p style='color: #7F1D1D; margin-top: 10px; font-size: 16px;'>
                    <b>Analisis Detektor:</b> Kertas lakmus biru langsung berubah menjadi merah! <br>
                    🎯 Fix, sampel ini adalah golongan <b>ASAM KARBOKSILAT (—COOH)</b> karena memiliki ion H+ bebas.
                </p>
            </div>
        """, unsafe_allow_html=True)

    elif sakelar_schiff:
        st.markdown("""
            <div style='background-color: #FAE8FF; border-left: 8px solid #D946EF; padding: 20px; border-radius: 8px;'>
                <h3 style='color: #86198F; margin: 0;'>🟣 Tabung Bereaksi: WARNA UNGU KEMERAHAN</h3>
                <p style='color: #701A75; margin-top: 10px; font-size: 16px;'>
                    <b>Analisis Detektor:</b> Reagen Schiff kembali ke warna asalnya akibat gugus karbonil bebas.<br>
                    🎯 Fix, sampel ini adalah golongan <b>ALDEHID / ALKANAL (—CHO)</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    elif sakelar_bisulfit:
        st.markdown("""
            <div style='background-color: #F8FAFC; border-left: 8px solid #64748B; padding: 20px; border-radius: 8px; border: 1px solid #CBD5E1;'>
                <h3 style='color: #334155; margin: 0;'>⚪ Tabung Bereaksi: TERBENTUK KRISTAL PUTIH</h3>
                <p style='color: #1E293B; margin-top: 10px; font-size: 16px;'>
                    <b>Analisis Detektor:</b> Terjadi reaksi adisi nukleofilik yang menghasilkan garam sukar larut.<br>
                    🎯 Fix, sampel ini adalah golongan <b>KETON / ALKANON (—CO—)</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div style='background-color: #FFFFFF; border-left: 8px solid #0EA5E9; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);'>
                <h3 style='color: #075985; margin: 0;'>💧 Tabung Saat Ini: BENING & JERNIH</h3>
                <p style='color: #0C4A6E; margin-top: 10px;'>
                    Belum ada reagen yang dimasukkan ke dalam sampel. Silakan klik/nyalakan salah satu <b>sakelar toggle</b> di atas untuk memulai reaksi kimia virtual!
                </p>
            </div>
        """, unsafe_allow_html=True)
