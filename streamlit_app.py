import streamlit as st
import pandas as pd
import random
from datetime import datetime
import base64

# 1. Konfigurasi Halaman Web Utama
st.set_page_config(page_title="Lab Virtual Analitik", page_icon="🧪", layout="wide")

# --- DATABASE USER ---
USER_VALID = "admin_lab"
PASSWORD_VALID = "kimia2026"

# ==========================================
# DATABASE 20 SOAL KUIS (10 KATION & 10 ANION)
# ==========================================
SOAL_MASTER = [
    {
        "pertanyaan": "Kation kelompok mana yang mengendap sebagai klorida jika ditambahkan asam klorida (HCl) encer?",
        "pilihan": ["Golongan I (Ag+, Pb2+, Hg2^2+)", "Golongan II (Cu2+, Cd2+, As3+)", "Golongan III (Fe3+, Al3+, Cr3+)", "Golongan IV (Ba2+, Ca2+, Sr2+)"],
        "jawaban": "Golongan I (Ag+, Pb2+, Hg2^2+)",
        "pembahasan": "Kation Golongan I adalah kation yang mengendap sebagai garam klorida yang tidak larut dalam suasana asam encer."
    },
    {
        "pertanyaan": "Jika larutan yang mengandung kation Fe^3+ ditambahkan pereaksi KSCN (Kalium Tiosianat), warna larutan akan berubah menjadi...",
        "pilihan": ["Merah darah", "Biru tua", "Hijau muda", "Kuning jernih"],
        "jawaban": "Merah darah",
        "pembahasan": "Reaksi Fe^3+ dengan SCN- membentuk kompleks [Fe(SCN)]^2+ yang berwarna merah darah yang sangat khas."
    },
    {
        "pertanyaan": "Endapan kuning terang PbI2 terbentuk ketika kation Timbal (Pb^2+) direaksikan dengan...",
        "pilihan": ["Kalium Iodida (KI)", "Natrium Hidroksida (NaOH)", "Asam Sulfat (H2SO4)", "Amonia (NH3)"],
        "jawaban": "Kalium Iodida (KI)",
        "pembahasan": "Pb^2+ bereaksi dengan ion I- menghasilkan endapan timbal(II) iodida (PbI2) yang berwarna kuning emas/terang."
    },
    {
        "pertanyaan": "Kation Cu^2+ jika ditambahkan sedikit larutan Amonia (NH3) akan membentuk endapan biru muda. Jika Amonia ditambahkan berlebih, endapan tersebut akan larut kembali membentuk larutan berwarna...",
        "pilihan": ["Biru tua/intens", "Hijau zamrud", "Ungu", "Tak berwarna"],
        "jawaban": "Biru tua/intens",
        "pembahasan": "Kelebihan amonia menyebabkan pembentukan ion kompleks tetraminatembaga(II) [Cu(NH3)4]^2+ yang larut dan berwarna biru tua."
    },
    {
        "pertanyaan": "Uji nyala (flame test) untuk kation Kalsium (Ca^2+) memberikan warna nyala yang khas, yaitu...",
        "pilihan": ["Merah bata", "Kuning", "Ungu", "Hijau"],
        "jawaban": "Merah bata",
        "pembahasan": "Ca2+ memberikan warna merah bata. Sebagai tambahan, Na+ memberikan warna kuning, K+ berwarna ungu, and Ba2+ berwarna hijau apel."
    },
    {
        "pertanyaan": "Uji spesifik untuk kation Amonium (NH4+) melibatkan pemanasan sampel dengan basa kuat (NaOH). Gas yang dilepaskan dapat diidentifikasi karena...",
        "pilihan": ["Mengubah kertas lakmus merah basah menjadi biru", "Mengubah kertas lakmus biru menjadi merah", "Membentuk endapan hitam dengan air", "Menghasilkan bau harum melati"],
        "jawaban": "Mengubah kertas lakmus merah basah menjadi biru",
        "pembahasan": "Gas amonia (NH3) yang terlepas bersifat basa, sehingga akan mengubah lakmus merah menjadi biru dan memiliki bau menyengat."
    },
    {
        "pertanyaan": "Kation Al^3+ dan Zn^2+ sama-sama membentuk endapan putih jika ditambahkan sedikit NaOH. Cara membedakannya adalah dengan menambahkan NaOH berlebih, lalu dialiri gas H2S. Kation yang akan membentuk endapan putih kembali adalah...",
        "pilihan": ["Zn^2+", "Al^3+", "Dua-duanya larut", "Dua-duanya mengendap"],
        "jawaban": "Zn^2+",
        "pembahasan": "Aluminium tidak mengendap dengan H2S, sedangkan Seng (Zn^2+) akan membentuk endapan seng sulfida (ZnS) yang berwarna putih."
    },
    {
        "pertanyaan": "Warna nyala kuning yang sangat dominan dan terang pada uji nyala disebabkan oleh keberadaan kation...",
        "pilihan": ["Natrium (Na+)", "Kalium (K+)", "Litium (Li+)", "Barium (Ba2+)"],
        "jawaban": "Natrium (Na+)",
        "pembahasan": "Natrium (Na+) memberikan warna nyala kuning emas yang sangat kuat bahkan pada intensitas konsentrasi yang kecil."
    },
    {
        "pertanyaan": "Pereaksi spesifik yang digunakan untuk mengidentifikasi kation Ni^2+ (Nikel) dalam suasana amoniakal sehingga menghasilkan endapan merah rose/merah muda adalah...",
        "pilihan": ["Dimetilglioksim (DMG)", "Asam Oksalat", "Kalson", "Ditianon"],
        "jawaban": "Dimetilglioksim (DMG)",
        "pembahasan": "Uji DMG adalah uji spesifik untuk nikel (Ni2+) yang menghasilkan kompleks kelat Ni(DMG)2 berwarna merah rose."
    },
    {
        "pertanyaan": "Kation Golongan IV (Ba2+, Sr2+, Ca2+) dipisahkan dari golongan lainnya dengan mengendapkannya sebagai garam...",
        "pilihan": ["Karbonat", "Klorida", "Sulfida", "Hidroksida"],
        "jawaban": "Karbonat",
        "pembahasan": "Kation golongan IV diendapkan menggunakan amonium karbonat (NH4)2CO3 dalam suasana netral atau sedikit basa."
    },
    {
        "pertanyaan": "Anion yang jika ditambahkan asam kuat (seperti HCl atau H2SO4 encer) langsung menghasilkan gas CO2 yang dapat mengeruhkan air kapur adalah...",
        "pilihan": ["Karbonat (CO3^2-)", "Sulfat (SO4^2-)", "Klorida (Cl-)", "Nitrat (NO3-)"],
        "jawaban": "Karbonat (CO3^2-)",
        "pembahasan": "Karbonat terdekomposisi oleh asam membentuk gas CO2. Gas CO2 jika dialirkan ke air kapur Ca(OH)2 akan membentuk endapan putih CaCO3."
    },
    {
        "pertanyaan": "Larutan barium klorida (BaCl2) digunakan sebagai pereaksi utama untuk menguji adanya anion...",
        "pilihan": ["Sulfat (SO4^2-)", "Klorida (Cl-)", "Nitrat (NO3-)", "Asetat (CH3COO-)"],
        "jawaban": "Sulfat (SO4^2-)",
        "pembahasan": "Ion Ba^2+ akan berikatan dengan SO4^2- membentuk endapan putih Barium Sulfat (BaSO4) yang sangat stabil dan tidak larut dalam asam encer."
    },
    {
        "pertanyaan": "Uji cincin cokelat (brown ring test) yang menggunakan FeSO4 and H2SO4 pekat digunakan untuk mengidentifikasi anion...",
        "pilihan": ["Nitrat (NO3-)", "Klorida (Cl-)", "Bromida (Br-)", "Fosfat (PO4^3-)"],
        "jawaban": "Nitrat (NO3-)",
        "pembahasan": "Cincin cokelat terbentuk akibat adanya kompleks [Fe(H2O)5(NO)]^2+ pada batas kedua cairan, menandakan adanya ion nitrat."
    },
    {
        "pertanyaan": "Anion Halida yang memberikan endapan kuning muda (pale yellow) dengan AgNO3 and endapan tersebut sukar larut dalam amonia encer adalah...",
        "pilihan": ["Bromida (Br-)", "Klorida (Cl-)", "Iodida (I-)", "Fluorida (F-)"],
        "jawaban": "Bromida (Br-)",
        "pembahasan": "AgCl (putih, mudah larut amonia), AgBr (kuning muda, sukar larut), AgI (kuning kuat, tidak larut amonia)."
    },
    {
        "pertanyaan": "Bagaimanakah bau gas H2S (Hidrogen Sulfida) yang khas ketika sampel mengandung anion S^2- ditambahkan asam kuat?",
        "pilihan": ["Telur busuk", "Cuka", "Buah busuk", "Amonia menyengat"],
        "jawaban": "Telur busuk",
        "pembahasan": "Asam akan mendesak sulfida membentuk gas H2S (Hidrogen Sulfida) yang terkenal memiliki bau menyengat seperti telur busuk."
    },
    {
        "pertanyaan": "Anion yang jika digerus dengan sedikit H2SO4 pekat akan melepaskan uap berbau cuka yang tajam adalah...",
        "pilihan": ["Asetat (CH3COO-)", "Oksalat (C2O4^2-)", "Klorida (Cl-)", "Nitrat (NO3-)"],
        "jawaban": "Asetat (CH3COO-)",
        "pembahasan": "Reaksi asetat dengan asam kuat akan membebaskan molekul asam asetat (CH3COOH) alias asam cuka yang mudah menguap."
    },
    {
        "pertanyaan": "Pereaksi Amonium Molybdat dalam suasana asam nitrat digunakan untuk menguji keberadaan anion...",
        "pilihan": ["Fosfat (PO4^3-)", "Sulfat (SO4^2-)", "Kromat (CrO4^2-)", "Sianida (CN-)"],
        "jawaban": "Fosfat (PO4^3-)",
        "pembahasan": "Ion fosfat bereaksi dengan amonium molybdat membentuk endapan kristal kuning amonium fosfomolybdat."
    },
    {
        "pertanyaan": "Anion yang memiliki warna larutan kuning asli, dan berubah menjadi jingga jika suasana larutan diubah menjadi asam adalah...",
        "pilihan": ["Kromat (CrO4^2-)", "Dikromat (Cr2O7^2-)", "Permanganat (MnO4-)", "Tiosianat (SCN-)"],
        "jawaban": "Kromat (CrO4^2-)",
        "pembahasan": "Ion kromat (CrO4^2-, kuning) berkesetimbangan dengan dikromat (Cr2O7^2-, jingga). Penambahan asam mendesak kesetimbangan ke arah dikromat."
    },
    {
        "pertanyaan": "Larutan AgNO3 jika ditambahkan ke dalam larutan yang mengandung anion Iodida (I-) akan menghasilkan endapan berwarna...",
        "pilihan": ["Kuning", "Putih", "Hitam", "Merah bata"],
        "jawaban": "Kuning",
        "pembahasan": "Reaksi menghasilkan endapan Perak Iodida (AgI) yang berwarna kuning cerah and tidak larut dalam larutan amonia."
    },
    {
        "pertanyaan": "Anion manakah di bawah ini yang tidak menghasilkan endapan dengan larutan AgNO3 maupun BaCl2 dalam suasana netral?",
        "pilihan": ["Nitrat (NO3-)", "Klorida (Cl-)", "Sulfat (SO4^2-)", "Karbonat (CO3^2-)"],
        "jawaban": "Nitrat (NO3-)",
        "pembahasan": "Hampir semua garam nitrat (NO3-) larut dalam air, sehingga tidak membentuk endapan dengan pereaksi kation umum."
    }
]

# --- INISIALISASI SESSION STATE ---
if "login_sukses" not in st.session_state:
    st.session_state["login_sukses"] = False
if "logbook_data" not in st.session_state:
    st.session_state["logbook_data"] = []
if "target_belajar" not in st.session_state:
    st.session_state["target_belajar"] = "Belum ditentukan"
if "pemicu_petasan" not in st.session_state:
    st.session_state["pemicu_petasan"] = False
if "tahapan_ujian" not in st.session_state:
    st.session_state["tahapan_ujian"] = []

# --- INISIALISASI STATE UNTUK KUIS ---
if "soal_acak" not in st.session_state:
    st.session_state.soal_acak = random.sample(SOAL_MASTER, len(SOAL_MASTER))
if "skor" not in st.session_state:
    st.session_state.skor = 0
if "index_soal" not in st.session_state:
    st.session_state.index_soal = 0
if "sudah_jawab" not in st.session_state:
    st.session_state.sudah_jawab = False

# --- DATA GAMBAR URL LANGSUNG ---
# Gambar untuk halaman login (Analis)
URL_GAMBAR_LOGIN = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800"
# Gambar untuk beranda (Banner Minimalis Erlenmeyer Warna-warni)
URL_GAMBAR_BERANDA_BANNER = "https://images.unsplash.com/photo-1617155093730-a8bf47be792d?auto=format&fit=crop&q=80&w=1200&h=400"

# --- HALAMAN 1: FORM LOGIN ---
if not st.session_state["login_sukses"]:
    st.markdown("<h2 style='text-align: center; color: #0284C7;'>🔐 LOGIN SISTEM LABORATORIUM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Silakan masukkan kredensial analis Anda untuk mengakses instrumen lab.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        # Menampilkan gambar laboratorium Analis di halaman depan
        st.image(URL_GAMBAR_LOGIN, caption="Fasilitas Lab Kimia Analisis Kualitatif", use_container_width=True)
            
        with st.form("form_login"):
            username = st.text_input("Username Analis", placeholder="Masukkan username...")
            password = st.text_input("Password", type="password", placeholder="Masukkan password...")
            tombol_login = st.form_submit_button("Masuk ke Laboratorium")
            
            if tombol_login:
                if username == USER_VALID and password == PASSWORD_VALID:
                    st.session_state["login_sukses"] = True
                    st.session_state["pemicu_petasan"] = True
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
        pilihan_halaman = st.sidebar.radio(
            "Pilih Halaman Kerja:",
            [
                "🏠 Beranda Lab", 
                "⚡ Identifikasi Ion", 
                "🧪 Rak Reagen Organik", 
                "🎮 Simulator TPS (Ujian)", 
                "🦺 K3 & APD Laboratorium", 
                "🏆 Kuis Akbar Kualitatif", 
                "📚 Referensi & Video", 
                "📋 Logbook Pengujian"
            ]
        )
        
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)"):
            st.session_state["login_sukses"] = False
            st.session_state["pemicu_petasan"] = False
            st.rerun()

    # --- KONTEN HALAMAN UTAMA (SISI KANAN) ---
    
    # ================= KONDISI A: BERANDA LAB =================
    if pilihan_halaman == "🏠 Beranda Lab":
        if st.session_state["pemicu_petasan"]:
            st.balloons()
            st.success("🎉 *Yey kamu berhasil login!* Selamat datang kembali di laboratorium virtual.")
            st.session_state["pemicu_petasan"] = False

        st.markdown("<h2 style='text-align: center; color: #0284C7;'>👋 SELAMAT DATANG DI ASISTEN LAB ANALITIK</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Sistem Informasi Manajemen Reagen & Instrumentasi Virtual</p>", unsafe_allow_html=True)
        
        # --- MENAMPILKAN GAMBAR BANNER KECIL (BERANDA) DI ATAS QUOTES ---
        # Gambar banner horizontal yang kecil dan minimalis
        st.image(URL_GAMBAR_BERANDA_BANNER, caption="Koleksi Reagen Lab Virtual", use_container_width=True)
            
        st.markdown("---")
        
        # Kotak Quotes Motivasi Asli
        st.markdown("""
            <div style='background-color: #E0F2FE; border-left: 6px solid #0284C7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 25px;'>
                <p style='color: #0369A1; font-style: italic; font-size: 16px; margin: 0;'>
                    "Sama seperti reaksi kimia eksoterm yang melepaskan energi, biarlah semangat belajarmu hari ini memancar dan menginspirasi sekitar! Jangan takut salah, karena eror dan kegagalan di lab adalah fraksi murni dari proses menuju kebenaran ilmiah."
                </p>
                <p style='color: #0284C7; font-size: 12px; font-weight: bold; margin-top: 5px; margin-bottom: 0;'>🔬 Salam Analis Hebat 🔬</p>
            </div>
        """, unsafe_allow_html=True)

        # Kartu Sambutan Asli
        st.markdown("""
            <div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 25px;'>
                <h4 style='color: #1E293B; margin: 0;'>Halo, Analis Kimia! 🧪</h4>
                <p style='color: #475569; margin-top: 8px; line-height: 1.5; font-size: 15px;'>
                    Selamat datang di platform asisten laboratorium virtual. Web ini sekarang dilengkapi dengan modul utama: 
                    <b>Identifikasi Kation/Anion Anorganik</b>, <b>Uji Gugus Fungsi Organik</b>, serta <b>Referensi Video & Buku Panduan</b> resmi. Silakan tentukan target belajar Anda di bawah sebelum memulai praktikum virtual!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
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
            index=None, placeholder="Pilih metode pengujian ion..."
        )
        st.divider()

        nama_reagen = "-"
        kesimpulan_gugus = "-"

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
                        nama_reagen, kesPrefix = "Filtrat -> K2CrO4 Filtrat -> H2C2O4 + NH4OH", "Kation Kalsium (Ca²⁺)"

        elif jenis_analisis == "Uji Anion (Non-Logam)":
            st.subheader("Uji Identifikasi Anion Spesifik")
            reagen_anion = st.selectbox("Pilih reagen yang ditambahkan ke sampel:", [
                "BaCl2 (Barium Klorida)", "AgNO3 (Perak Nitrat)", "FeSO4 + H2SO4 pekat (Uji Cincin Cokelat)"
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
                    nama_reagen, kesPrefix = "AgNO3", "Anion Bromida (Br⁻)"
                elif hasil_agno3 == "Kuning Terang":
                    st.success("✨ Anion Teridentifikasi: *Iodida ($I^-$)*")
                    nama_reagen, kesKeep = "AgNO3", "Anion Iodida (I⁻)"
            elif reagen_anion == "FeSO4 + H2SO4 pekat (Uji Cincin Cokelat)":
                st.write("Hasil: Terbentuk cincin berwarna cokelat di antara dua lapisan cairan.")
                st.success("✨ Anion Teridentifikasi: *Nitrat ($NO_3^-$)*")
                nama_reagen, kesimpulan_gugus = "FeSO4 + H2SO4 pekat", "Anion Nitrat (NO₃⁻)"

        elif jenis_analisis == "Uji Nyala Api (Flame Test)":
            st.subheader("Uji Nyala Logam Alkali & Alkali Tanah")
            warna_nyala = st.selectbox("Pilih warna nyala api yang terlihat:", [
                "Kuning keemasan intens", "Merah bata / Merah jingga", "Hijau kekuningan / Hijau apel", "Merah tua (Crimson)", "Ungu / Lilac"
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
                nama_reagen, kesvillain = "Flame Test", "Logam Kalium (K⁺)"

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
                st.success("📝 Data pengujian anorganik berhasil direkam ke Logbook digital.")
                st.toast("Data terekam!", icon="📝")

    # ================= KONDISI C: RAK REAGEN ORGANIK =================
    elif pilihan_halaman == "🧪 Rak Reagen Organik":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🧪 RAK REAGEN VIRTUAL (ORGANIK)</h2>", unsafe_allow_html=True)
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
                st.success("📝 Data pengujian organik berhasil direkam ke Logbook digital.")
                st.toast("Data terekam!", icon="📝")

    # ================= KONDISI D: SIMULATOR UJIAN TPS VIRTUAL =================
    elif pilihan_halaman == "🎮 Simulator TPS (Ujian)":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🎮 SIMULATOR TES PRAKTIK SIMULTAN (TPS)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Uji logika pemisahan kation kamu di sini. Tebak isi botol sampel misterius!</p>", unsafe_allow_html=True)
        st.divider()

        st.warning("🔬 *Botol Ujian Nomor 07:* Analisis kation apa yang ada di dalam botol ini!")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("➕ Tambahkan Larutan HCl Encer"):
                st.session_state["tahapan_ujian"].append("Ditambah HCl -> Terbentuk Endapan Putih")
        with col_m2:
            if st.button("🔥 Panaskan Endapan + Sentrifugasi"):
                if "Ditambah HCl -> Terbentuk Endapan Putih" in st.session_state["tahapan_ujian"]:
                    st.session_state["tahapan_ujian"].append("Dipanaskan -> Endapan Larut Sempurna")
                else:
                    st.error("Eror Prosedur: Tambahkan HCl dulu sebelum memanaskan endapan!")

        if st.session_state["tahapan_ujian"]:
            st.info("📋 *Jalur Reaksi yang Anda Lakukan:*")
            for langkah in st.session_state["tahapan_ujian"]:
                st.write(f"- {langkah}")

        with st.form("form_tps"):
            tebakan = st.selectbox("Kesimpulan Akhir Anda, Kation Ini Adalah:", ["Perak (Ag+)", "Timbal (Pb2+)", "Besi (Fe3+)", "Aluminium (Al3+)"])
            submit_ujian = st.form_submit_button("Kirim Jawaban ke Instruktur")
            if submit_ujian:
                if tebakan == "Timbal (Pb2+)":
                    st.balloons()
                    st.success("🎉 *Luar Biasa! Jawaban Benar.* Nilai TPS Anda: 100! Prosedur pemisahan Anda valid.")
                    st.session_state["tahapan_ujian"] = []
                else:
                    st.error("❌ *Jawaban Salah!* Cek kembali kelarutan senyawa kloridanya.")

    # ================= KONDISI E: REVISI MODUL K3 & APD VIRTUAL =================
    elif pilihan_halaman == "🦺 K3 & APD Laboratorium":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🦺 Pusat Panduan Interaktif K3 & APD Laboratorium</h2>", unsafe_allow_html=True)
        st.write("Platform edukasi digital untuk memastikan keselamatan kerja sebelum melakukan praktikum kimia analisis kualitatif.")
        st.markdown("---")

        tab_apd, tab_simulasi, tab_darurat = st.tabs([
            "🛡️ 1. Katalog APD Wajib", "🕹️ 2. Simulasi Memakai APD", "🚨 3. Prosedur Darurat (First Aid)"
        ])

        with tab_apd:
            st.header("Katalog Alat Pelindung Diri (APD) Standar")
            st.write("Berikut adalah spesifikasi APD yang wajib digunakan di laboratorium kimia:")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.subheader("👕 1. Jas Laboratorium")
                    st.markdown("""
                    * *Bahan:* Katun 100% (Tebal).
                    * *Fungsi:* Melindungi tubuh dan pakaian harian dari percikan zat asam/basa pekat.
                    * *Aturan K3:* Wajib berlengan panjang dan seluruh kancing harus terpasang rapi. Dilarang menggulung lengan baju.
                    """)
                with st.container(border=True):
                    st.subheader("🥽 2. Safety Goggles (Kacamata Pelindung)")
                    st.markdown("""
                    * *Bahan:* Polikarbonat anti-pecah dengan pelindung samping rapat.
                    * *Fungsi:* Mencegah percikan cairan korosif atau uap tajam langsung mengenai kornea mata.
                    * *Aturan K3:* Kacamata baca biasa tidak diizinkan sebagai pengganti karena memiliki celah di bagian samping.
                    """)
            with col2:
                with st.container(border=True):
                    st.subheader("🧤 3. Sarung Tangan Nitril")
                    st.markdown("""
                    * *Bahan:* Karet Nitril sintetik (bebas latex).
                    * *Fungsi:* Melindungi pori-pori kulit dari penetrasi larutan logam berat berbahaya ($Pb^{2+}$, $Hg^{2+}$) dan asam pekat.
                    * *Aturan K3:* Jangan gunakan sarung tangan kain karena justru menyerap cairan kimia.
                    """)
                with st.container(border=True):
                    st.subheader("👟 4. Sepatu Tertutup")
                    st.markdown("""
                    * *Bahan:* Kulit atau sintetik tebal (bukan kain tipis/kanvas).
                    * *Fungsi:* Menahan jatuhnya alat kaca yang pecah atau tumpahan reagen cair di lantai.
                    * *Aturan K3:* Sandal, sepatu sandal, atau flat-shoes dengan punggung kaki terbuka dilarang keras.
                    """)

        with tab_simulasi:
            st.header("🕹️ Simulasi Virtual: Ruang Ganti APD")
            st.write("Sebelum Anda diizinkan klik 'Masuk Laboratorium', lengkapi diri Anda dengan memilih APD yang benar di bawah ini:")
            pilih_jas = st.checkbox("Pakai Jas Laboratorium Katun Lengan Panjang")
            pilih_goggles = st.checkbox("Pakai Safety Goggles Rapat")
            pilih_sarung = st.selectbox("Pilih Jenis Sarung Tangan:", ["Tidak Pakai", "Sarung Tangan Kain", "Sarung Tangan Nitril K3"])
            pilih_sepatu = st.radio("Pilih Alas Kaki:", ["Sandal Santai", "Sepatu Kanvas / Slip-on", "Sepatu Kulit Tertutup"], index=0)
            
            st.markdown("---")
            if st.button("Verifikasi Kesiapan APD 🛡️", type="primary"):
                is_aman = True
                pesan_error = []
                if not pilih_jas: is_aman = False; pesan_error.append("- Anda belum memakai Jas Laboratorium.")
                if not pilih_goggles: is_aman = False; pesan_error.append("- Mata Anda sangat rentan, pasang Safety Goggles!")
                if pilih_sarung != "Sarung Tangan Nitril K3": is_aman = False; pesan_error.append("- Pilihan sarung tangan salah! Gunakan bahan Nitril untuk proteksi kimia.")
                if pilih_sepatu != "Sepatu Kulit Tertutup": is_aman = False; pesan_error.append("- Alas kaki tidak aman. Wajib menggunakan Sepatu Tertutup.")
                
                if is_aman:
                    st.balloons()
                    st.success("🟢 STATUS: AMAN! Seluruh APD Anda memenuhi standar K3. Anda diizinkan masuk ke laboratorium.")
                else:
                    st.error("🔴 STATUS: BAHAYA / DITOLAK! Anda belum siap memasuki laboratorium karena:")
                    for err in pesan_error: st.write(err)

        with tab_darurat:
            st.header("🚨 Prosedur Tanggap Darurat Laboratorium")
            st.write("Jika terjadi kecelakaan kerja, lakukan tindakan pertolongan pertama berikut secara tenang namun cepat:")
            with st.expander("👁️ 1. Kontaminasi Bahan chemical pada Mata"):
                st.markdown("""
                * *Tindakan:* Segera bawa korban ke *Eye Wash Station*.
                * *Prosedur:* Bilas mata dengan air mengalir bersih selama minimal 15-20 menit dengan posisi kelopak mata dipaksa terbuka. 
                * *Larangan:* Jangan menggosok mata dengan tangan atau tisu. Hubungi tim medis setelah pembilasan selesai.
                """)
            with st.expander("🦺 2. Tumpahan Zat Kimia Skala Besar ke Tubuh"):
                st.markdown("""
                * *Tindakan:* Segera menuju ke area *Safety Shower* terdekat.
                * *Prosedur:* Tarik tuas pancuran air, lalu lepaskan jas lab atau pakaian yang terkontaminasi secara cepat di bawah guyuran air. Bilas seluruh tubuh secara menyeluruh.
                """)
            with st.expander("🔥 3. Kebakaran Kecil di Meja Praktikum"):
                st.markdown("""
                * *Tindakan:* Gunakan *APAR (Alat Pemadam Api Ringan)*.
                * *Prosedur:* Ingat teknik *PASS* (Pull/Tarik pin, Aim/Arahkan ke sumber api, Squeeze/Tekan tuas, Sweep/Sapukan dari sisi ke sisi). Anda juga bisa menutup api kecil menggunakan kain lap yang telah dibasahi air.
                """)

    # ================= KONDISI F: SEGMEN KUIS 20 SOAL =================
    elif pilihan_halaman == "🏆 Kuis Akbar Kualitatif":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🏆 KUIS AKBAR: KATION & ANION</h2>", unsafe_allow_html=True)
        st.write("Uji pemahaman mendalam Anda mengenai reaksi identifikasi kimia kualitatif di sini!")
        st.markdown("---")

        if st.session_state.index_soal < len(st.session_state.soal_acak):
            soal_sekarang = st.session_state.soal_acak[st.session_state.index_soal]
            total_soal = len(st.session_state.soal_acak)
            
            st.progress(st.session_state.index_soal / total_soal, text=f"Kemajuan: Soal {st.session_state.index_soal + 1} dari {total_soal}")
            st.markdown(f"### *Soal {st.session_state.index_soal + 1}*")
            st.subheader(soal_sekarang["pertanyaan"])
            
            pilihan = st.radio("Pilih salah satu jawaban:", soal_sekarang["pilihan"], index=None, key=f"q_{st.session_state.index_soal}")
            st.write("")
            
            if not st.session_state.sudah_jawab:
                if st.button("Kirim Jawaban 📩", use_container_width=True):
                    if pilihan is not None:
                        st.session_state.sudah_jawab = True
                        if pilihan == soal_sekarang["jawaban"]:
                            st.session_state.skor += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Tolong pilih salah satu opsi terlebih dahulu sebelum mengirim!")
            else:
                if pilihan == soal_sekarang["jawaban"]:
                    st.success("🎯 *Benar!* Jawaban Anda tepat sekali.")
                else:
                    st.error(f"❌ *Salah.* Jawaban Anda: {pilihan}")
                    st.warning(f"💡 *Jawaban yang Benar:* {soal_sekarang['jawaban']}")
                    
                with st.expander("📖 Lihat Pembahasan Lengkap", expanded=True):
                    st.write(soal_sekarang["pembahasan"])
                
                teks_tombol = "Lihat Hasil Akhir 🏆" if st.session_state.index_soal == total_soal - 1 else "Soal Selanjutnya ➡️"
                if st.button(teks_tombol, type="primary", use_container_width=True):
                    st.session_state.index_soal += 1
                    st.session_state.sudah_jawab = False
                    st.rerun()
        else:
            st.balloons()
            st.success("🎉 Selamat! Anda telah menyelesaikan seluruh rangkaian kuis.")
            total_soal = len(st.session_state.soal_acak)
            skor_akhir = (st.session_state.skor / total_soal) * 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Skor Akhir", f"{skor_akhir:.0f} / 100")
            c2.metric("Benar", f"{st.session_state.skor} Soal")
            c3.metric("Salah", f"{total_soal - st.session_state.skor} Soal")
            
            st.markdown("---")
            if skor_akhir == 100: st.subheader("🥇 Luar Biasa! Anda Master Kimia Analisis Kualitatif!")
            elif skor_akhir >= 75: st.subheader("🥈 Kinerja Sangat Baik! Pemahaman Anda sudah sangat kuat.")
            else: st.subheader("📚 Semangat! Terus pelajari tabel kation-anion untuk memperkuat hapalan.")
            
            if st.button("Ulangi Kuis (Soal akan Diacak Lagi) 🔄", use_container_width=True):
                st.session_state.skor = 0
                st.session_state.index_soal = 0
                st.session_state.sudah_jawab = False
                st.session_state.soal_acak = random.sample(SOAL_MASTER, len(SOAL_MASTER))
                st.rerun()

    # ================= KONDISI G: REFERENSI & VIDEO LENGKAP =================
    elif pilihan_halaman == "📚 Referensi & Video":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>📚 REFERENSI METODE & MEDIA BELAJAR VIDEO</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Media literatur buku teks resmi dan video demonstrasi laboratorium</p>", unsafe_allow_html=True)
        st.markdown("---")

        col_buku, col_yt = st.columns([1, 1])

        with col_buku:
            st.markdown("### 📖 Buku Teks & Panduan Standar")
            st.markdown("""
            Gunakan literatur ilmiah tepercaya di bawah ini untuk menyusun dasar teori laporan praktikum:
            1. *Vogel's Qualitative Inorganic Analysis (G. Svehla)*
               * Fokus: Skema pemisahan kation golongan I-V dan pembentukan endapan spesifik.
            2. *Vogel's Textbook of Practical Organic Chemistry*
               * Fokus: Prosedur uji reaksi penentuan gugus fungsi aldehid, keton, dan asam karboksilat.
            3. *Official Methods of Analysis (AOAC International)*
               * Fokus: Regulasi standar pengambilan sampel (sampling) serta preparasi sampel industri.
            """)
            st.info("💡 Tips Literatur: Selalu catat edisi buku dan halaman resep reagen sebagai validitas data analis.")

        with col_yt:
            st.markdown("### 📺 Video Demonstrasi Laboratorium")
            st.markdown("Silakan pilih kategori materi video yang ingin Anda tonton langsung di bawah ini:")
            
            pilihan_kategori = st.selectbox(
                "Pilihan Kategori Utama:",
                ["Uji Gugus Fungsi Organik", "Uji Kation Golongan 1", "Sistem Keselamatan Kerja K3"]
            )

            if pilihan_kategori == "Uji Gugus Fungsi Organik":
                video_organik = st.radio(
                    "Pilih Materi Video Organik:",
                    ["Video 1: Tes Gugus Fungsi Utama", "Video 2: Uji Identifikasi Senyawa Organik", "Video 3: Analisis Reaksi Gugus Fungsi"]
                )
                if video_organik == "Video 1: Tes Gugus Fungsi Utama":
                    st.caption("🎥 Hubungan Struktur Senyawa & Identifikasi Reaksi Kimia")
                    st.video("https://youtu.be/dPXgUFDqSik?si=kfE5aOt1sdj5MNNm")
                elif video_organik == "Video 2: Uji Identifikasi Senyawa Organik":
                    st.caption("🎥 Prosedur Praktikum dan Perubahan Warna Indikator")
                    st.video("https://youtu.be/2g8eB2FEHcA?si=K4XTS-4Swp1pJL3d")
                elif video_organik == "Video 3: Analisis Reaksi Gugus Fungsi":
                    st.caption("🎥 Karakteristik Sifat Fisika & Kimia Larutan Sampel")
                    st.video("https://youtu.be/naS7RTSkmLE?si=gpiOW4oV0Qdcpmw-")
                
            elif pilihan_kategori == "Uji Kation Golongan 1":
                video_kation = st.radio(
                    "Pilih Materi Video Kation:",
                    ["Video 1: Skema Pengendapan Kation Gol I", "Video 2: Konfirmasi Reaksi Timbal, Perak & Merkuri"]
                )
                if video_kation == "Video 1: Skema Pengendapan Kation Gol I":
                    st.caption("🎥 Pemisahan Analisis Kualitatif Kation Menggunakan Reagen HCl")
                    st.video("https://youtu.be/dAygxePSXHg?si=MfmebJCooq7u_In6")
                elif video_kation == "Video 2: Konfirmasi Reaksi Timbal, Perak & Merkuri":
                    st.caption("🎥 Reaksi Spesifik Pembentukan Kompleks Warna Larutan Kation")
                    st.video("https://youtu.be/W7IKGhpKkEk?si=tJ9AUEx8qYhOZamP")
                
            elif pilihan_kategori == "Sistem Keselamatan Kerja K3":
                st.caption("🎥 Prosedur Penanganan Hazard, Penggunaan APD, dan Budaya 5S/Kaizen di Lab Industri")
                st.video("https://youtu.be/BRDApYgvDqQ?si=PUf8bBVqXsMvrJ-e")

    # ================= KONDISI H: TAMPILAN LOGBOOK DATA =================
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
