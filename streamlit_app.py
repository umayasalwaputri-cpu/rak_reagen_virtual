import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Lab Virtual Analitik", page_icon="🧪", layout="centered")

# --- DATABASE USER ---
USER_VALID = "admin_lab"
PASSWORD_VALID = "kimia2026"

# Inisialisasi Session State untuk Status Login, Logbook, dan Target Belajar
if "login_sukses" not in st.session_state:
    st.session_state["login_sukses"] = False
if "logbook_data" not in st.session_state:
    st.session_state["logbook_data"] = []
if "target_belajar" not in st.session_state:
    st.session_state["target_belajar"] = "Belum ditentukan"

# --- HALAMAN 1: FORM LOGIN ---
if not st.session_state["login_sukses"]:
    st.markdown("<h2 style='text-align: center; color: #0284C7;'>🔐 LOGIN SISTEM LABORATORIUM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Silakan masukkan kredensial analis Anda untuk mengakses instrumen lab.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.form("form_login"):
        username = st.text_input("Username Analis", placeholder="Masukkan username...")
        password = st.text_input("Password", type="password", placeholder="Masukkan password...")
        tombol_login = st.form_submit_button("Masuk ke Laboratorium")
        
        if tombol_login:
            if username == USER_VALID and password == PASSWORD_VALID:
                st.session_state["login_sukses"] = True
                st.success("🔑 Login berhasil! Membuka gerbang lab...")
                st.rerun()
            else:
                st.error("❌ Username atau Password salah! Silakan periksa kembali.")

# --- HALAMAN 2: APLIKASI UTAMA (Jika Sudah Login) ---
else:
    # --- PENGATURAN SIDEBAR (SISI KIRI) ---
    with st.sidebar:
        st.markdown("### 👤 Profil Analis")
        st.markdown(f"Selamat Datang, *{USER_VALID}*")
        st.caption(f"🎯 Target Hari Ini: {st.session_state['target_belajar']}")
        st.markdown("---")
        
        st.markdown("### 🗺️ Menu Instrumen")
        pilihan_halaman = st.radio(
            "Pilih Halaman Kerja:",
            ["🏠 Beranda Lab", "🧪 Rak Reagen Virtual", "📋 Logbook Pengujian"]
        )
        
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)"):
            st.session_state["login_sukses"] = False
            st.rerun()

    # --- KONTEN HALAMAN UTAMA (SISI KANAN) ---
    
    # KONDISI A: BERANDA LAB + QUOTES MOTIVASI + TARGET BELAJAR
    if pilihan_halaman == "🏠 Beranda Lab":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>👋 SELAMAT DATANG DI ASISTEN LAB ANALITIK</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Sistem Informasi Manajemen Reagen & Instrumentasi Virtual</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # ✨ KOTAK QUOTES MOTIVASI KIMIA
        st.markdown("""
            <div style='background-color: #E0F2FE; border-left: 6px solid #0284C7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 25px;'>
                <p style='color: #0369A1; font-style: italic; font-size: 16px; margin: 0;'>
                    "Sama seperti reaksi kimia eksoterm yang melepaskan energi, biarlah semangat belajarmu hari ini memancar dan menginspirasi sekitar! Jangan takut salah, karena eror dan kegagalan di lab adalah fraksi murni dari proses menuju kebenaran ilmiah."
                </p>
                <p style='color: #0284C7; font-size: 12px; font-weight: bold; margin-top: 5px; margin-bottom: 0;'>🔬 Salam Analis Hebat 🔬</p>
            </div>
        """, unsafe_allow_html=True)

        # Kartu Sambutan
        st.markdown("""
            <div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 25px;'>
                <h4 style='color: #1E293B; margin: 0;'>Halo, Analis Kimia! 🧪</h4>
                <p style='color: #475569; margin-top: 8px; line-height: 1.5; font-size: 15px;'>
                    Selamat datang di platform asisten laboratorium virtual. Web ini dirancang untuk memudahkan Anda 
                    dalam melakukan simulasi pengujian kualitatif gugus fungsi secara cepat, aman, dan efisien.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 🎯 MENU IDENTIFIKASI TARGET BELAJAR
        st.markdown("### 🎯 Identifikasi Target Belajar Praktikum")
        st.markdown("Pilih fokus kompetensi analisis yang ingin Anda kuasai pada sesi praktikum virtual hari ini:")
        
        opsi_target = [
            "Memahami Reaksi Identifikasi Asam Karboksilat via Uji Lakmus Biru",
            "Memahami Reaksi Adisi Gugus Aldehid menggunakan Reagen Schiff",
            "Mengidentifikasi Senyawa Golongan Keton melalui Pembentukan Kristal Bisulfit",
            "Menguasai Seluruh Kompetensi Uji Kualitatif Senyawa Karbonil & Karboksilat"
        ]
        
        # Form input untuk memilih target belajar
        with st.form("form_target"):
            pilihan_target = st.selectbox("Pilih Fokus Belajar Anda:", opsi_target)
            tombol_target = st.form_submit_button("🔒 Kunci & Simpan Target Belajar")
            
            if tombol_target:
                st.session_state["target_belajar"] = pilihan_target
                st.success(f"🎯 Target berhasil dikunci! Hari ini Anda berfokus pada: *{pilihan_target}*")
                st.toast("Target belajar diperbarui!", icon="🎯")
                st.rerun()

    # KONDISI B: RAK REAGEN VIRTUAL
    elif pilihan_halaman == "🧪 Rak Reagen Virtual":
        st.markdown("<h2 style='text-align: center; color: #0284C7; font-family: sans-serif;'>🧪 RAK REAGEN VIRTUAL</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #64748B;'>Fokus Target: <b>{st.session_state['target_belajar']}</b></p>", unsafe_allow_html=True)
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
        
        nama_reagen = "-"
        kesimpulan_gugus = "-"

        if sakelar_aktif > 1:
            st.warning("⚠️ *Kontaminasi Reagen!* Harap hanya menyalakan satu sakelar reagen saja untuk menjaga akurasi analisis sampel.")
        elif sakelar_lakmus:
            nama_reagen = "Kertas Lakmus Biru"
            kesimpulan_gugus = "Asam Karboksilat (—COOH)"
            st.markdown("""
                <div style='background-color: #FFE2E2; border-left: 8px solid #EF4444; padding: 20px; border-radius: 8px;'>
                    <h3 style='color: #991B1B; margin: 0;'>🔴 Tabung Bereaksi: WARNA MERAH</h3>
                    <p style='color: #7F1D1D; margin-top: 10px; font-size: 16px;'>
                        <b>Analisis Detektor:</b> Kertas lakmus biru langsung berubah menjadi merah! <br>
                        🎯 Fix, sampel ini adalah golongan <b>ASAM KARBOKSILAT (—COOH)</b> karena memiliki ion H+ bebas.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        elif sakelar_schiff:
            nama_reagen = "Reagen Schiff"
            kesimpulan_gugus = "Aldehid / Alkanal (—CHO)"
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
            nama_reagen = "Natrium Bisulfit (NaHSO3)"
            kesimpulan_gugus = "Keton / Alkanon (—CO—)"
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

        # Tombol aksi untuk mencatat ke logbook digital
        if sakelar_aktif == 1:
            st.markdown("---")
            if st.button("💾 Catat Hasil Uji ke Logbook"):
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["logbook_data"].append({
                    "Waktu Analisis": waktu_sekarang,
                    "Target Belajar": st.session_state["target_belajar"],
                    "Reagen Digunakan": nama_reagen,
                    "Hasil Identifikasi": kesimpulan_gugus
                })
                st.toast("✅ Data pengujian berhasil direkam ke logbook!", icon="📝")

    # KONDISI C: TAMPILAN LOGBOOK DATA
    elif pilihan_halaman == "📋 Logbook Pengujian":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>📋 LOGBOOK DIGITAL LABORATORIUM</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Daftar riwayat rekaman pengujian & evaluasi target belajar</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.info(f"🎯 *Fokus Kompetensi Sesi Ini:* {st.session_state['target_belajar']}")
        
        if len(st.session_state["logbook_data"]) > 0:
            df_log = pd.DataFrame(st.session_state["logbook_data"])
            st.dataframe(df_log, use_container_width=True)
            
            if st.button("🗑️ Bersihkan Semua Log"):
                st.session_state["logbook_data"] = []
                st.rerun()
        else:
            st.warning("Belum ada riwayat praktikum yang tersimpan. Silakan kunci target belajar Anda di Beranda, lalu lakukan pengujian di area Rak Reagen Virtual.")
