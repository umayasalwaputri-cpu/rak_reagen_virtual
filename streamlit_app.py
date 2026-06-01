import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Lab Virtual Analitik", page_icon="🧪", layout="wide")

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
    
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        with st.form("form_login"):
            username = st.text_input("Username Analis", placeholder="Masukkan username...")
            password = st.text_input("Password", type="password", placeholder="Masukkan password...")
            tombol_login = st.form_submit_button("Masuk ke Laboratorium")
            
            if tombol_login:
                if username == USER_VALID and password == PASSWORD_VALID:
                    # TENTUKAN STATUS LOGIN DULU
                    st.session_state["login_sukses"] = True
                    
                    # 💥 TEMBAKKAN PETASAN DI SINI
                    st.balloons()
                    
                    # LANGSUNG RE-RUN AGAR MASUK KE HALAMAN UTAMA BERSAMA PETASANNYA
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
        
        st.markdown("### 🗺️ Menu Navigasi")
        pilihan_halaman = st.radio(
            "Pilih Halaman Kerja:",
            ["🏠 Beranda Lab", "⚡ Identifikasi Ion", "🧪 Rak Reagen Organik", "📋 Logbook Pengujian"]
        )
        
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)"):
            st.session_state["login_sukses"] = False
            st.rerun()

    # --- KONTEN HALAMAN UTAMA (SISI KANAN) ---
    
    # ================= KONDISI A: BERANDA LAB =================
    if pilihan_halaman == "🏠 Beranda Lab":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>👋 SELAMAT DATANG DI ASISTEN LAB ANALITIK</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Sistem Informasi Manajemen Reagen & Instrumentasi Virtual</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Kotak Quotes Motivasi
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
                    Selamat datang di platform asisten laboratorium virtual. Web ini sekarang dilengkapi dengan dua modul utama: 
                    <b>Identifikasi Kation/Anion Anorganik</b> dan <b>Uji Gugus Fungsi Organik</b>. Silakan tentukan target belajar Anda di bawah sebelum memulai praktikum virtual!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Menu Identifikasi Target Belajar
        st.markdown("### 🎯 Identifikasi Target Belajar Praktikum")
        st.markdown("Pilih fokus kompetensi analisis yang ingin Anda kuasai pada sesi praktikum virtual hari ini:")
        
        opsi_target = [
            "Memahami Sistem Pemisahan Kation Golongan I-V",
            "Mempelajari Reaksi Identifikasi Anion Spesifik (Sulfat, Halida, Nitrat)",
            "Menguasai Karakteristik Warna Uji Nyala Api Logam Alkali/Alkali Tanah",
            "Memahami Reaksi Identifikasi Senyawa Organik (Karbonil & Karboksilat)"
        ]
        
        with st.form("form_target"):
            pilihan_target = st.selectbox("Pilih Fokus Belajar Anda:", opsi_target)
            tombol_target = st.form_submit_button("🔒 Kunci & Simpan Target Belajar")
            
            if tombol_target:
                st.session_state["target_belajar"] = pilihan_target
                st.success(f"🎯 Target berhasil dikunci! Hari ini Anda berfokus pada: *{pilihan_target}*")
                st.toast("Target belajar diperbarui!", icon="🎯")
                st.rerun()

    # ================= KONDISI B: IDENTIFIKASI ION ANORGANIK =================
    elif pilihan_halaman == "⚡ Identifikasi Ion":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>⚡ SISTEM IDENTIFIKASI KATION & ANION</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #64748B;'>Fokus Target Sesi Ini: <b>{st.session_state['target_belajar']}</b></p>", unsafe_allow_html=True)
        st.markdown("---")

        with st.expander("📚 Klik di sini untuk membaca Materi & Skema Dasar"):
            st.markdown("""
            ### Dasar Teori Pemisahan Kation
            Analisis kualitatif kation didasarkan pada perbedaan kelarutan garam-garamnya. 
            Secara umum, kation dipisahkan menjadi 5 golongan berdasarkan reagen selektif:
            * *Golongan I:* Mengendap dengan HCl encer ($Ag^+$, $Pb^{2+}$, $Hg_2^{2+}$).
            * *Golongan II:* Mengendap dengan $H_2S$ dalam suasana asam.
            * *Golongan III:* Mengendap dengan $H_2S$ dalam suasana basa / amoniakal.
            * *Golongan IV:* Mengendap dengan $(NH_4)_2CO_3$ ($Ba^{2+}$, $Sr^{2+}$, $Ca^{2+}$).
            * *Golongan V:* Sisa kation yang tidak mengendap ($Mg^{2+}$, $Na^+$, $K^+$).
            """)
            st.info("💡 Tips Lab: Selalu cuci endapan dengan akuades sebelum menambahkan reagen tahap berikutnya agar tidak ada kontaminasi ion dari golongan sebelumnya.")

        jenis_analisis = st.selectbox(
            "Pilih Metode Analisis:",
            ["Skema Pemisahan Kation Gol. I-V", "Uji Anion (Non-Logam)", "Uji Nyala Api (Flame Test)"],
            index=None,
            placeholder="Pilih metode pengujian ion..."
        )
        st.divider()

        nama_reagen = "-"
        kesimpulan_gugus = "-"

        # 1. SKEMA KATION
        if jenis_analisis == "Skema Pemisahan Kation Gol. I-V":
            st.subheader("Pemisahan Kation Golongan I-V")
            st.write("Berdasarkan Skema: $Ag^+$, $Pb^{2+}$, $Hg_2^{2+}$, $Al^{3+}$, $Fe^{3+}$, $Ba^{2+}$, $Sr^{2+}$, $Ca^{2+}$")
            st.write("*Tahap 1: Penambahan HCl encer*")
            
            tahap_1 = st.radio(
                "Pilih jalur berdasarkan hasil reaksi dengan HCl encer:",
                ["Terbentuk Endapan (AgCl, PbCl2, Hg2Cl2)", "Berupa Filtrat (Al3+, Fe3+, Ba2+, Sr2+, Ca2+)"],
                index=None
            )

            if tahap_1 == "Terbentuk Endapan (AgCl, PbCl2, Hg2Cl2)":
                st.info("🧪 Fokus pada Endapan: Tambahkan $H_2O$ (cuci) lalu panaskan dengan $H_2O$.")
                tahap_2_gol1 = st.radio("Apa yang terjadi pada endapan setelah dipanaskan?", 
                    ["Endapan Larut (Pb2+)", "Endapan Tidak Larut (AgCl, Hg2Cl2)"], index=None)
                
                if tahap_2_gol1 == "Endapan Larut (Pb2+)":
                    st.write("➡️ Tambahkan $K_2CrO_4$")
                    st.success("✨ Terbentuk endapan $PbCrO_4$ kuning. Kation: *Timbal ($Pb^{2+}$)*")
                    nama_reagen, kesimpulan_gugus = "HCl -> Pemanasan -> K2CrO4", "Kation Timbal (Pb²⁺)"
                    
                elif tahap_2_gol1 == "Endapan Tidak Larut (AgCl, Hg2Cl2)":
                    st.write("➡️ Tambahkan $NH_4OH$ berlebih (>>)")
                    tahap_3_gol1 = st.radio("Apa hasil penambahan amonia?", 
                        ["Endapan Putih Hg(NH2)Cl + Hitam Hg", "Menjadi Larutan (Ag(NH3)2+ Cl-)"], index=None)
                    
                    if tahap_3_gol1 == "Endapan Putih Hg(NH2)Cl + Hitam Hg":
                        st.success("✨ Kation: *Merkurium(I) ($Hg_2^{2+}$)*")
                        nama_reagen, kesimpulan_gugus = "HCl -> NH4OH (>>)", "Kation Merkurium(I) (Hg₂²⁺)"
                    elif tahap_3_gol1 == "Menjadi Larutan (Ag(NH3)2+ Cl-)":
                        st.write("➡️ Tambahkan $HNO_3$")
                        st.success("✨ Terbentuk endapan $AgCl$ putih. Kation: *Perak ($Ag^+$)*")
                        nama_reagen, kesimpulan_gugus = "HCl -> NH4OH -> HNO3", "Kation Perak (Ag⁺)"

            elif tahap_1 == "Berupa Filtrat (Al3+, Fe3+, Ba2+, Sr2+, Ca2+)":
                st.info("🧪 Fokus pada Filtrat: Tambahkan $NH_4OH$ berlebih (>>).")
                tahap_2_filtrat = st.radio("Apa yang terbentuk?", 
                    ["Terbentuk Endapan (Al(OH)3, Fe(OH)3)", "Berupa Filtrat (Ba2+, Sr2+, Ca2+)"], index=None)
                
                if tahap_2_filtrat == "Terbentuk Endapan (Al(OH)3, Fe(OH)3)":
                    st.write("➡️ Tambahkan $NaOH$")
                    tahap_3_gol3 = st.radio("Apa hasil penambahan NaOH?", 
                        ["Endapan Fe(OH)3 (Tidak larut)", "Larutan Al(OH)4- (Larut)"], index=None)
                    
                    if tahap_3_gol3 == "Endapan Fe(OH)3 (Tidak larut)":
                        st.write("➡️ Tambahkan $HNO_3$ (menjadi $Fe^{3+}$), lalu tambahkan $SCN^-$")
                        st.success("✨ Terbentuk kompleks $Fe(SCN)_3$ merah. Kation: *Besi(III) ($Fe^{3+}$)*")
                        nama_reagen, kesimpulan_gugus = "HCl Filtrat -> NH4OH -> NaOH -> HNO3 + SCN-", "Kation Besi(III) (Fe³⁺)"
                    elif tahap_3_gol3 == "Larutan Al(OH)4- (Larut)":
                        st.write("➡️ Tambahkan $HCl$ lalu $Na_2CO_3$")
                        st.success("✨ Terbentuk endapan $Al(OH)_3$ putih. Kation: *Aluminium ($Al^{3+}$)*")
                        nama_reagen, kesimpulan_gugus = "HCl Filtrat -> NH4OH -> NaOH -> HCl + Na2CO3", "Kation Aluminium (Al³⁺)"
                        
                elif tahap_2_filtrat == "Berupa Filtrat (Ba2+, Sr2+, Ca2+)":
                    st.write("➡️ Tambahkan $K_2CrO_4$")
                    tahap_3_gol4 = st.radio("Apa hasilnya?", 
                        ["Terbentuk Endapan (BaCrO4, SrCrO4)", "Berupa Filtrat (Ca2+)"], index=None)
                    
                    if tahap_3_gol4 == "Terbentuk Endapan (BaCrO4, SrCrO4)":
                        st.write("➡️ Tambahkan $CH_3COOH$")
                        tahap_4_gol4 = st.radio("Hasil penambahan asam asetat:", 
                            ["Endapan BaCrO4 Kuning", "Larutan Sr2+"], index=None)
                        
                        if tahap_4_gol4 == "Endapan BaCrO4 Kuning":
                            st.success("✨ Kation: *Barium ($Ba^{2+}$)*")
                            nama_reagen, kesBuffer = "Filtrat -> K2CrO4 -> CH3COOH", "Kation Barium (Ba²⁺)"
                        elif tahap_4_gol4 == "Larutan Sr2+":
                            st.write("➡️ Tambahkan $Na_2CO_3$")
                            st.success("✨ Terbentuk endapan $SrCO_3$ putih. Kation: *Stronsium ($Sr^{2+}$)*")
                            nama_reagen, kesimpulan_gugus = "Filtrat -> K2CrO4 -> CH3COOH -> Na2CO3", "Kation Stronsium (Sr²⁺)"
                            
                    elif tahap_3_gol4 == "Berupa Filtrat (Ca2+)":
                        st.write("➡️ Tambahkan $H_2C_2O_4$ dan $NH_4OH$")
                        st.success("✨ Terbentuk endapan $CaC_2O_4$ putih. Kation: *Kalsium ($Ca^{2+}$)*")
                        nama_reagen, kesimpulan_gugus = "Filtrat -> K2CrO4 Filtrat -> H2C2O4 + NH4OH", "Kation Kalsium (Ca²⁺)"

        # 2. UJI ANION
        elif jenis_analisis == "Uji Anion (Non-Logam)":
            st.subheader("Uji Identifikasi Anion Spesifik")
            reagen_anion = st.selectbox("Pilih reagen yang ditambahkan ke sampel:", [
                "BaCl2 (Barium Klorida)",
                "AgNO3 (Perak Nitrat)",
                "FeSO4 + H2SO4 pekat (Uji Cincin Cokelat)"
            ], index=None)

            if reagen_anion == "BaCl2 (Barium Klorida)":
                st.write("Hasil: Terbentuk endapan putih yang *tidak larut* dalam HCl encer.")
                st.success("✨ Anion Teridentifikasi: *Sulfat ($SO_4^{2-}$)*")
                nama_reagen, kesimpulan_gugus = "BaCl2 + HCl", "Anion Sulfat (SO₄²⁻)"
            elif reagen_anion == "AgNO3 (Perak Nitrat)":
                hasil_agno3 = st.radio("Warna endapan yang terbentuk:", ["Putih", "Kuning Pucat", "Kuning Terang"], index=None)
                if hasil_agno3 == "Putih":
                    st.success("✨ Anion Teridentifikasi: *Klorida ($Cl^-$)*")
                    nama_reagen, kesimpulan_gugus = "AgNO3", "Anion Klorida (Cl⁻)"
                elif hasil_agno3 == "Kuning Pucat":
                    st.success("✨ Anion Teridentifikasi: *Bromida ($Br^-$)*")
                    nama_reagen, kesimpulan_gugus = "AgNO3", "Anion Bromida (Br⁻)"
                elif hasil_agno3 == "Kuning Terang":
                    st.success("✨ Anion Teridentifikasi: *Iodida ($I^-$)*")
                    nama_reagen, kesimpulan_gugus = "AgNO3", "Anion Iodida (I⁻)"
            elif reagen_anion == "FeSO4 + H2SO4 pekat (Uji Cincin Cokelat)":
                st.write("Hasil: Terbentuk cincin berwarna cokelat di antara dua lapisan cairan.")
                st.success("✨ Anion Teridentifikasi: *Nitrat ($NO_3^-$)*")
                nama_reagen, kesimpulan_gugus = "FeSO4 + H2SO4 pekat", "Anion Nitrat (NO₃⁻)"

        # 3. UJI NYALA API
        elif jenis_analisis == "Uji Nyala Api (Flame Test)":
            st.subheader("Uji Nyala Logam Alkali & Alkali Tanah")
            warna_nyala = st.selectbox("Pilih warna nyala api yang terlihat:", [
                "Kuning keemasan intens",
                "Merah bata / Merah jingga",
                "Hijau kekuningan / Hijau apel",
                "Merah tua (Crimson)",
                "Ungu / Lilac"
            ], index=None)

            if warna_nyala == "Kuning keemasan intens":
                st.success("✨ Logam Teridentifikasi: *Natrium ($Na^+$)*")
                nama_reagen, kesimpulan_gugus = "Flame Test", "Logam Natrium (Na⁺)"
            elif warna_nyala == "Merah bata / Merah jingga":
                st.success("✨ Logam Teridentifikasi: *Kalsium ($Ca^{2+}$)*")
                nama_reagen, kesimpulan_gugus = "Flame Test", "Logam Kalsium (Ca²⁺)"
            elif warna_nyala == "Hijau kekuningan / Hijau apel":
                st.success("✨ Logam Teridentifikasi: *Barium ($Ba^{2+}$)*")
                nama_reagen, kesimpulan_gugus = "Flame Test", "Logam Barium (Ba²⁺)"
            elif warna_nyala == "Merah tua (Crimson)":
                st.success("✨ Logam Teridentifikasi: *Stronsium ($Sr^{2+}$)* atau *Litium ($Li^+$)*")
                nama_reagen, kesimpulan_gugus = "Flame Test", "Logam Stronsium/Litium"
            elif warna_nyala == "Ungu / Lilac":
                st.success("✨ Logam Teridentifikasi: *Kalium ($K^+$)*")
                nama_reagen, kesimpulan_gugus = "Flame Test", "Logam Kalium (K⁺)"

        # 💥 TRIGGER PETASAN & APRESIASI (ANORGANIK)
        if kesimpulan_gugus != "-":
            st.markdown("---")
            if st.button("💾 Catat Hasil Uji Anorganik ke Logbook"):
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["logbook_data"].append({
                    "Waktu Analisis": waktu_sekarang,
                    "Target Belajar": st.session_state["target_belajar"],
                    "Reagen Digunakan": nama_reagen,
                    "Hasil Identifikasi": kesimpulan_gugus
                })
                # Memunculkan Efek Petasan (Balloons)
                st.balloons()
                st.success("🎉 *Yey kamu berhasil!* Kompetensi praktikum tercapai dan data terekam di Logbook digital.")
                st.toast("Data terekam!", icon="📝")

    # ================= KONDISI C: RAK REAGEN ORGANIK =================
    elif pilihan_halaman == "🧪 Rak Reagen Organik":
        st.markdown("<h2 style='text-align: center; color: #0284C7; font-family: sans-serif;'>🧪 RAK REAGEN VIRTUAL (ORGANIK)</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #64748B;'>Fokus Target Sesi Ini: <b>{st.session_state['target_belajar']}</b></p>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### 🎛️ Panel Sakelar Reagen Organik (On / Off)")
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

        # 💥 TRIGGER PETASAN & APRESIASI (ORGANIK)
        if sakelar_aktif == 1:
            st.markdown("---")
            if st.button("💾 Catat Hasil Uji Organik ke Logbook"):
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["logbook_data"].append({
                    "Waktu Analisis": waktu_sekarang,
                    "Target Belajar": st.session_state["target_belajar"],
                    "Reagen Digunakan": nama_reagen,
                    "Hasil Identifikasi": kesimpulan_gugus
                })
                # Memunculkan Efek Petasan (Balloons)
                st.balloons()
                st.success("🎉 *Yey kamu berhasil!* Analisis gugus fungsi tersimpan aman di Logbook.")
                st.toast("Data terekam!", icon="📝")

    # ================= KONDISI D: TAMPILAN LOGBOOK DATA =================
    elif pilihan_halaman == "📋 Logbook Pengujian":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>📋 LOGBOOK DIGITAL LABORATORIUM</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Daftar riwayat rekaman pengujian & evaluasi target belajar</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.info(f"🎯 *Fokus Kompetensi Hari Ini:* {st.session_state['target_belajar']}")
        
        if len(st.session_state["logbook_data"]) > 0:
            df_log = pd.DataFrame(st.session_state["logbook_data"])
            st.dataframe(df_log, use_container_width=True)
            
            if st.button("🗑️ Bersihkan Semua Log"):
                st.session_state["logbook_data"] = []
                st.rerun()
        else:
            st.warning("Belum ada riwayat praktikum yang tersimpan. Silakan tentukan target belajar Anda di Beranda, lalu lakukan pengujian di area menu Ion atau Organik.")
