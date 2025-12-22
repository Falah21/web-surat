# surat_kuasa.py
import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import smart_title, parse_tanggal_ke_terbilang

def run():
    st.header("Surat Kuasa")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Pastikan data sesuai dengan dokumen legal/identitas</div>""", unsafe_allow_html=True)
    
    # ====== LOAD TEMPLATE ======
    template_path = "templates/SURAT KUASA.docx"
    if not os.path.exists(template_path):
        st.error(f"Template '{template_path}' tidak ditemukan di folder aplikasi.")
        return

    doc = DocxTemplate(template_path)

    # ====== INFORMASI DOKUMEN ======
    st.subheader("Informasi Dokumen")

    nama_file = st.text_input("Judul File Dokumen *", "SURAT KUASA", key="sk_nama_file")
    docx_path = f"{nama_file}.docx"

    tgl_setuju = st.date_input("Tanggal Pembuatan / Penandatanganan Surat *", key="sk_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    kota_setuju = st.text_input("Kota Penandatanganan *", key="sk_kota_setuju", placeholder="Masukkan kota penandatanganan")

    # ====== DATA PEMBERI KUASA ======
    st.subheader("Data Pemberi Kuasa")

    nama_pemberi_kuasa = st.text_input("Nama Pemberi Kuasa *", key="sk_nama_pemberi", placeholder="Masukkan nama lengkap pemberi kuasa")
    nama_pemberi_kuasa_title = smart_title(nama_pemberi_kuasa)

    ttl_pemberi_kuasa = st.text_input(
        "Tempat, Tanggal Lahir Pemberi Kuasa *",
        placeholder="Contoh: Surabaya, 10 Januari 1999",
        key="sk_ttl_pemberi",
    )

    alamat_pemberi_kuasa = st.text_input("Alamat Pemberi Kuasa *", key="sk_alamat_pemberi", placeholder="Masukkan alamat lengkap pemberi kuasa")

    # ====== DATA PENERIMA KUASA ======
    st.subheader("Data Penerima Kuasa")

    nama_penerima_kuasa = st.text_input("Nama Penerima Kuasa *", key="sk_nama_penerima", placeholder="Masukkan nama lengkap penerima kuasa")
    nama_penerima_kuasa_title = smart_title(nama_penerima_kuasa)

    ttl_penerima_kuasa = st.text_input(
        "Tempat, Tanggal Lahir Penerima Kuasa *",
        placeholder="Contoh: Surabaya, 5 Mei 2000",
        key="sk_ttl_penerima",
    )

    alamat_penerima_kuasa = st.text_input("Alamat Penerima Kuasa *", key="sk_alamat_penerima", placeholder="Masukkan alamat lengkap penerima kuasa")

    # ====== DATA SEWA / OBJEK KUASA ======
    st.subheader("Data Sewa / Objek Kuasa")

    kategori_sewa = st.text_input(
        "Kategori Sewa *",
        placeholder="Contoh: rumah dinas, mess, container, lahan, dll.",
        key="sk_kategori_sewa",
    )

    tgl_sewa = st.date_input("Tanggal Perjanjian Sewa *", key="sk_tgl_sewa")
    hari_sewa, tanggal_sewa, bulan_sewa, tahun_sewa = parse_tanggal_ke_terbilang(tgl_sewa)

    # ====== CONTEXT UNTUK TEMPLATE DOCX ======
    context = {
        # tanggal persetujuan / penandatanganan
        "hari_setuju": hari_setuju,
        "tanggal_setuju": tanggal_setuju,
        "bulan_setuju": bulan_setuju,
        "tahun_setuju": tahun_setuju,
        "kota_setuju": kota_setuju,

        # pihak pemberi kuasa
        "nama_pemberi_kuasa": nama_pemberi_kuasa_title,
        "ttl_pemberi_kuasa": ttl_pemberi_kuasa,
        "alamat_pemberi_kuasa": alamat_pemberi_kuasa,

        # pihak penerima kuasa
        "nama_penerima_kuasa": nama_penerima_kuasa_title,
        "ttl_penerima_kuasa": ttl_penerima_kuasa,
        "alamat_penerima_kuasa": alamat_penerima_kuasa,

        # sewa
        "kategori_sewa": kategori_sewa,
        "hari_sewa": hari_sewa,
        "tanggal_sewa": tanggal_sewa,
        "bulan_sewa": bulan_sewa,
        "tahun_sewa": tahun_sewa,
    }

    st.write("---")
    if st.button("📄 Generate Surat Kuasa", key="sk_btn_generate"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not kota_setuju.strip():
            errors.append("Kota Penandatanganan")
        
        # Data Pemberi Kuasa
        if not nama_pemberi_kuasa.strip():
            errors.append("Nama Pemberi Kuasa")
        if not ttl_pemberi_kuasa.strip():
            errors.append("Tempat, Tanggal Lahir Pemberi Kuasa")
        if not alamat_pemberi_kuasa.strip():
            errors.append("Alamat Pemberi Kuasa")
        
        # Data Penerima Kuasa
        if not nama_penerima_kuasa.strip():
            errors.append("Nama Penerima Kuasa")
        if not ttl_penerima_kuasa.strip():
            errors.append("Tempat, Tanggal Lahir Penerima Kuasa")
        if not alamat_penerima_kuasa.strip():
            errors.append("Alamat Penerima Kuasa")
        
        # Data Sewa/Objek Kuasa
        if not kategori_sewa.strip():
            errors.append("Kategori Sewa")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return
        
        try:
            doc.render(context)
            doc.save(docx_path)
            with open(docx_path, "rb") as f:
                st.download_button(
                    "⬇ Download DOCX",
                    f,
                    file_name=f"{nama_file}.docx",
                    key="sk_dl_docx",
                )
            st.success("Surat kuasa berhasil dibuat!")
        except Exception as e:

            st.error(f"Terjadi kesalahan saat membuat dokumen: {e}")

def show():
    """Fungsi utama untuk ditampilkan di aplikasi Streamlit"""
    run()
