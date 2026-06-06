import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 1. Konfigurasi Halaman Web Utama
st.set_page_config(page_title="Lab-Analitika: Dashboard Virtual", page_icon="🧪", layout="wide")

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
        "pembahasan": "Ca2+ memberikan warna merah bata. Sebagai tambahan, Na+ memberikan warna kuning, K+ berwarna ungu, dan Ba2+ berwarna hijau apel."
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
        "pertanyaan": "Uji cincin cokelat (brown ring test) yang menggunakan FeSO4 dan H2SO4 pekat digunakan untuk mengidentifikasi anion...",
        "pilihan": ["Nitrat (NO3-)", "Klorida (Cl-)", "Bromida (Br-)", "Fosfat (PO4^3-)"],
        "jawaban": "Nitrat (NO3-)",
        "pembahasan": "Cincin cokelat terbentuk akibat adanya kompleks [Fe(H2O)5(NO)]^2+ pada batas kedua cairan, menandakan adanya ion nitrat."
    },
    {
        "pertanyaan": "Anion Halida yang memberikan endapan kuning muda (pale yellow) dengan AgNO3 dan endapan tersebut sukar larut dalam amonia encer adalah...",
        "pilihan": ["Bromida (Br-)", "Klorida (Cl-)", "Iodida (I-)", "Fluorida (F-)"],
        "jawaban": "Bromida (Br-)",
        "pembahasan": "AgCl (putih, mudah larut amonia), AgBr (kuning muda, sukar larut), AgI (kuning kuat, tidak larut amonia)."
    },
    {
        "pertanyaan": "Jika sampel yang mengandung anion S^2- (Sulfida) ditambahkan asam kuat, akan tercium bau khas seperti...",
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
        "pembahasan": "Reaksi menghasilkan endapan Perak Iodida (AgI) yang berwarna kuning cerah dan tidak larut dalam larutan amonia."
    },
    {
        "pertanyaan": "Anion manakah di bawah ini yang tidak menghasilkan endapan dengan larutan AgNO3 maupun BaCl2 dalam suasana netral?",
        "pilihan": ["Nitrat (NO3-)", "Klorida (Cl-)", "Sulfat (SO4^2-)", "Karbonat (CO3^2-)"],
        "jawaban": "Nitrat (NO3-)",
        "pembahasan": "Hampir semua garam nitrat (NO3-) larut dalam air, sehingga tidak membentuk endapan dengan pereaksi kation umum."
    }
]

# Inisialisasi Session State Global
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

# Inisialisasi Session State Khusus Kuis
if "soal_acak" not in st.session_state:
    st.session_state.soal_acak = random.sample(SOAL_MASTER, len(SOAL_MASTER))
if "skor" not in st.session_state:
    st.session_state.skor = 0
if "index_soal" not in st.session_state:
    st.session_state.index_soal = 0
if "sudah_jawab" not in st.session_state:
    st.session_state.sudah_jawab = False

# --- HALAMAN 1: FORM LOGIN ---
if not st.session_state["login_sukses"]:
    st.markdown("<h2 style='text-align: center; color: #0284C7;'>🔐 LOGIN SISTEM LABORATORIUM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
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
                    st.error("❌ Username atau Password salah!")

# --- HALAMAN 2: APLIKASI UTAMA (Jika Sudah Login) ---
else:
    with st.sidebar:
        st.markdown("### 👤 Profil Analis")
        st.markdown(f"Selamat Datang, *{USER_VALID}*")
        st.caption(f"🎯 Target Hari Ini: {st.session_state['target_belajar']}")
        st.markdown("---")
        
        st.markdown("### 🗺️ Menu Navigasi (Kelompok 1)")
        pilihan_halaman = st.sidebar.radio(
            "Pilih Halaman Kerja:",
            [
                "🏠 Beranda Lab", 
                "⚡ Identifikasi Ion", 
                "🧪 Rak Reagen Organik", 
                "🎮 Simulator TPS (Ujian)", 
                "🦺 K3 & APD Laboratorium", 
                "📊 Perencana Sampling", 
                "🏆 Kuis Akbar Kualitatif", # Menu baru kuis kamu!
                "📚 Referensi & Video", 
                "📋 Logbook Pengujian"
            ]
        )
        
        st.markdown("---")
        if st.button("🚪 Keluar (Logout)"):
            st.session_state["login_sukses"] = False
            st.session_state["pemicu_petasan"] = False
            st.rerun()

    # ================= KONDISI A: BERANDA LAB =================
    if pilihan_halaman == "🏠 Beranda Lab":
        if st.session_state["pemicu_petasan"]:
            st.balloons()
            st.success("🎉 *Yey kamu berhasil login!* Selamat datang di dashboard Kelompok 1.")
            st.session_state["pemicu_petasan"] = False

        st.markdown("<h2 style='text-align: center; color: #0284C7;'>👋 SELAMAT DATANG DI LAB-ANALITIKA VIRTUAL</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Dashboard Eksklusif Kelompok 1 — Spesialisasi Identifikasi Kation & Anion</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🎯 Identifikasi Target Belajar Praktikum")
        opsi_target = [
            "Memahami Sistem Pemisahan Kation Golongan I-V",
            "Mempelajari Reaksi Identifikasi Anion Spesifik (Sulfat, Halida, Nitrat)",
            "Menguasai Karakteristik Warna Uji Nyala Api Logam Alkali/Alkali Tanah"
        ]
        
        with st.form("form_target"):
            pilihan_target = st.selectbox("Pilih Fokus Belajar Anda:", opsi_target)
            tombol_target = st.form_submit_button("🔒 Kunci & Simpan Target Belajar")
            if tombol_target:
                st.session_state["target_belajar"] = pilihan_target
                st.success(f"🎯 Target berhasil dikunci!")
                st.rerun()

    # ================= KONDISI B: IDENTIFIKASI ION ANORGANIK =================
    elif pilihan_halaman == "⚡ Identifikasi Ion":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>⚡ SISTEM IDENTIFIKASI KATION & ANION</h2>", unsafe_allow_html=True)
        st.markdown("---")
        jenis_analisis = st.selectbox("Pilih Metode Analisis:", ["Skema Pemisahan Kation Gol. I-V", "Uji Anion (Non-Logam)", "Uji Nyala Api (Flame Test)"], index=None)
        
        nama_reagen, kesimpulan_gugus = "-", "-"

        if jenis_analisis == "Skema Pemisahan Kation Gol. I-V":
            tahap_1 = st.radio("Tahap 1: Hasil reaksi dengan HCl encer:", ["Terbentuk Endapan (AgCl, PbCl2, Hg2Cl2)", "Berupa Filtrat (Al3+, Fe3+, Ba2+)"], index=None)
            if tahap_1 == "Terbentuk Endapan (AgCl, PbCl2, Hg2Cl2)":
                tahap_2 = st.radio("Apa yang terjadi setelah dicuci & dipanaskan dengan air?", ["Endapan Larut (Pb2+)", "Endapan Tidak Larut (AgCl, Hg2Cl2)"], index=None)
                if tahap_2 == "Endapan Larut (Pb2+)":
                    st.success("✨ Terbentuk endapan $PbCrO_4$ kuning jika ditambah $K_2CrO_4$. Kation: *Timbal ($Pb^{2+}$)*")
                    nama_reagen, kesimpulan_gugus = "HCl -> Panas", "Kation Timbal (Pb²⁺)"

        if kesimpulan_gugus != "-":
            if st.button("💾 Catat ke Logbook"):
                st.session_state["logbook_data"].append({"Waktu Analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Target Belajar": st.session_state["target_belajar"], "Reagen Digunakan": nama_reagen, "Hasil Identifikasi": kesimpulan_gugus})
                st.success("📝 Data berhasil disimpan!")

    # ================= KONDISI C: RAK REAGEN ORGANIK =================
    elif pilihan_halaman == "🧪 Rak Reagen Organik":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🧪 RAK REAGEN VIRTUAL ORGANIK</h2>", unsafe_allow_html=True)
        st.markdown("---")
        col_reg1, col_reg2, col_reg3 = st.columns(3)
        with col_reg1: sakelar_lakmus = st.toggle("Celup Lakmus Biru")
        with col_reg2: sakelar_schiff = st.toggle("Tetes Reagen Schiff")
        with col_reg3: sakelar_bisulfit = st.toggle("Tambah NaHSO3")

        if sakelar_lakmus: st.info("🔴 Hasil: Warna Merah -> Golongan ASAM KARBOKSILAT (—COOH)")
        elif sakelar_schiff: st.info("🟣 Hasil: Ungu Kemerahan -> Golongan ALDEHID (—CHO)")
        elif sakelar_bisulfit: st.info("⚪ Hasil: Kristal Putih -> Golongan KETON (—CO—)")

    # ================= KONDISI D: SIMULATOR UJIAN TPS VIRTUAL =================
    elif pilihan_halaman == "🎮 Simulator TPS (Ujian)":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🎮 SIMULATOR TES PRAKTIK SIMULTAN (TPS)</h2>", unsafe_allow_html=True)
        st.warning("🔬 *Botol Ujian Nomor 07:* Analisis kation apa yang ada di dalam botol ini!")
        
        if st.button("➕ Tambahkan Larutan HCl Encer"):
            st.session_state["tahapan_ujian"].append("Ditambah HCl -> Terbentuk Endapan Putih")
        if st.button("🔥 Panaskan Endapan"):
            st.session_state["tahapan_ujian"].append("Dipanaskan -> Endapan Larut Sempurna")

        if st.session_state["tahapan_ujian"]:
            for langkah in st.session_state["tahapan_ujian"]: st.write(f"- {langkah}")

        with st.form("form_tps"):
            tebakan = st.selectbox("Kesimpulan Akhir Kation:", ["Perak (Ag+)", "Timbal (Pb2+)", "Besi (Fe3+)"])
            if st.form_submit_button("Kirim Jawaban"):
                if tebakan == "Timbal (Pb2+)": st.success("🎉 Jawaban Benar! Nilai Anda: 100")
                else: st.error("❌ Salah, coba cek lagi sifat kelarutannya.")

    # ================= KONDISI E: MODUL K3 & APD LABORAT (REVISI KAMU) =================
    elif pilihan_halaman == "🦺 K3 & APD Laboratorium":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🦺 Pusat Panduan Interaktif K3 & APD Laboratorium</h2>", unsafe_allow_html=True)
        st.write("Platform edukasi digital untuk memastikan keselamatan kerja sebelum praktikum kimia kualitatif.")
        st.markdown("---")

        tab_apd, tab_simulasi, tab_ghs, tab_darurat = st.tabs([
            "🛡️ 1. Katalog APD Wajib", "🕹️ 2. Simulasi Memakai APD", "⚠️ 3. Simbol Bahaya GHS", "🚨 4. Prosedur Darurat (First Aid)"
        ])

        with tab_apd:
            st.header("Katalog Alat Pelindung Diri (APD) Standar")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.subheader("👕 1. Jas Laboratorium")
                    st.markdown("* *Bahan:* Katun 100% (Tebal).\n* *Fungsi:* Melindungi dari percikan zat kimia pekat.")
                with st.container(border=True):
                    st.subheader("🥽 2. Safety Goggles")
                    st.markdown("* *Fungsi:* Mencegah percikan cairan korosif mengenai kornea mata.")
            with col2:
                with st.container(border=True):
                    st.subheader("🧤 3. Sarung Tangan Nitril")
                    st.markdown("* *Fungsi:* Melindungi dari penetrasi logam berat ($Pb^{2+}$, $Hg^{2+}$).")
                with st.container(border=True):
                    st.subheader("👟 4. Sepatu Tertutup")
                    st.markdown("* *Fungsi:* Menahan kejatuhan pecahan kaca atau tumpahan reagen.")

        with tab_simulasi:
            st.header("🕹️ Simulasi Virtual: Ruang Ganti APD")
            pilih_jas = st.checkbox("Pakai Jas Laboratorium Katun Lengan Panjang")
            pilih_goggles = st.checkbox("Pakai Safety Goggles Rapat")
            pilih_sarung = st.selectbox("Pilih Jenis Sarung Tangan:", ["Tidak Pakai", "Sarung Tangan Kain", "Sarung Tangan Nitril K3"])
            pilih_sepatu = st.radio("Pilih Alas Kaki:", ["Sandal Santai", "Sepatu Kanvas", "Sepatu Kulit Tertutup"])
            
            if st.button("Verifikasi Kesiapan APD 🛡️", type="primary"):
                if pilih_jas and pilih_goggles and pilih_sarung == "Sarung Tangan Nitril K3" and pilih_sepatu == "Sepatu Kulit Tertutup":
                    st.balloons()
                    st.success("🟢 STATUS: AMAN! Seluruh APD Anda memenuhi standar K3 Kelompok 1.")
                else:
                    st.error("🔴 STATUS: BAHAYA / DITOLAK! Lengkapi kembali parameter APD wajib Anda.")

        with tab_ghs:
            st.header("⚠️ Sistem Klasifikasi Bahaya GHS")
            simbol = st.radio("Pilih Simbol Bahaya:", ["💀 Toksik Akut", "🔥 Korosif", "⭕ Pengoksidasi", "⚠️ Bahaya Kesehatan Jangka Panjang"])
            if simbol == "💀 Toksik Akut": st.error("### 💀 Toksik Akut\n* *Contoh:* Kalium Sianida ($KCN$), Gas $H_2S$.")
            elif simbol == "🔥 Korosif": st.warning("### 🔥 Korosif\n* *Contoh:* Asam Sulfat ($H_2SO_4$), $HCl$, $NaOH$.")
            elif simbol == "⭕ Pengoksidasi": st.info("### ⭕ Pengoksidasi\n* *Contoh:* Asam Nitrat ($HNO_3$).")
            elif simbol == "⚠️ Bahaya Kesehatan Jangka Panjang": st.warning("### ⚠️ Bahaya Kesehatan\n* *Contoh:* Larutan Kation Timbal ($Pb^{2+}$).")

        with tab_darurat:
            st.header("🚨 Prosedur Tanggap Darurat Laboratorium")
            with st.expander("👁️ 1. Kontaminasi Bahan Kimia pada Mata"): st.markdown("Segera bawa korban ke *Eye Wash Station*, bilas air mengalir selama 15-20 menit.")
            with st.expander("🦺 2. Tumpahan Zat Kimia Skala Besar"): st.markdown("Segera menuju ke area *Safety Shower* terdekat, bilas tubuh secara menyeluruh.")
            with st.expander("🔥 3. Kebakaran Kecil"): st.markdown("Gunakan *APAR* dengan teknik *PASS* (Pull, Aim, Squeeze, Sweep).")

    # ================= KONDISI F: PERENCANA SAMPLING LAPANGAN =================
    elif pilihan_halaman == "📊 Perencana Sampling":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>📊 ASISTEN PERENCANAAN SAMPLING INDUSTRI</h2>", unsafe_allow_html=True)
        total_wadah = st.number_input("Masukkan total wadah di gudang:", min_value=1, value=25)
        st.info(f"💡 Anda wajib mengambil sampel acak dari *{round((total_wadah * 0.5) + 1)} wadah** berbeda ($\sqrt{N}+1$).")

    # ================= KONDISI G: SEGMEN KUIS BARU (DARI KAMU - FIXED BUG) =================
    elif pilihan_halaman == "🏆 Kuis Akbar Kualitatif":
        st.markdown("<h2 style='text-align: center; color: #0284C7;'>🏆 KUIS AKBAR: KATION & ANION INTERAKTIF</h2>", unsafe_allow_html=True)
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
                        st.warning("⚠️ Tolong pilih salah satu opsi terlebih dahulu!")
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
            
            if st.button("Ulangi Kuis 🔄", use_container_width=True):
                st.session_state.skor = 0
                st.session_state.index_soal = 0
                st.session_state.sudah_jawab = False
                st.session_state.soal_acak = random.sample(SOAL_MASTER, len(SOAL_MASTER))
                st.rerun()

    # ================= KONDISI H: REFERENSI & VIDEO =================
    elif pilihan_halaman == "📚 Referensi & Video":
        st.markdown("### 📚 REFERENSI METODE & MEDIA BELAJAR VIDEO")
        st.video("https://youtu.be/dAygxePSXHg?si=MfmebJCooq7u_In6")

    # ================= KONDISI I: LOGBOOK DATA =================
    elif pilihan_halaman == "📋 Logbook Pengujian":
        st.markdown("### 📋 LOGBOOK DIGITAL LABORATORIUM")
        if st.session_state["logbook_data"]:
            st.dataframe(pd.DataFrame(st.session_state["logbook_data"]), use_container_width=True)
