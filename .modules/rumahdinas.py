import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import terbilang_desimal, smart_title, parse_tanggal_ke_terbilang, parse_angka_simple, format_display
from db import get_rumah_dinas_collection
from datetime import datetime

def run():
    st.header("🏠 Perjanjian Kerjasama Rumah Dinas/Mess")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Data biaya akan dihitung otomatis</div>""", unsafe_allow_html=True)
    
    template_path = "templates/FIKS - (FRITA) PERJANJIAN RUMAH DINAS.docx"
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
    nama_file = st.text_input("Judul File Dokumen *", "SURAT PERJANJIAN KERJASAMA RUMAH DINAS", key="r_nama_file")
    docx_path = f"{nama_file}.docx"

    nomor_perjanjian = st.text_input("Nomor Perjanjian *", key="r_nomor_perjanjian", 
                                     value="SPER/RD/../33000/../20..",
                                     placeholder="Masukkan nomor perjanjian/SPER")
    nomor_perjanjian_upper = (nomor_perjanjian or "").upper()
    
    tgl_setuju = st.date_input("Tanggal Penandatanganan Surat *", key="r_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ====== DATA RUMAH DINAS ======
    st.subheader("Data Rumah Dinas/Mess")
    
    col1, col2 = st.columns(2)
    with col1:
        alamat_rumdis = st.text_input("Alamat Rumah Dinas *", key="r_alamat_rumdis", 
                                      placeholder="Contoh: Jalan Menanggal No. 67/D1 Surabaya")
    with col2:
        kota_rumdis = st.text_input("Kota Rumah Dinas *", key="r_kota_rumdis", 
                                    placeholder="Contoh: Surabaya", value="Surabaya")
    
    alamat_rumdis_upper = (alamat_rumdis or "").upper()
    alamat_rumdis_title = smart_title(alamat_rumdis)
    kota_rumdis_title = smart_title(kota_rumdis)
    
    provinsi_rumdis = st.text_input("Provinsi Rumah Dinas", key="r_provinsi_rumdis", 
                                    placeholder="Contoh: Jawa Timur", value="Jawa Timur")
    provinsi_rumdis_title = smart_title(provinsi_rumdis)
    
    ukuran_meter = st.text_input("Luas Bangunan (m²) *", key="r_ukuran_meter", 
                                 placeholder="Contoh: 60")

    # ====== FORMAT UKURAN BANGUNAN ======
    # Format ukuran_meter2: "60 m² (enam puluh meter persegi)"
    ukuran_meter2_display = ""
    if ukuran_meter:
        try:
            meter_int = int(float(ukuran_meter))
            terbilang_raw = terbilang_desimal(str(meter_int))
            terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
            ukuran_meter2_display = f"{meter_int} m² ({terbilang_only} meter persegi)"
        except:
            ukuran_meter2_display = f"{ukuran_meter} m²"

    # ====== DATA PIHAK KEDUA ======
    st.subheader("Data Pihak Kedua")
    nama_perusahaan_pihak_kedua = st.text_input("Nama Perusahaan *", key="r_nama_perusahaan", placeholder="Masukkan nama perusahaan")
    
    nama_perusahaan_pihak_kedua_upper = (nama_perusahaan_pihak_kedua or "").upper()
    nama_perusahaan_pihak_kedua_title = smart_title(nama_perusahaan_pihak_kedua)
    
    jenis_badan_usaha = st.text_area("Jenis Badan Usaha Perusahaan *", key="r_jenis_perusahaan", placeholder="Jelaskan jenis badan usaha perusahaan") 

    nama_pihak_kedua = st.text_input("Nama Penandatangan *", key="r_nama_pihak", 
                                     placeholder="Masukkan nama lengkap penandatangan beserta gelar")
    nama_pihak_kedua_upper = (nama_pihak_kedua or "").upper()
    nama_pihak_kedua_title = smart_title(nama_pihak_kedua)

    jabatan_pihak_kedua = st.text_input("Jabatan Penandatangan *", key="r_jabatan", 
                                        placeholder="Contoh: Direktur Utama, Manager")
    jabatan_pihak_kedua_upper = (jabatan_pihak_kedua or "").upper()
    jabatan_pihak_kedua_title = smart_title(jabatan_pihak_kedua)
    
    nomor_telepon_pihak_kedua = st.text_input("Nomor Telepon/HP *", key="r_telepon", 
                                              placeholder="Masukkan nomor telepon")
    email_pihak_kedua = st.text_input("Email Perusahaan *", key="r_email", 
                                      placeholder="Masukkan email perusahaan")

    # ====== DURASI SEWA ======
    st.subheader("Durasi dan Periode Sewa")
    
    col1, col2 = st.columns(2)
    with col1:
        lama_sewa = st.text_input("Lama Sewa *", key="r_lama_sewa", 
                                  placeholder="Contoh: 12")
    with col2:
        satuan_sewa = st.selectbox("Satuan Sewa", ["bulan", "tahun"], key="r_satuan_sewa", index=1)
    
    # Format lama sewa
    lama_sewa_angka = lama_sewa
    lama_sewa_terbilang = ""
    if lama_sewa:
        terbilang_raw = terbilang_desimal(lama_sewa)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        lama_sewa_terbilang = f"{lama_sewa} ({terbilang_only}) {satuan_sewa}"

    # ====== PERIODE SEWA ======
    st.subheader("Periode Sewa")
    
    tgl_mulai = st.date_input("Tanggal Mulai Sewa *", key="r_tgl_mulai")
    hari_mulai, tanggal_mulai, bulan_mulai, tahun_mulai = parse_tanggal_ke_terbilang(tgl_mulai)

    tgl_selesai = st.date_input("Tanggal Selesai Sewa *", key="r_tgl_selesai")
    hari_selesai, tanggal_selesai, bulan_selesai, tahun_selesai = parse_tanggal_ke_terbilang(tgl_selesai)

    # ====== DASAR PERJANJIAN ======
    st.subheader("Dasar Perjanjian - Pasal 1")
    st.caption("Isi dasar perjanjian dibawah ini dengan benar")
    
    point_pertama_pasal_1 = st.text_area("Point Pertama *", key="r_point1", 
                                         placeholder="Masukkan point pertama pasal 1 mengenai Dasar Perjanjian",
                                         height=100)

    # ====== DATA BIAYA SEWA ======
    st.subheader("Data Biaya Sewa")
    
    harga_sewa_tahunan = st.text_input("Harga Sewa per Tahun (Rp) *", key="r_harga_sewa", 
                                       placeholder="Contoh: 50000000")
    
    # Format harga sewa
    harga_sewa_num = parse_angka_simple(harga_sewa_tahunan)
    harga_sewa_rumdis_terbilang = format_display(harga_sewa_tahunan, harga_sewa_num)
    
    # # Jika satuan bulan, konversi ke tahun untuk perhitungan
    # lama_sewa_num = parse_angka_simple(lama_sewa)
    # if satuan_sewa == "bulan":
    #     # Konversi bulan ke tahun untuk perhitungan
    #     lama_sewa_tahun = lama_sewa_num / 12
    #     total_biaya = harga_sewa_num * lama_sewa_tahun
    #     # st.info(f"**Harga Sewa per Tahun:** {harga_sewa_rumdis_terbilang}")
    #     # st.info(f"**Total Biaya untuk {lama_sewa_num} bulan:** {format_display(str(int(total_biaya)))}")
    #     st.text_input("Total Biaya Kontribusi:", value=harga_sewa_rumdis_terbilang, key="r_total_biaya", disabled=True)

    # else:
    #     # Satuan sudah tahun
    #     total_biaya = harga_sewa_num * lama_sewa_num
    #     # st.info(f"**Harga Sewa per Tahun:** {harga_sewa_rumdis_terbilang}")
    #     # st.info(f"**Total Biaya untuk {lama_sewa_num} tahun:** {format_display(str(int(total_biaya)))}")

    # Konversi ke string untuk template
    context = {
        # INFORMASI DOKUMEN
        "nomor_perjanjian": nomor_perjanjian,
        "nomor_perjanjian_upper": nomor_perjanjian_upper,
        "hari_setuju": hari_setuju,
        "tanggal_setuju": tanggal_setuju,
        "bulan_setuju": bulan_setuju,
        "tahun_setuju": tahun_setuju,
        
        # DATA RUMAH DINAS
        "alamat_rumdis": alamat_rumdis,
        "alamat_rumdis_upper": alamat_rumdis_upper,
        "alamat_rumdis_title": alamat_rumdis_title,
        "kota_rumdis": kota_rumdis,
        "kota_rumdis_title": kota_rumdis_title,
        "provinsi_rumdis": provinsi_rumdis,
        "provinsi_rumdis_title": provinsi_rumdis_title,
        
        # DATA UKURAN BANGUNAN
        "ukuran_meter": ukuran_meter,
        "ukuran_meter2": ukuran_meter2_display,
        
        # DATA PIHAK KEDUA
        "jenis_badan_usaha": jenis_badan_usaha,
        "nama_perusahaan_pihak_kedua": nama_perusahaan_pihak_kedua,
        "nama_perusahaan_pihak_kedua_upper": nama_perusahaan_pihak_kedua_upper,
        "nama_perusahaan_pihak_kedua_title": nama_perusahaan_pihak_kedua_title,
        
        "nama_pihak_kedua": nama_pihak_kedua,
        "nama_pihak_kedua_upper": nama_pihak_kedua_upper,
        "nama_pihak_kedua_title": nama_pihak_kedua_title,
        
        "jabatan_pihak_kedua": jabatan_pihak_kedua,
        "jabatan_pihak_kedua_upper": jabatan_pihak_kedua_upper,
        "jabatan_pihak_kedua_title": jabatan_pihak_kedua_title,
        
        "nomor_telepon_pihak_kedua": nomor_telepon_pihak_kedua,
        "email_pihak_kedua": email_pihak_kedua,
        
        # DURASI SEWA
        "lama_sewa": lama_sewa_angka,
        "lama_sewa_terbilang": lama_sewa_terbilang,
        "satuan_sewa": satuan_sewa,
        
        "hari_mulai": hari_mulai,
        "tanggal_mulai": tanggal_mulai,
        "bulan_mulai": bulan_mulai,
        "tahun_mulai": tahun_mulai,
        
        "hari_selesai": hari_selesai,
        "tanggal_selesai": tanggal_selesai,
        "bulan_selesai": bulan_selesai,
        "tahun_selesai": tahun_selesai,
        
        # DASAR PERJANJIAN
        "point_pertama_pasal_1": point_pertama_pasal_1,
        
        # DATA BIAYA SEWA
        "harga_sewa_rumdis_terbilang": harga_sewa_rumdis_terbilang,
    }
    
    st.write("---")
    if st.button("📄 Generate Surat Perjanjian (Rumah Dinas)", key="btn_generate_rumdis"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian")
        
        # Data Rumah Dinas
        if not alamat_rumdis.strip():
            errors.append("Alamat Rumah Dinas")
        if not kota_rumdis.strip():
            errors.append("Kota Rumah Dinas")
        if not ukuran_meter.strip():
            errors.append("Luas Bangunan")
        
        # Data Pihak Kedua
        if not jenis_badan_usaha:
            errors.append("Jenis Badan Usaha")
        if not nama_perusahaan_pihak_kedua.strip():
            errors.append("Nama Perusahaan")
        if not nama_pihak_kedua.strip():
            errors.append("Nama Penandatangan")
        if not jabatan_pihak_kedua.strip():
            errors.append("Jabatan Penandatangan")
        if not nomor_telepon_pihak_kedua.strip():
            errors.append("Nomor Telepon/HP")
        if not email_pihak_kedua.strip():
            errors.append("Email Perusahaan")
        
        # Durasi Sewa
        if not lama_sewa.strip():
            errors.append("Lama Sewa")
        
        # Dasar Perjanjian
        if not point_pertama_pasal_1.strip():
            errors.append("Point Pertama Pasal 1")
        
        # Data Biaya
        if not harga_sewa_tahunan.strip():
            errors.append("Harga Sewa per Tahun")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return
        
        # ===== CEK DUPLIKASI =====
        collection = get_rumah_dinas_collection()
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

        data_rumdis = {
            "Lokasi": alamat_rumdis_title,
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": nama_pihak_kedua_title,
            "Luas (m²)": ukuran_meter,
            "Tanggal Mulai": tgl_mulai.strftime("%d-%m-%Y"),
            "Tanggal Selesai": tgl_selesai.strftime("%d-%m-%Y"),
            "Biaya Sewa Pertahun": harga_sewa_tahunan,
            "created_at": datetime.utcnow()
        }

        collection.insert_one(data_rumdis)

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