import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import terbilang_desimal, smart_title, parse_tanggal_ke_terbilang, parse_angka_simple, format_display
from db import get_container_collection
from datetime import datetime

def run():
    st.header("📦 Perjanjian Kerjasama Container")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Data biaya akan dihitung otomatis</div>""", unsafe_allow_html=True)
    
    template_path = "templates/FIKS - (FRITA) PERJANJIAN CONTAINER.docx"
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
    nama_file = st.text_input("Judul File Dokumen *", "SURAT PERJANJIAN KERJASAMA CONTAINER", key="c_nama_file")
    docx_path = f"{nama_file}.docx"

    nomor_perjanjian = st.text_input("Nomor Perjanjian *", key="c_nomor_perjanjian", placeholder="Masukkan nomor perjanjian/SPER", value="SPER/KK/../33000/../20..")
    nomor_perjanjian_upper = (nomor_perjanjian or "").upper()
    
    tgl_setuju = st.date_input("Tanggal Penandatanganan Surat *", key="c_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ====== DATA PENYEWA (PIHAK KEDUA) ======
    st.subheader("Data Penyewa (Pihak Kedua)")
    nama_perusahaan_pihak_kedua = st.text_input("Nama Perusahaan *", key="c_nama_perusahaan", placeholder="Masukkan nama perusahaan")
    nama_perusahaan_pihak_kedua_upper = (nama_perusahaan_pihak_kedua or "").upper()
    nama_perusahaan_pihak_kedua_title = smart_title(nama_perusahaan_pihak_kedua)

    jenis_badan_usaha = st.text_area("Jenis Badan Usaha Perusahaan *", key="c_jenis_perusahaan", placeholder="Jelaskan jenis badan usaha perusahaan") 

    nama_pihak_kedua = st.text_input("Nama Penyewa *", key="c_nama_pihak", placeholder="Masukkan nama lengkap penyewa beserta gelar")
    nama_pihak_kedua_upper = (nama_pihak_kedua or "").upper()
    nama_pihak_kedua_title = smart_title(nama_pihak_kedua)

    jabatan_pihak_kedua = st.text_input("Jabatan Penyewa *", key="c_jabatan", placeholder="Contoh: Direktur Utama")
    jabatan_pihak_kedua_upper = (jabatan_pihak_kedua or "").upper()
    jabatan_pihak_kedua_title = smart_title(jabatan_pihak_kedua)

    alamat_pihak_kedua = st.text_input("Alamat Perusahaan *", key="c_alamat", placeholder="Masukkan alamat lengkap perusahaan")
    alamat_pihak_kedua_title = smart_title(alamat_pihak_kedua)

    nomor_telepon_pihak_kedua = st.text_input("Nomor Telepon Penyewa/Perusahaan *", key="c_telepon", placeholder="Masukkan nomor telepon")
    email_pihak_kedua = st.text_input("Email Perusahaan *", key="c_email", placeholder="Masukkan email perusahaan")

    # ====== DASAR PERJANJIAN (DINAMIS) ======
    st.subheader("Dasar Perjanjian - Pasal 1")
    st.caption("Klik tambah jika ingin menambah dasar perjanjian")
    
    # simpan ke session_state
    if "dasar_perjanjian" not in st.session_state:
        st.session_state.dasar_perjanjian = [""]
    
    # render input
    for i, val in enumerate(st.session_state.dasar_perjanjian):
        st.text_area(
            f"Dasar Perjanjian {i+1}",
            key=f"dasar_{i}",
            height=80
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Tambah Point"):
            st.session_state.dasar_perjanjian.append("")
            st.rerun()
    
    with col2:
        if len(st.session_state.dasar_perjanjian) > 1:
            if st.button("➖ Hapus Point Terakhir"):
                st.session_state.dasar_perjanjian.pop()
                st.rerun()
    
    # ====== FORMAT DASAR PERJANJIAN (INI KUNCI UTAMA) ======
    dasar_perjanjian_list = [
        st.session_state[f"dasar_{i}"].strip()
        for i in range(len(st.session_state.dasar_perjanjian))
        if st.session_state.get(f"dasar_{i}", "").strip()
    ]
    
    dasar_perjanjian_text = "\n".join(
        f"({i+1}).    {p}."
        for i, p in enumerate(dasar_perjanjian_list)
    )

    # ====== DATA SEWA CONTAINER ======
    st.subheader("Data Sewa Container")
    wilayah = st.text_input("Wilayah *", key="c_wilayah", placeholder="Contoh: Barat Dock Beluga")
    wilayah_upper = (wilayah or "").upper()
    wilayah_title = smart_title(wilayah)

    # Dropdown untuk ukuran container dalam feet
    ukuran_options = ["Pilih Ukuran Container", "20", "40"]
    ukuran_feet = st.selectbox("Ukuran (dalam feet) *", ukuran_options, key="c_ukuran")
    
    # Otomatis isi ukuran meter berdasarkan pilihan feet
    if ukuran_feet == "20":
        ukuran_meter = "14,4"
        ukuran_meter_num = 14.4
    elif ukuran_feet == "40":
        ukuran_meter = "28,8"
        ukuran_meter_num = 28.8
    else:
        ukuran_meter = ""
        ukuran_meter_num = 0

    # Tampilkan ukuran meter (read-only)
    # st.text_input("Ukuran meter persegi", value=ukuran_meter, key="c_ukuran_meter", disabled=True)


    if "c_ukuran_meter" not in st.session_state:
        st.session_state["c_ukuran_meter"] = "" 
    if ukuran_feet == "20":
        st.session_state["c_ukuran_meter"] = "14,4"
    elif ukuran_feet == "40":
        st.session_state["c_ukuran_meter"] = "28,8"
    else:
        st.session_state["c_ukuran_meter"] = ""
    
    st.text_input(
        "Ukuran meter persegi",
        key="c_ukuran_meter",
        disabled=True
    )

    # FORMAT UKURAN FEET:
    # 1. ukuran_feet: hanya angka
    ukuran_feet_angka = ukuran_feet if ukuran_feet != "Pilih Ukuran Container" else ""
    
    # 2. ukuran_feet_terbilang: angka + terbilang
    ukuran_feet_terbilang = ""
    if ukuran_feet and ukuran_feet != "Pilih Ukuran Container":
        terbilang_raw = terbilang_desimal(ukuran_feet)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        ukuran_feet_terbilang = f"{ukuran_feet} ({terbilang_only})"

    # FORMAT UKURAN METER:
    # 3. ukuran_meter: hanya angka
    ukuran_meter_angka = ukuran_meter
    
    # 4. ukuran_meter_terbilang: angka + terbilang
    ukuran_meter_terbilang = ""
    if ukuran_meter:
        terbilang_raw = terbilang_desimal(ukuran_meter.replace(",", "."))
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        ukuran_meter_terbilang = f"{ukuran_meter} ({terbilang_only})"

    # ====== FORMAT UKURAN LAHAN ======
    # Format ukuran_meter2: "285 m² (dua ratus delapan puluh lima meter persegi)"
    ukuran_meter2_display = ""
    if ukuran_meter:
        # Ambil hanya bagian integer
        try:
            meter_int = int(float(ukuran_meter))
            terbilang_raw = terbilang_desimal(str(meter_int))
            terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
            ukuran_meter2_display = f"{meter_int} m² ({terbilang_only} meter persegi)"
        except:
            ukuran_meter2_display = f"{ukuran_meter} m² ({terbilang_only} meter persegi)"

    # ====== DURASI SEWA ======
    st.subheader("Durasi dan Periode Sewa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        lama_sewa = st.text_input("Lama Sewa *", key="c_lama_sewa", placeholder="Contoh: 12")
    
    with col2:
        satuan_sewa = st.selectbox("Satuan", ["bulan", "tahun"], key="c_satuan_sewa", index=0)
    
    # FORMAT LAMA SEWA:
    # 1. lama_sewa: hanya angka
    lama_sewa_angka = lama_sewa
    
    # 2. lama_sewa_terbilang: angka + terbilang + satuan
    lama_sewa_terbilang = ""
    if lama_sewa:
        terbilang_raw = terbilang_desimal(lama_sewa)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        lama_sewa_terbilang = f"{lama_sewa} ({terbilang_only}) {satuan_sewa}"

    # ====== PERIODE SEWA ======
    st.subheader("Periode Sewa")
    tgl_mulai = st.date_input("Tanggal Mulai Sewa *", key="c_tgl_mulai")
    hari_mulai, tanggal_mulai, bulan_mulai, tahun_mulai = parse_tanggal_ke_terbilang(tgl_mulai)

    tgl_selesai = st.date_input("Tanggal Selesai Sewa *", key="c_tgl_selesai")
    hari_selesai, tanggal_selesai, bulan_selesai, tahun_selesai = parse_tanggal_ke_terbilang(tgl_selesai)

    # ====== DATA BIAYA - INPUT LANGSUNG ======
    st.subheader("Harga Objek Perjanjian")
    
    col1, col2 = st.columns(2)
    with col1:
        harga_container_perbulan_input = st.text_input("Biaya Kontribusi Container per Bulan (Rp) *", key="c_harga_container", placeholder="Contoh: 1440000")
    with col2:
        biaya_sampah_input = st.text_input("Biaya Sampah per Bulan (Rp)", key="c_biaya_sampah", placeholder="Contoh: 50000")

    # ====== PERHITUNGAN OTOMATIS ======
    st.subheader("Total Biaya Kontribusi")
    
    # Konversi ukuran meter untuk perhitungan
    def parse_meter_value(meter_str):
        try:
            return float(meter_str.replace(',', '.'))
        except:
            return 0

    ukuran_meter_calc = parse_meter_value(ukuran_meter) if ukuran_meter else 0
    
    # Hitung nilai-nilai
    harga_container_num = parse_angka_simple(harga_container_perbulan_input)
    biaya_sampah_num = parse_angka_simple(biaya_sampah_input)
    lama_sewa_num = parse_angka_simple(lama_sewa)
    
    # Jika satuan tahun, konversi ke bulan untuk perhitungan
    if satuan_sewa == "tahun":
        lama_sewa_bulan = lama_sewa_num * 12
    else:
        lama_sewa_bulan = lama_sewa_num
    
    # Perhitungan
    biaya_total_perbulan = harga_container_num
    total_biaya_kontribusi = (biaya_total_perbulan * lama_sewa_bulan) + (biaya_sampah_num * lama_sewa_bulan)
    
    # Format semua biaya
    harga_container_display = format_display(harga_container_perbulan_input, harga_container_num)
    biaya_sampah_display = format_display(biaya_sampah_input, biaya_sampah_num)
    biaya_total_perbulan_display = format_display(str(biaya_total_perbulan))
    total_biaya_kontribusi_display = format_display(str(total_biaya_kontribusi))
    
    # Tampilkan total
    # st.text_input("Total Biaya Kontribusi (belum termasuk biaya fasilitas listrik dan air)", value=total_biaya_kontribusi_display, key="c_total_biaya", disabled=True)

    # ====== SESSION STATE: TOTAL BIAYA ======
    if "c_total_biaya" not in st.session_state:
        st.session_state["c_total_biaya"] = ""
    
    st.session_state["c_total_biaya"] = total_biaya_kontribusi_display
    
    st.text_input(
        "Total Biaya Kontribusi (belum termasuk biaya fasilitas listrik dan air)",
        key="c_total_biaya",
        disabled=True
    )

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

        # DASAR PERJANJIAN
        "dasar_perjanjian": dasar_perjanjian_text,

        # DATA WILAYAH
        "wilayah": wilayah,
        "wilayah_upper": wilayah_upper,
        "wilayah_title": wilayah_title,

        # DATA UKURAN - SEMUA VARIASI
        "ukuran_feet": ukuran_feet_angka,               # hanya angka
        "ukuran_feet_terbilang": ukuran_feet_terbilang, # angka + terbilang
        "ukuran_meter": ukuran_meter_angka,             # hanya angka
        "ukuran_meter_terbilang": ukuran_meter_terbilang, # angka + terbilang
        "ukuran_meter2": ukuran_meter2_display,

        # DURASI SEWA - SEMUA VARIASI
        "lama_sewa": lama_sewa_angka,                   # hanya angka
        "lama_sewa_terbilang": lama_sewa_terbilang,     # angka + terbilang + satuan
        "satuan_sewa": satuan_sewa,                     # hanya satuan
        "hari_mulai": hari_mulai,
        "tanggal_mulai": tanggal_mulai,
        "bulan_mulai": bulan_mulai,
        "tahun_mulai": tahun_mulai,
        "hari_selesai": hari_selesai,
        "tanggal_selesai": tanggal_selesai,
        "bulan_selesai": bulan_selesai,
        "tahun_selesai": tahun_selesai,

        # DATA BIAYA
        "harga_container": harga_container_display,
        "biaya_sampah": biaya_sampah_display,
        "biaya_total_perbulan": biaya_total_perbulan_display,
        "total_biaya_kontribusi": total_biaya_kontribusi_display,
    }
    
    st.write("---")
    if st.button("📄 Generate Surat Perjanjian (Container)", key="btn_generate_container"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian")
        
        # Data Penyewa
        if not nama_perusahaan_pihak_kedua.strip():
            errors.append("Nama Perusahaan")
        if not nama_pihak_kedua.strip():
            errors.append("Nama Penyewa")
        if not jabatan_pihak_kedua.strip():
            errors.append("Jabatan Penyewa")
        if not alamat_pihak_kedua.strip():
            errors.append("Alamat Perusahaan")
        if not nomor_telepon_pihak_kedua.strip():
            errors.append("Nomor Telepon")
        if not email_pihak_kedua.strip():
            errors.append("Email Perusahaan")
        
        # Data Container
        if not wilayah.strip():
            errors.append("Wilayah")
        if ukuran_feet == "Pilih Ukuran Container":
            errors.append("Ukuran Container")
        
        # Dasar Perjanjian
        if not dasar_perjanjian_list:
            error.append("Minimal 1 dasar perjanjian harus diisi")
        
        # Data Biaya
        if not harga_container_perbulan_input.strip():
            errors.append("Biaya Kontribusi Container per Bulan")
        
        # Durasi Sewa
        if not lama_sewa.strip():
            errors.append("Lama Sewa")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return
        
        # ===== CEK DUPLIKASI =====
        collection = get_container_collection()
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
        data_container = {
            "Lokasi": wilayah_title,
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": nama_perusahaan_pihak_kedua_title,
            "Volume (Feet)": ukuran_feet_angka,
            "Luas (m²)": ukuran_meter_angka,
            "Tanggal Mulai": tgl_mulai.strftime("%d-%m-%Y"),
            "Tanggal Selesai": tgl_selesai.strftime("%d-%m-%Y"),
            "Biaya Sewa Perbulan": biaya_total_perbulan,
            "created_at": datetime.utcnow()
        }

        collection.insert_one(data_container)

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



