import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import terbilang_desimal, smart_title, parse_tanggal_ke_terbilang, parse_angka_simple, format_display
from db import get_kantor_collection
from datetime import datetime

def run():
    st.header("🏢 Perjanjian Kerjasama Kantor")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Total biaya akan dihitung otomatis</div>""", unsafe_allow_html=True)
    
    template_path = "templates/FIKS - (FRITA) PERJANJIAN KERJASAMA PENDAYAGUNAAN RUANG KANTOR.docx"
    if not os.path.exists(template_path):
        st.error(f"Template '{template_path}' tidak ditemukan di folder aplikasi.")
        return
    
    try:
        doc = DocxTemplate(template_path)
    except Exception as e:
        st.error(f"Error loading template: {str(e)}")
        return

    # ====== INFORMASI DOKUMEN ======
    st.subheader("Informasi Dokumen")
    nama_file = st.text_input("Judul File Dokumen *", "SURAT PERJANJIAN KERJASAMA KANTOR", key="k_nama_file")
    docx_path = f"{nama_file}.docx"

    nomor_perjanjian = st.text_input("Nomor Perjanjian *", key="k_nomor_perjanjian", placeholder="Masukkan nomor perjanjian/SPER", value="SPER/KK/../33000/../20..")
    nomor_perjanjian_upper = (nomor_perjanjian or "").upper()
    
    tgl_setuju = st.date_input("Tanggal Penandatanganan Surat *", key="k_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ====== DATA PENYEWA (PIHAK KEDUA) ======
    st.subheader("Data Penyewa (Pihak Kedua)")
    nama_perusahaan_pihak_kedua = st.text_input("Nama Perusahaan *", key="k_nama_perusahaan", placeholder="Masukkan nama perusahaan")
    nama_perusahaan_pihak_kedua_upper = (nama_perusahaan_pihak_kedua or "").upper()
    nama_perusahaan_pihak_kedua_title = smart_title(nama_perusahaan_pihak_kedua)
    
    jenis_badan_usaha = st.text_area("Jenis Badan Usaha Perusahaan *", key="k_jenis_perusahaan", placeholder="Jelaskan jenis badan usaha perusahaan") 

    nama_pihak_kedua = st.text_input("Nama Penandatangan *", key="k_nama_pihak", placeholder="Masukkan nama lengkap penandatangan beserta gelar")
    nama_pihak_kedua_upper = (nama_pihak_kedua or "").upper()
    nama_pihak_kedua_title = smart_title(nama_pihak_kedua)

    jabatan_pihak_kedua = st.text_input("Jabatan Penandatangan *", key="k_jabatan", placeholder="Contoh: Direktur Utama")
    jabatan_pihak_kedua_upper = (jabatan_pihak_kedua or "").upper()
    jabatan_pihak_kedua_title = smart_title(jabatan_pihak_kedua)

    alamat_pihak_kedua = st.text_input("Alamat Perusahaan *", key="k_alamat", placeholder="Masukkan alamat lengkap perusahaan")
    alamat_pihak_kedua_title = smart_title(alamat_pihak_kedua)
    
    nomor_telepon_pihak_kedua = st.text_input("Nomor Telepon Perusahaan *", key="k_telepon", placeholder="Masukkan nomor telepon")
    email_pihak_kedua = st.text_input("Email Perusahaan", key="k_email", placeholder="Masukkan email perusahaan")

    # ====== DATA LOKASI GEDUNG ======
    st.subheader("Data Lokasi Gedung")
    lokasi_gedung = st.text_input("Lokasi Gedung *", key="k_lokasi_gedung", placeholder="Contoh: Gedung EX-Divisi Pemeliharaan & Perbaikan")
    lokasi_gedung_upper = (lokasi_gedung or "").upper()
    lokasi_gedung_title = smart_title(lokasi_gedung)

    # ====== DASAR PERJANJIAN ======
    st.subheader("Dasar Perjanjian - Pasal 1")
    st.caption("Isi dasar perjanjian dibawah ini dengan benar")
    point_pertama_pasal_1 = st.text_area("Point Pertama *", key="k_point1", placeholder="Masukkan point pertama pasal 1 mengenai Dasar Perjanjian")
    point_kedua_pasal_1 = st.text_area("Point Kedua *", key="k_point2", placeholder="Masukkan point kedua pasal 1 mengenai Dasar Perjanjian")
    point_ketiga_pasal_1 = st.text_area("Point Ketiga *", key="k_point3", placeholder="Masukkan point ketiga pasal 1 mengenai Dasar Perjanjian")

    # ====== DATA UKURAN RUANGAN DAN DURASI ======
    st.subheader("Data Ukuran Ruangan dan Durasi")

    col1, col2, col3 = st.columns(3)
    with col1:
        ukuran_meter = st.text_input("Ukuran Ruangan (m²) *", key="k_ukuran_meter", placeholder="Contoh: 50")
    with col2:
        lama_sewa = st.text_input("Lama Sewa *", key="k_lama_sewa", placeholder="Contoh: 12")
    with col3:
        nilai_ampere = st.text_input("Daya Listrik (Ampere)", key="k_ampere", placeholder="Contoh: 2")

    # Tambahkan satuan sewa (opsional)
    satuan_sewa = st.selectbox(
        "Satuan Sewa",
        ["bulan", "tahun"],
        key="k_satuan_sewa",
        index=0  # default "bulan"
    )

    # Format ukuran meter dengan terbilang
    ukuran_meter_display = ""
    if ukuran_meter:
        terbilang_raw = terbilang_desimal(ukuran_meter)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        ukuran_meter_display = f"{ukuran_meter} ({terbilang_only})"

    # Format lama sewa dengan terbilang
    lama_sewa_display = ""
    if lama_sewa:
        terbilang_raw = terbilang_desimal(lama_sewa)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        lama_sewa_display = f"{lama_sewa} ({terbilang_only}) {satuan_sewa}"

    # ====== DURASI DAN PERIODE SEWA ======
    st.subheader("Periode Sewa")
    tgl_mulai = st.date_input("Tanggal Mulai Sewa *", key="k_tgl_mulai")
    hari_mulai, tanggal_mulai, bulan_mulai, tahun_mulai = parse_tanggal_ke_terbilang(tgl_mulai)

    tgl_selesai = st.date_input("Tanggal Selesai Sewa *", key="k_tgl_selesai")
    hari_selesai, tanggal_selesai, bulan_selesai, tahun_selesai = parse_tanggal_ke_terbilang(tgl_selesai)

    # ====== DATA BIAYA - INPUT LANGSUNG ======
    st.subheader("Data Biaya (Input Langsung)")
    
    col1, col2 = st.columns(2)
    with col1:
        harga_lahan_kantor_input = st.text_input("Harga Biaya Objek*", key="k_harga_lahan_kantor", placeholder="Contoh: 5000000")
    with col2:
        harga_total_listrik_input = st.text_input("Harga Listrik (Rp)", key="k_harga_listrik", placeholder="Contoh: 200000")

    col3, col4 = st.columns(2)
    with col3:
        harga_total_air_input = st.text_input("Biaya Air (Rp)", key="k_air_input", placeholder="Contoh: 100000")
    with col4:
        biaya_sampah_input = st.text_input("Biaya Sampah (Rp)", key="k_sampah_input", placeholder="Contoh: 50000")

    # ====== PERHITUNGAN TOTAL OTOMATIS ======
    st.subheader("Total Biaya Kontribusi")
    
    # Hitung nilai-nilai
    harga_lahan_kantor_num = parse_angka_simple(harga_lahan_kantor_input)
    harga_total_listrik_num = parse_angka_simple(harga_total_listrik_input)
    harga_total_air_num = parse_angka_simple(harga_total_air_input)
    biaya_sampah_num = parse_angka_simple(biaya_sampah_input)
    
    # Hitung total biaya kontribusi
    total_biaya_kontribusi = harga_lahan_kantor_num + harga_total_listrik_num + harga_total_air_num + biaya_sampah_num
    
    # Format nilai untuk template
    nilai_ampere_display = ""
    if nilai_ampere and nilai_ampere.strip():
        terbilang_raw = terbilang_desimal(nilai_ampere)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        nilai_ampere_display = f"{nilai_ampere} ({terbilang_only})"
    
    # Format semua biaya
    harga_lahan_kantor_display = format_display(harga_lahan_kantor_input, harga_lahan_kantor_num)
    harga_total_listrik_display = format_display(harga_total_listrik_input, harga_total_listrik_num)
    harga_total_air_display = format_display(harga_total_air_input, harga_total_air_num)
    biaya_sampah_display = format_display(biaya_sampah_input, biaya_sampah_num)
    total_biaya_kontribusi_display = format_display(str(total_biaya_kontribusi))
    
    # Tampilkan total
    st.text_input("Total Biaya Kontribusi:", value=total_biaya_kontribusi_display, key="k_total_biaya", disabled=True)

    # Konversi ke string untuk template
    context = {
        # INFORMASI DOKUMEN
        "nomor_perjanjian": nomor_perjanjian,
        "nomor_perjanjian_upper": nomor_perjanjian_upper,
        "hari_setuju": hari_setuju,
        "tanggal_setuju": tanggal_setuju,
        "bulan_setuju": bulan_setuju,
        "tahun_setuju": tahun_setuju,
        
        # DATA PENYEWA
        "nama_perusahaan_pihak_kedua": nama_perusahaan_pihak_kedua,
        "nama_perusahaan_pihak_kedua_upper": nama_perusahaan_pihak_kedua_upper,
        "nama_perusahaan_pihak_kedua_title": nama_perusahaan_pihak_kedua_title,
        "jenis_badan_usaha": jenis_badan_usaha,
        "nama_pihak_kedua": nama_pihak_kedua,
        "nama_pihak_kedua_upper": nama_pihak_kedua_upper,
        "nama_pihak_kedua_title": nama_pihak_kedua_title,
        "jabatan_pihak_kedua": jabatan_pihak_kedua,
        "jabatan_pihak_kedua_upper": jabatan_pihak_kedua_upper,
        "jabatan_pihak_kedua_title": jabatan_pihak_kedua_title,

        "alamat_pihak_kedua": alamat_pihak_kedua,
        "alamat_pihak_kedua_title": alamat_pihak_kedua_title,        
        "nomor_telepon_pihak_kedua": nomor_telepon_pihak_kedua,
        "email_pihak_kedua": email_pihak_kedua,

        # DATA LOKASI
        "lokasi_gedung": lokasi_gedung,
        "lokasi_gedung_upper": lokasi_gedung_upper,
        "lokasi_gedung_title": lokasi_gedung_title,

        # DASAR PERJANJIAN
        "point_pertama_pasal_1": point_pertama_pasal_1,
        "point_kedua_pasal_1": point_kedua_pasal_1,
        "point_ketiga_pasal_1": point_ketiga_pasal_1,

        # DATA UKURAN
        "ukuran_meter": ukuran_meter_display,

        # DURASI SEWA
        "lama_sewa": lama_sewa_display,
        "hari_mulai": hari_mulai,
        "tanggal_mulai": tanggal_mulai,
        "bulan_mulai": bulan_mulai,
        "tahun_mulai": tahun_mulai,
        "hari_selesai": hari_selesai,
        "tanggal_selesai": tanggal_selesai,
        "bulan_selesai": bulan_selesai,
        "tahun_selesai": tahun_selesai,

        # DATA BIAYA
        "harga_lahan_kantor": harga_lahan_kantor_display,
        "harga_total_listrik": harga_total_listrik_display,
        "harga_total_air": harga_total_air_display,
        "biaya_sampah": biaya_sampah_display,
        "nilai_ampere": nilai_ampere_display,
        "total_biaya_kontribusi": total_biaya_kontribusi_display,
    }

    st.write("---")
    if st.button("📄 Generate Surat Perjanjian (Kantor)", key="btn_generate_kantor"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian")
        
        # Data Penyewa
        if not nama_perusahaan_pihak_kedua.strip():
            errors.append("Nama Perusahaan")
        if not nama_pihak_kedua.strip():
            errors.append("Nama Penandatangan")
        if not jabatan_pihak_kedua.strip():
            errors.append("Jabatan Penandatangan")
        if not alamat_pihak_kedua.strip():
            errors.append("Alamat Perusahaan")
        if not nomor_telepon_pihak_kedua.strip():
            errors.append("Nomor Telepon")
        
        # Data Lokasi
        if not lokasi_gedung.strip():
            errors.append("Lokasi Gedung")
        
        # Dasar Perjanjian
        if not point_pertama_pasal_1.strip():
            errors.append("Point Pertama Pasal 1")
        if not point_kedua_pasal_1.strip():
            errors.append("Point Kedua Pasal 1")
        if not point_ketiga_pasal_1.strip():
            errors.append("Point Ketiga Pasal 1")
        
        # Data Ukuran
        if not ukuran_meter.strip():
            errors.append("Ukuran Ruangan (meter persegi)")
        
        # Data Biaya - PERBAIKAN: ganti label sesuai dengan input
        if not harga_lahan_kantor_input.strip():
            errors.append("Harga Biaya Objek")
        
        # Durasi Sewa - PERBAIKAN: hapus "(bulan)" karena sekarang ada pilihan satuan
        if not lama_sewa.strip():
            errors.append("Lama Sewa")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return

        # ===== CEK DUPLIKASI =====
        collection = get_kantor_collection()
        if collection.find_one({"Nomor Surat Perjanjian": nomor_perjanjian_upper}):
            st.error("❌ Nomor Surat Perjanjian sudah terdaftar di database!")
            return

        # ===== GENERATE DOCX =====
        try:
            doc.render(context)
            doc.save(docx_path)
        except Exception as e:
            st.error(f"Gagal membuat dokumen: {str(e)}")
            return
        
        # ===== SIMPAN DATABASE (SETELAH DOCX BERHASIL) =====

        data_kantor = {
            "Lokasi": lokasi_gedung_title,
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": nama_perusahaan_pihak_kedua_title,
            "Luas (m²)": ukuran_meter,
            "Tanggal Mulai": tgl_mulai.strftime("%d-%m-%Y"),
            "Tanggal Selesai": tgl_selesai.strftime("%d-%m-%Y"),
            "Biaya Sewa Perbulan": harga_lahan_kantor_input,
            "created_at": datetime.utcnow()
        }

        collection.insert_one(data_kantor)

        # ===== DOWNLOAD =====
        with open(docx_path, "rb") as f:
            st.download_button(
                "⬇ Download DOCX",
                f,
                file_name=f"{nama_file}.docx"
            )

        st.success("✅ Surat berhasil dibuat dan disimpan ke database!")

def show():
    """Fungsi utama untuk ditampilkan di aplikasi Streamlit"""
    run()