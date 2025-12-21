# mess_page.py
import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import terbilang_desimal, smart_title, parse_tanggal_ke_terbilang, format_rupiah_terbilang
from db import get_mess_collection
from datetime import datetime

def run():
    st.header("Perjanjian Sewa Mess Menanggal")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Pastikan data sesuai dengan dokumen identitas</div>""", unsafe_allow_html=True)

    template_path = "templates/FIKS - (FRITA) PERJANJIAN KONTRIBUSI MESS MENANGGAL.docx"
    if not os.path.exists(template_path):
        st.error(f"Template '{template_path}' tidak ditemukan di folder aplikasi.")
        return
    doc = DocxTemplate(template_path)

    # ====== INFORMASI DOKUMEN ======
    st.subheader("Informasi Dokumen")
    
    nama_file = st.text_input("Judul File Dokumen *", "SURAT PERJANJIAN SEWA MESS", key="m_nama_file")
    docx_path = f"{nama_file}.docx"
    
    nomor_perjanjian = st.text_input("Nomor Perjanjian (SPER) *", key="m_nomor_perjanjian", placeholder="Masukkan nomor perjanjian/SPER", value="SPER/MM/../33000/../20..")
    nomor_perjanjian_upper = (nomor_perjanjian or "").upper()
    
    tgl_setuju = st.date_input("Tanggal Penandatanganan Surat *", key="m_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ====== DATA PENYEWA (PIHAK KEDUA) ======
    st.subheader("Data Penyewa (Pihak Kedua)")
    
    nama_pihak_kedua = st.text_input("Nama Penyewa *", key="m_nama_pihak", placeholder="Masukkan nama lengkap penyewa")
    nama_pihak_kedua_title = smart_title(nama_pihak_kedua)
    nama_pihak_kedua_upper = (nama_pihak_kedua or "").upper()

    nip_pihak_kedua = st.text_input("NIP *", key="m_nip", placeholder="Masukkan NIP penyewa")
    
    pekerjaan_pihak_kedua = st.text_input("Pekerjaan *", key="m_pekerjaan", placeholder="Masukkan pekerjaan/jabatan")
    pekerjaan_pihak_kedua_title = smart_title(pekerjaan_pihak_kedua)
    pekerjaan_pihak_kedua_upper = (pekerjaan_pihak_kedua or "").upper()

    divisi_pihak_kedua = st.text_input("Divisi *", key="m_divisi", placeholder="Masukkan divisi/bagian")
    divisi_pihak_kedua_title = smart_title(divisi_pihak_kedua)
    divisi_pihak_kedua_upper = (divisi_pihak_kedua or "").upper()

    # tempat_pekerjaan_pihak_kedua = st.text_input("Tempat Pekerjaan *", key="m_tempat", placeholder="Contoh: PT PAL Indonesia (Persero)")
    # tempat_pekerjaan_pihak_kedua_title = smart_title(tempat_pekerjaan_pihak_kedua)

    alamat_pihak_kedua = st.text_input("Alamat *", key="m_alamat", placeholder="Masukkan alamat lengkap penyewa")
    alamat_pihak_kedua_title = smart_title(alamat_pihak_kedua)

    nomor_telepon_pihak_kedua = st.text_input("Nomor HP/WA *", key="m_telepon", placeholder="Masukkan nomor telepon aktif")
    email_pihak_kedua = st.text_input("Email *", key="m_email", placeholder="Masukkan email aktif")

    # ====== DATA MESS YANG DISEWA ======
    st.subheader("Data Mess yang Disewa")
    
    nomor_blok = st.text_input("Nomor Blok Mess *", key="m_blok", placeholder="Contoh: 67/D1")

    # ====== DASAR PERJANJIAN ======
    st.subheader("Dasar Perjanjian - Pasal 1")
    st.caption("Isi dasar perjanjian dibawah ini dengan benar")
    
    point_pertama_pasal_1 = st.text_area("Point Pertama *", key="m_point1", placeholder="Masukkan point pertama pasal 1 mengenai Dasar Perjanjian")
    point_kedua_pasal_1 = st.text_area("Point Kedua *", key="m_point2", placeholder="Masukkan point kedua pasal 1 mengenai Dasar Perjanjian")

    # ====== DURASI DAN PERIODE SEWA ======
    st.subheader("Durasi dan Periode Sewa")
    
    col1, col2 = st.columns(2)

    with col1:
        lama_sewa = st.text_input(
            "Lama Sewa *",
            key="m_lama_sewa",
            placeholder="Contoh: 12"
        )

    with col2:
        satuan_sewa = st.selectbox(
            "Satuan",
            ["bulan", "tahun"],
            key="m_satuan_sewa"
        )
    
    lama_sewa_display = ""

    if lama_sewa:
        terbilang_raw = terbilang_desimal(lama_sewa)

        if "(" in terbilang_raw and ")" in terbilang_raw:
            terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip()
        else:
            terbilang_only = terbilang_raw

        lama_sewa_display = f"{lama_sewa} ({terbilang_only}) {satuan_sewa}"

    tgl_mulai = st.date_input("Tanggal Mulai Sewa *", key="m_tgl_mulai")
    hari_mulai, tanggal_mulai, bulan_mulai, tahun_mulai = parse_tanggal_ke_terbilang(tgl_mulai)

    tgl_selesai = st.date_input("Tanggal Selesai Sewa *", key="m_tgl_selesai")
    hari_selesai, tanggal_selesai, bulan_selesai, tahun_selesai = parse_tanggal_ke_terbilang(tgl_selesai)

    # Harga Mess
    harga_mess_input = st.text_input("Harga Sewa Mess per Periode *",key="m_harga_mess",placeholder="Contoh: 350000")
    harga_mess_display = format_rupiah_terbilang(harga_mess_input)

    context = {
        # INFORMASI DOKUMEN
        "nomor_perjanjian": nomor_perjanjian,
        "nomor_perjanjian_upper": nomor_perjanjian_upper,
        "hari_setuju": hari_setuju,
        "tanggal_setuju": tanggal_setuju,
        "bulan_setuju": bulan_setuju,
        "tahun_setuju": tahun_setuju,

        # DATA PENYEWA
        "nama_pihak_kedua_title": nama_pihak_kedua_title,
        "nama_pihak_kedua_upper": nama_pihak_kedua_upper,
        "nip_pihak_kedua": nip_pihak_kedua,
        "pekerjaan_pihak_kedua_title": pekerjaan_pihak_kedua_title,
        "pekerjaan_pihak_kedua_upper": pekerjaan_pihak_kedua_upper,        
        "divisi_pihak_kedua_title": divisi_pihak_kedua_title,
        "divisi_pihak_kedua_upper": divisi_pihak_kedua_upper,
        # "tempat_pekerjaan_pihak_kedua": tempat_pekerjaan_pihak_kedua,
        "alamat_pihak_kedua_title": alamat_pihak_kedua_title,
        "nomor_telepon_pihak_kedua": nomor_telepon_pihak_kedua,
        "email_pihak_kedua": email_pihak_kedua,

        # DATA MESS
        "nomor_blok": nomor_blok,

        # DASAR PERJANJIAN
        "point_pertama_pasal_1": point_pertama_pasal_1,
        "point_kedua_pasal_1": point_kedua_pasal_1,

        # DURASI SEWA
        "lama_sewa_terbilang": lama_sewa_display,
        "hari_mulai": hari_mulai,
        "tanggal_mulai": tanggal_mulai,
        "bulan_mulai": bulan_mulai,
        "tahun_mulai": tahun_mulai,
        "hari_selesai": hari_selesai,
        "tanggal_selesai": tanggal_selesai,
        "bulan_selesai": bulan_selesai,
        "tahun_selesai": tahun_selesai,

        "harga_mess": harga_mess_display,
    }


    st.write("---")
    if st.button("📄 Generate Surat Perjanjian (Mess)", key="btn_generate_mess"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian (SPER)")
        
        # Data Penyewa
        if not nama_pihak_kedua.strip():
            errors.append("Nama Penyewa")
        if not nip_pihak_kedua.strip():
            errors.append("NIP")
        if not pekerjaan_pihak_kedua.strip():
            errors.append("Pekerjaan")
        if not divisi_pihak_kedua.strip():
            errors.append("Divisi")
        # if not tempat_pekerjaan_pihak_kedua.strip():
        #     errors.append("Tempat Pekerjaan")
        if not alamat_pihak_kedua.strip():
            errors.append("Alamat")
        if not nomor_telepon_pihak_kedua.strip():
            errors.append("Nomor HP/WA")
        if not email_pihak_kedua.strip():
            errors.append("Email")
        
        # Data Mess
        if not nomor_blok.strip():
            errors.append("Nomor Blok Mess")
        
        # Dasar Perjanjian
        if not point_pertama_pasal_1.strip():
            errors.append("Point Pertama Pasal 1")
        if not point_kedua_pasal_1.strip():
            errors.append("Point Kedua Pasal 1")
        
        # Durasi Sewa
        if not lama_sewa.strip():
            errors.append("Lama Sewa (bulan)")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return
        
        # ===== CEK DUPLIKASI =====
        collection = get_mess_collection()
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

        lokasi_mess = "Jl Cipta Menanggal Tengah / Pagesangan Blok " + nomor_blok
        biaya_sewa = int(harga_mess_input.replace(".", "").replace(",", ""))
        
        data_mess = {
            "Lokasi": lokasi_mess,
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": nama_pihak_kedua_title,
            "NIP": nip_pihak_kedua,
            "Unit Kerja": divisi_pihak_kedua_title,
            "Tanggal Mulai": tgl_mulai.strftime("%d-%m-%Y"),
            "Tanggal Selesai": tgl_selesai.strftime("%d-%m-%Y"),
            "Biaya Sewa Perbulan": biaya_sewa,
            "created_at": datetime.utcnow()
        }

        collection.insert_one(data_mess)

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