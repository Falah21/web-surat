import os
import streamlit as st
from docxtpl import DocxTemplate
from helpers import terbilang_desimal, smart_title, parse_tanggal_ke_terbilang, parse_angka_simple, format_display
from db import get_lahan_collection
from datetime import datetime

def run():
    st.header("🌱 Perjanjian Kerjasama Lahan")
    st.markdown("""<div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #0000ff;">
    <strong>📋 Panduan Pengisian Form:</strong><br>
    1. Isi semua data pada form di bawah<br>
    2. Field dengan tanda <span style="color: #ff4b4b;">*</span> wajib diisi<br>
    3. Data biaya akan dihitung otomatis</div>""", unsafe_allow_html=True)
    
    template_path = "templates/FIKS - (FRITA) PERJANJIAN LAHAN.docx"
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
    nama_file = st.text_input("Judul File Dokumen *", "SURAT PERJANJIAN KERJASAMA LAHAN", key="l_nama_file")
    docx_path = f"{nama_file}.docx"

    nomor_perjanjian = st.text_input("Nomor Perjanjian *", key="l_nomor_perjanjian", 
                                     value="SPER/KK/../34000/../20..",
                                     placeholder="Masukkan nomor perjanjian/SPER")
    nomor_perjanjian_upper = (nomor_perjanjian or "").upper()
    
    tgl_setuju = st.date_input("Tanggal Penandatanganan Surat *", key="l_tgl_setuju")
    hari_setuju, tanggal_setuju, bulan_setuju, tahun_setuju = parse_tanggal_ke_terbilang(tgl_setuju)

    # ====== DATA PIHAK KEDUA ======
    st.subheader("Data Perusahaan Pihak Kedua")
    # col1, col2 = st.columns(2)
    # with col1:
    #     jenis_badan_usaha = st.selectbox(
    #         "Jenis Badan Usaha *",
    #         ["PT", "CV", "UD", "Firma", "Perseroan Terbatas", "Perusahaan Perorangan"],
    #         key="l_jenis_badan_usaha"
    #     )
    # with col2:
    #     nama_perusahaan_pihak_kedua = st.text_input("Nama Perusahaan *", key="l_nama_perusahaan", 
    #                                                 placeholder="Masukkan nama perusahaan")
    nama_perusahaan_pihak_kedua = st.text_input("Nama Perusahaan *", key="l_nama_perusahaan", placeholder="Masukkan nama perusahaan") 
    nama_perusahaan_pihak_kedua_upper = (nama_perusahaan_pihak_kedua or "").upper()
    nama_perusahaan_pihak_kedua_title = smart_title(nama_perusahaan_pihak_kedua)

    jenis_badan_usaha = st.text_area("Jenis Badan Usaha Perusahaan *", key="l_jenis_perusahaan", placeholder="Jelaskan jenis badan usaha perusahaan") 
    
    nama_proyek = st.text_area("Nama Proyek *", key="l_nama_proyek", placeholder="Masukkan nama proyek")
    nama_proyek_upper = (nama_proyek or "").upper()
    nama_proyek_title = smart_title(nama_proyek)

    nama_pihak_kedua = st.text_input("Nama Penandatangan *", key="l_nama_pihak", placeholder="Masukkan nama lengkap penandatangan beserta gelar")
    nama_pihak_kedua_upper = (nama_pihak_kedua or "").upper()
    nama_pihak_kedua_title = smart_title(nama_pihak_kedua)

    jabatan_pihak_kedua = st.text_input("Jabatan Penandatangan *", key="l_jabatan", placeholder="Contoh: Direktur Utama, Manager Proyek")
    jabatan_pihak_kedua_upper = (jabatan_pihak_kedua or "").upper()
    jabatan_pihak_kedua_title = smart_title(jabatan_pihak_kedua)

    alamat_perusahaan_pihak_kedua = st.text_input("Alamat Perusahaan *", key="l_alamat", placeholder="Masukkan alamat lengkap perusahaan")
    alamat_perusahaan_pihak_kedua_title = smart_title(alamat_perusahaan_pihak_kedua)
    
    nomor_telepon_pihak_kedua = st.text_input("Nomor Telepon/HP/WA *", key="l_telepon", placeholder="Masukkan nomor telepon")
    email_pihak_kedua = st.text_input("Email Perusahaan *", key="l_email", placeholder="Masukkan email perusahaan")

    # ====== DATA LAHAN ======
    st.subheader("Data Lahan")
    
    wilayah = st.text_input("Wilayah Lahan *", key="l_wilayah", placeholder="Contoh: Divisi Rekayasa Umum")
    wilayah_upper = (wilayah or "").upper()
    wilayah_title = smart_title(wilayah)
    
    col1, col2 = st.columns(2)
    with col1:
        ukuran_meter = st.text_input("Ukuran Lahan (m²) *", key="l_ukuran_meter", placeholder="Contoh: 235")
    with col2:
        lama_sewa = st.text_input("Lama Sewa *", key="l_lama_sewa", placeholder="Contoh: 12")
    
    satuan_sewa = st.selectbox("Satuan Sewa", ["bulan", "tahun"], key="l_satuan_sewa", index=0)
    
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
            ukuran_meter2_display = f"{ukuran_meter} m²"
    
    # ====== FORMAT LAMA SEWA ======
    lama_sewa_angka = lama_sewa
    lama_sewa_terbilang = ""
    if lama_sewa:
        terbilang_raw = terbilang_desimal(lama_sewa)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        lama_sewa_terbilang = f"{lama_sewa} ({terbilang_only}) {satuan_sewa}"

    # ====== PERIODE SEWA ======
    st.subheader("Periode Sewa")
    
    tgl_mulai = st.date_input("Tanggal Mulai Sewa *", key="l_tgl_mulai")
    hari_mulai, tanggal_mulai, bulan_mulai, tahun_mulai = parse_tanggal_ke_terbilang(tgl_mulai)

    tgl_selesai = st.date_input("Tanggal Selesai Sewa *", key="l_tgl_selesai")
    hari_selesai, tanggal_selesai, bulan_selesai, tahun_selesai = parse_tanggal_ke_terbilang(tgl_selesai)

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
            if st.button("➖ Hapus Point"):
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

    # ====== DATA BIAYA ======
    st.subheader("Data Biaya")
    
    col1, col2 = st.columns(2)
    with col1:
        harga_dasar_lahan = st.text_input("Harga Dasar Lahan per m² per Bulan (Rp) *", key="l_harga_dasar_lahan", placeholder="Contoh: 50000")
    with col2:
        biaya_kontribusi_sampah = st.text_input("Biaya Kontribusi Sampah per Bulan (Rp) *", key="l_biaya_sampah", placeholder="Contoh: 50000")
    
    angka_ppn = st.text_input("Persentase PPN (%)", key="l_ppn", value="11")

    # ====== PERHITUNGAN TERMIN ======
    st.subheader("Pembayaran Termin")
    
    termin = st.selectbox("Jumlah Termin", ["1", "2", "3"], key="l_termin", index=2)
    
    bulan_termin_1 = st.text_input("Termin I (Bulan)", key="l_termin1", 
                                   placeholder="Contoh: Januari-Maret 2024") 
                                #    value="Januari-Maret 2024")
    bulan_termin_2 = st.text_input("Termin II (Bulan)", key="l_termin2", 
                                   placeholder="Contoh: April-Juni 2024") 
                                #    value="April-Juni 2024")
    bulan_termin_3 = st.text_input("Termin III (Bulan)", key="l_termin3", 
                                   placeholder="Contoh: Juli-September 2024")
                                #    value="Juli-September 2024")

    # ====== PERHITUNGAN OTOMATIS ======
    st.subheader("Perhitungan Otomatis")
    
    # Parsing angka
    ukuran_meter_num = parse_angka_simple(ukuran_meter)
    harga_dasar_lahan_num = parse_angka_simple(harga_dasar_lahan)
    biaya_sampah_num = parse_angka_simple(biaya_kontribusi_sampah)
    ppn_num = parse_angka_simple(angka_ppn) / 100 if angka_ppn else 0.11  # default 11%
    
    # Perhitungan
    total_harga_lahan = ukuran_meter_num * harga_dasar_lahan_num
    total_harga_setelah_ppn = total_harga_lahan * (1 + ppn_num)
    
    total_biaya_sampah = biaya_sampah_num
    total_biaya_sampah_setelah_ppn = biaya_sampah_num * (1 + ppn_num)
    
    total_biaya_kontribusi = total_harga_setelah_ppn + total_biaya_sampah_setelah_ppn
    
    # Format untuk display
    # Fungsi untuk format angka dengan titik
    def format_titik(value):
        try:
            num = parse_angka_simple(value)
            return f"{num:,.0f}".replace(",", ".")
        except:
            return "0"
    # Format untuk display
    harga_dasar_lahan_angka_formatted = format_titik(harga_dasar_lahan)
    harga_dasar_lahan_display = format_display(harga_dasar_lahan, harga_dasar_lahan_num)
    total_harga_lahan_display = format_display(str(total_harga_lahan))
    total_harga_setelah_ppn_display = format_display(str(int(total_harga_setelah_ppn)))
    biaya_kontribusi_sampah_display = format_display(biaya_kontribusi_sampah, biaya_sampah_num)
    total_biaya_sampah_setelah_ppn_display = format_display(str(int(total_biaya_sampah_setelah_ppn)))
    total_biaya_kontribusi_display = format_display(str(int(total_biaya_kontribusi)))
    
    # Format termin
    termin_terbilang = ""
    if termin:
        terbilang_raw = terbilang_desimal(termin)
        terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip() if "(" in terbilang_raw else terbilang_raw
        termin_terbilang = f"{termin} ({terbilang_only})"
    
    # # Tampilkan hasil perhitungan
    # st.info(f"**Total Harga Lahan per Bulan:** {total_harga_lahan_display}")
    # st.info(f"**Total Harga Lahan setelah PPN:** {total_harga_setelah_ppn_display}")
    # st.info(f"**Biaya Sampah setelah PPN:** {total_biaya_sampah_setelah_ppn_display}")
    # st.success(f"**Total Biaya Kontribusi per Bulan:** {total_biaya_kontribusi_display}")

    # Tampilkan total
    # st.text_input("Total Harga Lahan setelah PPN:", value=total_harga_setelah_ppn_display, key="l_harga_setelah_ppn", disabled=True)
    # st.text_input("Total Biaya Sampah setelah PPN:", value=total_biaya_sampah_setelah_ppn_display, key="l_sampah_setelah_ppn", disabled=True)
    # st.text_input("Total Biaya Kontribusi per Bulan:", value=total_biaya_kontribusi_display, key="l_biaya_kontribusi", disabled=True)

    # ====== SESSION STATE: TOTAL HARGA LAHAN SETELAH PPN ======
    if "l_harga_setelah_ppn" not in st.session_state:
        st.session_state["l_harga_setelah_ppn"] = ""
    
    st.session_state["l_harga_setelah_ppn"] = total_harga_setelah_ppn_display
    
    st.text_input("Total Harga Lahan setelah PPN:", key="l_harga_setelah_ppn", disabled=True)
    
    
    # ====== SESSION STATE: TOTAL BIAYA SAMPAH SETELAH PPN ======
    if "l_sampah_setelah_ppn" not in st.session_state:
        st.session_state["l_sampah_setelah_ppn"] = ""
    
    st.session_state["l_sampah_setelah_ppn"] = total_biaya_sampah_setelah_ppn_display
    
    st.text_input("Total Biaya Sampah setelah PPN:", key="l_sampah_setelah_ppn", disabled=True)
    
    
    # ====== SESSION STATE: TOTAL BIAYA KONTRIBUSI ======
    if "l_biaya_kontribusi" not in st.session_state:
        st.session_state["l_biaya_kontribusi"] = ""
    
    st.session_state["l_biaya_kontribusi"] = total_biaya_kontribusi_display
    
    st.text_input("Total Biaya Kontribusi per Bulan:", key="l_biaya_kontribusi", disabled=True)

   

    # Konversi ke string untuk template
    context = {
        # INFORMASI DOKUMEN
        "nomor_perjanjian": nomor_perjanjian,
        "nomor_perjanjian_upper": nomor_perjanjian_upper,
        "hari_setuju": hari_setuju,
        "tanggal_setuju": tanggal_setuju,
        "bulan_setuju": bulan_setuju,
        "tahun_setuju": tahun_setuju,
        
        # DATA PIHAK KEDUA
        "jenis_badan_usaha_perusahaan_pihak_kedua": jenis_badan_usaha,
        "nama_perusahaan_pihak_kedua": nama_perusahaan_pihak_kedua,
        "nama_perusahaan_pihak_kedua_upper": nama_perusahaan_pihak_kedua_upper,
        "nama_perusahaan_pihak_kedua_title": nama_perusahaan_pihak_kedua_title,
        
        "nama_proyek": nama_proyek,
        "nama_proyek_upper": nama_proyek_upper,
        "nama_proyek_title": nama_proyek_title,
        
        "nama_pihak_kedua": nama_pihak_kedua,
        "nama_pihak_kedua_upper": nama_pihak_kedua_upper,
        "nama_pihak_kedua_title": nama_pihak_kedua_title,
        
        "jabatan_pihak_kedua": jabatan_pihak_kedua,
        "jabatan_pihak_kedua_upper": jabatan_pihak_kedua_upper,
        "jabatan_pihak_kedua_title": jabatan_pihak_kedua_title,
        
        "alamat_perusahaan_pihak_kedua": alamat_perusahaan_pihak_kedua,
        "alamat_perusahaan_pihak_kedua_title": alamat_perusahaan_pihak_kedua_title,
        
        "nomor_telepon_pihak_kedua": nomor_telepon_pihak_kedua,
        "email_pihak_kedua": email_pihak_kedua,
        
        # DATA LAHAN
        "wilayah": wilayah,
        "wilayah_upper": wilayah_upper,
        "wilayah_title": wilayah_title,
        
        # DATA UKURAN
        "ukuran_meter": ukuran_meter,
        "ukuran_meter2": ukuran_meter2_display,
        
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
        "dasar_perjanjian": dasar_perjanjian_text,
        
        # DATA BIAYA (ANGKA)
        "harga_dasar_lahan_angka": harga_dasar_lahan_angka_formatted,
        "angka_ppn": angka_ppn,
        
        # DATA BIAYA (TERBILANG)
        "total_harga_lahan_terbilang": total_harga_lahan_display,
        "total_harga_setelah_ppn_terbilang": total_harga_setelah_ppn_display,
        "biaya_kontribusi_sampah_terbilang": biaya_kontribusi_sampah_display,
        "total_biaya_sampah_setelah_ppn_terbilang": total_biaya_sampah_setelah_ppn_display,
        "total_biaya_kontrbusi_terbilang": total_biaya_kontribusi_display,
        
        # TERMIN PEMBAYARAN
        "termin_terbilang": termin_terbilang,
        "bulan_termin_1": bulan_termin_1,
        "bulan_termin_2": bulan_termin_2,
        "bulan_termin_3": bulan_termin_3,
    }
    
    st.write("---")
    if st.button("📄 Generate Surat Perjanjian (Lahan)", key="btn_generate_lahan"):
        # ====== VALIDASI DATA ======
        errors = []
        
        # Informasi Dokumen
        if not nomor_perjanjian.strip():
            errors.append("Nomor Perjanjian")
        
        # Data Pihak Kedua
        if not jenis_badan_usaha:
            errors.append("Jenis Badan Usaha")
        if not nama_perusahaan_pihak_kedua.strip():
            errors.append("Nama Perusahaan")
        if not nama_proyek.strip():
            errors.append("Nama Proyek")
        if not nama_pihak_kedua.strip():
            errors.append("Nama Penandatangan")
        if not jabatan_pihak_kedua.strip():
            errors.append("Jabatan Penandatangan")
        if not alamat_perusahaan_pihak_kedua.strip():
            errors.append("Alamat Perusahaan")
        if not nomor_telepon_pihak_kedua.strip():
            errors.append("Nomor Telepon/HP/WA")
        if not email_pihak_kedua.strip():
            errors.append("Email Perusahaan")
        
        # Data Lahan
        if not wilayah.strip():
            errors.append("Wilayah Lahan")
        if not ukuran_meter.strip():
            errors.append("Ukuran Lahan")
        if not lama_sewa.strip():
            errors.append("Lama Sewa")
        
        # Dasar Perjanjian
        if not dasar_perjanjian_list:
            error.append("Minimal 1 dasar perjanjian harus diisi")
        
        # Data Biaya
        if not harga_dasar_lahan.strip():
            errors.append("Harga Dasar Lahan per m²")
        if not biaya_kontribusi_sampah.strip():
            errors.append("Biaya Kontribusi Sampah")
        
        # Cek apakah ada error
        if errors:
            st.error(f"**Harap lengkapi data berikut:**\n\n• " + "\n• ".join(errors))
            return
        
                # ===== CEK DUPLIKASI =====
        collection = get_lahan_collection()
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

        data_lahan = {
            "Lokasi": wilayah_title,
            "Nomor Surat Perjanjian": nomor_perjanjian_upper,
            "Penyewa": nama_perusahaan_pihak_kedua_title,
            "Luas (m²)": ukuran_meter,
            "Tanggal Mulai": tgl_mulai.strftime("%d-%m-%Y"),
            "Tanggal Selesai": tgl_selesai.strftime("%d-%m-%Y"),
            "Biaya Sewa Pertahun": total_biaya_kontribusi,
            "created_at": datetime.utcnow()
        }

        collection.insert_one(data_lahan)

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

