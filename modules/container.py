import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import (
    terbilang_desimal,
    smart_title,
    parse_tanggal_ke_terbilang,
    parse_angka_simple,
    format_display
)
from db import get_container_collection
from datetime import datetime


# ================= HELPER =================
def readonly_input(label, key, value):
    if key not in st.session_state:
        st.session_state[key] = ""
    st.session_state[key] = value
    st.text_input(label, key=key, disabled=True)


# ================= MAIN =================
def run():
    st.header("📦 Perjanjian Kerjasama Container")

    st.markdown("""
    <div style="background-color:#f8f9fa;padding:12px;border-radius:8px;border-left:4px solid #0000ff">
    <strong>📋 Panduan:</strong><br>
    • Isi semua field wajib (*)<br>
    • Data biaya dihitung otomatis
    </div>
    """, unsafe_allow_html=True)

    # ================= TEMPLATE =================
    template_path = "templates/FIKS - (FRITA) PERJANJIAN CONTAINER.docx"
    if not os.path.exists(template_path):
        st.error("Template DOCX tidak ditemukan.")
        return

    doc = DocxTemplate(template_path)

    # ================= INFORMASI DOKUMEN =================
    st.subheader("Informasi Dokumen")

    nama_file = st.text_input(
        "Judul File Dokumen *",
        "SURAT PERJANJIAN KERJASAMA CONTAINER"
    )

    nomor_perjanjian = st.text_input(
        "Nomor Perjanjian *",
        value="SPER/KK/../33000/../20.."
    )
    nomor_perjanjian_upper = nomor_perjanjian.upper()

    tgl_setuju = st.date_input("Tanggal Penandatanganan *")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ================= DATA PENYEWA =================
    st.subheader("Data Penyewa (Pihak Kedua)")

    nama_perusahaan = st.text_input("Nama Perusahaan *")
    jenis_badan_usaha = st.text_area("Jenis Badan Usaha *")
    nama_penyewa = st.text_input("Nama Penyewa *")
    jabatan = st.text_input("Jabatan Penyewa *")
    alamat = st.text_input("Alamat Perusahaan *")
    telepon = st.text_input("Nomor Telepon *")
    email = st.text_input("Email *")

    # ================= DASAR PERJANJIAN =================
    st.subheader("Dasar Perjanjian - Pasal 1")
    point1 = st.text_area("Point Pertama *")
    point2 = st.text_area("Point Kedua *")

    # ================= DATA CONTAINER =================
    st.subheader("Data Sewa Container")

    wilayah = st.text_input("Wilayah *")

    ukuran_feet = st.selectbox(
        "Ukuran Container (Feet) *",
        ["Pilih Ukuran Container", "20", "40"]
    )

    if ukuran_feet == "20":
        ukuran_meter = "14,4"
    elif ukuran_feet == "40":
        ukuran_meter = "28,8"
    else:
        ukuran_meter = ""

    readonly_input(
        "Ukuran Meter Persegi",
        "c_ukuran_meter",
        ukuran_meter
    )

    # ================= DURASI =================
    st.subheader("Durasi & Periode Sewa")

    col1, col2 = st.columns(2)
    with col1:
        lama_sewa = st.text_input("Lama Sewa *")
    with col2:
        satuan_sewa = st.selectbox("Satuan", ["bulan", "tahun"])

    tgl_mulai = st.date_input("Tanggal Mulai Sewa *")
    tgl_selesai = st.date_input("Tanggal Selesai Sewa *")

    # ================= BIAYA =================
    st.subheader("Harga Objek Perjanjian")

    col1, col2 = st.columns(2)
    with col1:
        harga_container_input = st.text_input(
            "Biaya Kontribusi Container per Bulan (Rp) *"
        )
    with col2:
        biaya_sampah_input = st.text_input(
            "Biaya Sampah per Bulan (Rp)",
            value="0"
        )

    # ================= PERHITUNGAN =================
    harga_container = parse_angka_simple(harga_container_input)
    biaya_sampah = parse_angka_simple(biaya_sampah_input)
    lama_sewa_num = parse_angka_simple(lama_sewa)

    lama_sewa_bulan = lama_sewa_num * 12 if satuan_sewa == "tahun" else lama_sewa_num

    total_biaya = (harga_container + biaya_sampah) * lama_sewa_bulan
    total_biaya_display = format_display(str(total_biaya))

    readonly_input(
        "Total Biaya Kontribusi (belum termasuk listrik & air)",
        "c_total_biaya",
        total_biaya_display
    )

    # ================= GENERATE =================
    if st.button("📄 Generate Surat Perjanjian"):
        errors = []

        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian")
        if not nama_perusahaan.strip():
            errors.append("Nama Perusahaan")
        if ukuran_feet == "Pilih Ukuran Container":
            errors.append("Ukuran Container")
        if not harga_container_input.strip():
            errors.append("Biaya Container")
        if not lama_sewa.strip():
            errors.append("Lama Sewa")

        if errors:
            st.error("Harap lengkapi:\n• " + "\n• ".join(errors))
            return

        collection = get_container_collection()
        if collection.find_one({"Nomor Surat Perjanjian": nomor_perjanjian_upper}):
            st.error("Nomor perjanjian sudah terdaftar.")
            return

        context = {
            "nomor_perjanjian": nomor_perjanjian_upper,
            "nama_perusahaan": smart_title(nama_perusahaan),
            "jenis_badan_usaha": jenis_badan_usaha,
            "nama_penyewa": smart_title(nama_penyewa),
            "jabatan": smart_title(jabatan),
            "alamat": alamat,
            "telepon": telepon,
            "email": email,
            "wilayah": smart_title(wilayah),
            "ukuran_feet": ukuran_feet,
            "ukuran_meter": ukuran_meter,
            "lama_sewa": lama_sewa,
            "satuan_sewa": satuan_sewa,
            "total_biaya": total_biaya_display,
            "hari_setuju": hari_setuju,
            "tanggal_setuju": tanggal_setuju,
            "bulan_setuju": bulan_setuju,
            "tahun_setuju": tahun_setuju,
        }

        doc.render(context)
        docx_path = f"{nama_file}.docx"
        doc.save(docx_path)

        collection.insert_one({
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": smart_title(nama_perusahaan),
            "Total Biaya": total_biaya,
            "created_at": datetime.utcnow()
        })

        with open(docx_path, "rb") as f:
            st.download_button("⬇ Download DOCX", f, file_name=docx_path)

        st.success("✅ Surat berhasil dibuat dan disimpan ke database.")


def show():
    run()
