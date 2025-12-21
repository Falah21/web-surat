# import streamlit as st
# import os
# import sys
# from datetime import datetime

# # Konfigurasi halaman
# st.set_page_config(
#     page_title="AutoSurat",
#     page_icon="📄",
#     layout="wide"
# )

# # Tambahkan path modules ke sys.path agar bisa diimport
# current_dir = os.path.dirname(os.path.abspath(__file__))
# modules_path = os.path.join(current_dir, "modules")
# if modules_path not in sys.path:
#     sys.path.append(modules_path)

# # CSS styling
# st.markdown("""
# <style>
#     # /* Kurangi margin default dari elemen Streamlit */
#     # .stApp {
#     #     margin-top: 0px;
#     # }
#     # .block-container {
#     #     padding-top: 1rem;
#     #     padding-bottom: 0rem;
#     # }
#     .main-header {
#         text-align: center;
#         color: #1E3A8A;
#         padding: 20px 0;
#     }
#     .card {
#         border: 1px solid #ddd;
#         border-radius: 10px;
#         padding: 20px;
#         margin: 10px 0;
#         background-color: white;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#         transition: transform 0.2s, box-shadow 0.2s;
#         height: 180px;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#     }
#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 5px 15px rgba(0,0,0,0.15);
#     }
#     .card-title {
#         color: #1E3A8A;
#         font-size: 1.3em;
#         margin-bottom: 10px;
#         line-height: 1.3;
#     }
#     .card-desc {
#         color: #666;
#         font-size: 0.9em;
#         margin-bottom: 15px;
#         flex-grow: 1;
#     }
#     .card-icon {
#         font-size: 1.8em;
#         margin-bottom: 10px;
#     }
#     .stButton>button {
#         width: 100%;
#         font-size: 0.9em;
#         padding: 8px 16px;
#     }
#     .back-button {
#         background-color: #6B7280 !important;
#         color: white !important;
#         margin-bottom: 20px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Inisialisasi session state
# if 'current_page' not in st.session_state:
#     st.session_state.current_page = "dashboard"
# if 'surat_container' not in st.session_state:
#     st.session_state.surat_container = []
# if 'surat_kantor' not in st.session_state:
#     st.session_state.surat_kantor = []
# if 'surat_rumah_dinas' not in st.session_state:
#     st.session_state.surat_rumah_dinas = []
# if 'surat_mess' not in st.session_state:
#     st.session_state.surat_mess = []
# if 'surat_lahan' not in st.session_state:
#     st.session_state.surat_lahan = []

# # ====== DASHBOARD ======
# def show_dashboard():
#     st.markdown("<h1 class='main-header'>Sistem Pembuatan Surat Otomatis</h1>", unsafe_allow_html=True)
#     # st.markdown("### Dashboard Utama")
#     st.markdown("""
#                 <h4 style='text-align: center; margin-bottom: 20px;'>
#                 Silahkan pilih jenis menu yang ada dibawah ini:
#                 </h4>""", unsafe_allow_html=True)
    
#     # Baris pertama - 3 kolom
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>🚢</div>
#             <div class='card-title'>Peti Kemas (Container)</div>
#             <div class='card-desc'>
#                 Untuk perjanjian kerjasama pendayagunaan peti kemas (container).
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("Buat Surat Container", key="btn_container", use_container_width=True):
#             st.session_state.current_page = "container"
#             st.rerun()
    
#     with col2:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>🏢</div>
#             <div class='card-title'>Kantor</div>
#             <div class='card-desc'>
#                 Untuk perjanjian kerjasama pendayagunaan ruang kantor.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("Buat Surat Kantor", key="btn_kantor", use_container_width=True):
#             st.session_state.current_page = "kantor"
#             st.rerun()
    
#     with col3:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>🏠</div>
#             <div class='card-title'>Rumah Dinas</div>
#             <div class='card-desc'>
#                 Untuk perjanjian kerjasama pendayagunaan rumah dinas PT PAL Indonesia.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("Buat Surat Rumah Dinas", key="btn_rumah_dinas", use_container_width=True):
#             st.session_state.current_page = "rumah_dinas"
#             st.rerun()
    
#     # Spasi antara baris
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Baris kedua - 3 kolom
#     col4, col5, col6 = st.columns(3)
    
#     with col4:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>🏘️</div>
#             <div class='card-title'>Mess Menanggal</div>
#             <div class='card-desc'>
#                 Untuk perjanjian kontribusi mess di komplek Menanggal, Surabaya.
#             </div>
#         </div>
#          """, unsafe_allow_html=True)
            
#         if st.button("Buat Surat Mess", key="btn_mess", use_container_width=True):
#             st.session_state.current_page = "mess"
#             st.rerun()
        
#     with col5:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>🌱</div>
#             <div class='card-title'>Lahan</div>
#             <div class='card-desc'>
#                 Untuk perjanjian kerjasama pendayagunaan lahan.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
            
#         if st.button("Buat Surat Lahan", key="btn_lahan", use_container_width=True):
#             st.session_state.current_page = "lahan"
#             st.rerun()

#     with col6:
#         st.markdown("""
#         <div class='card'>
#             <div class='card-icon'>📂</div>
#             <div class='card-title'>Lihat Arsip Data</div>
#             <div class='card-desc'>
#                 Lihat dan kelola arsip surat yang sudah dibuat sebelumnya.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         if st.button("Lihat Arsip", key="btn_arsip", use_container_width=True):
#             st.session_state.current_page = "arsip"
#             st.rerun()
            
# # ====== RUMAH DINAS ======
# def show_rumah_dinas():
#     # Tombol kembali
#     col1, col2 = st.columns([1, 6])
#     with col1:
#         if st.button("← Dashboard", use_container_width=True, key="back_rumah_dinas"):
#             st.session_state.current_page = "dashboard"
#             st.rerun()
    
#     # Coba import modul rumah dinas
#     try:
#         # Coba beberapa cara import
#         try:
#             # Cara 1: Import langsung dari modules
#             from modules import rumahdinas
#             rumahdinas.show()
#         except ImportError:
#             # Cara 2: Import dari current directory
#             import modules.rumahdinas
#             rumahdinas.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul rumah dinas: {str(e)}")
#         st.info("""
#         **Troubleshooting:**
#         1. Pastikan ada folder `modules` di direktori yang sama dengan `app.py`
#         2. Pastikan ada file `rumahdinas.py` di dalam folder `modules`
#         3. Pastikan file `rumahdinas.py` memiliki fungsi `show()`
        
#         **Struktur folder yang benar:**
#         ```
#         your_project/
#         ├── app.py
#         ├── modules/
#         │   ├── __init__.py
#         │   └── rumahdinas.py
#         └── requirements.txt
#         ```
#         """)

# # ====== Halaman lain (dalam pengembangan) ======
# def show_container():
#     col1, col2 = st.columns([1, 6])
#     with col1:
#         if st.button("← Dashboard", use_container_width=True, key="back_container"):
#             st.session_state.current_page = "dashboard"
#             st.rerun()
    
#     try:
#         # Coba beberapa cara import
#         try:
#             # Cara 1: Import langsung dari modules
#             from modules import container
#             container.show()
#         except ImportError:
#             # Cara 2: Import dari current directory
#             import modules.container
#             container.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul container: {str(e)}")
#         st.info("""
#         **Troubleshooting:**
#         1. Pastikan ada folder `modules` di direktori yang sama dengan `app.py`
#         2. Pastikan ada file `container.py` di dalam folder `modules`
#         3. Pastikan file `container.py` memiliki fungsi `show()`
        
#         **Struktur folder yang benar:**
#         ```
#         your_project/
#         ├── app.py
#         ├── modules/
#         │   ├── __init__.py
#         │   └── container.py
#         └── requirements.txt
#         ```
#         """)

# def show_kantor():
#     col1, col2 = st.columns([1, 6])
#     with col1:
#         if st.button("← Dashboard", use_container_width=True, key="back_kantor"):
#             st.session_state.current_page = "dashboard"
#             st.rerun()
    
#     try:
#         # Coba beberapa cara import
#         try:
#             # Cara 1: Import langsung dari modules
#             from modules import kantor
#             kantor.show()
#         except ImportError:
#             # Cara 2: Import dari current directory
#             import modules.kantor
#             kantor.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul kantor: {str(e)}")
#         st.info("""
#         **Troubleshooting:**
#         1. Pastikan ada folder `modules` di direktori yang sama dengan `app.py`
#         2. Pastikan ada file `kantor.py` di dalam folder `modules`
#         3. Pastikan file `kantor.py` memiliki fungsi `show()`
        
#         **Struktur folder yang benar:**
#         ```
#         your_project/
#         ├── app.py
#         ├── modules/
#         │   ├── __init__.py
#         │   └── kantor.py
#         └── requirements.txt
#         ```
#         """)

# def show_mess():
#     col1, col2 = st.columns([1, 6])
#     with col1:
#         if st.button("← Dashboard", use_container_width=True, key="back_mess"):
#             st.session_state.current_page = "dashboard"
#             st.rerun()
    
#     try:
#         # Coba beberapa cara import
#         try:
#             # Cara 1: Import langsung dari modules
#             from modules import mess
#             mess.show()
#         except ImportError:
#             # Cara 2: Import dari current directory
#             import modules.mess
#             mess.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul mess: {str(e)}")
#         st.info("""
#         **Troubleshooting:**
#         1. Pastikan ada folder `modules` di direktori yang sama dengan `app.py`
#         2. Pastikan ada file `mess.py` di dalam folder `modules`
#         3. Pastikan file `mess.py` memiliki fungsi `show()`
        
#         **Struktur folder yang benar:**
#         ```
#         your_project/
#         ├── app.py
#         ├── modules/
#         │   ├── __init__.py
#         │   └── mess.py
#         └── requirements.txt
#         ```
#         """)

# def show_lahan():
#     col1, col2 = st.columns([1, 6])
#     with col1:
#         if st.button("← Dashboard", use_container_width=True, key="back_lahan"):
#             st.session_state.current_page = "dashboard"
#             st.rerun()
    
#     try:
#         # Coba beberapa cara import
#         try:
#             # Cara 1: Import langsung dari modules
#             from modules import lahan
#             lahan.show()
#         except ImportError:
#             # Cara 2: Import dari current directory
#             import modules.lahan
#             lahan.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul lahan: {str(e)}")
#         st.info("""
#         **Troubleshooting:**
#         1. Pastikan ada folder `modules` di direktori yang sama dengan `app.py`
#         2. Pastikan ada file `lahan.py` di dalam folder `modules`
#         3. Pastikan file `lahan.py` memiliki fungsi `show()`
        
#         **Struktur folder yang benar:**
#         ```
#         your_project/
#         ├── app.py
#         ├── modules/
#         │   ├── __init__.py
#         │   └── lahan.py
#         └── requirements.txt
#         ```
#         """)

# # ====== ARSIP DATA ======
# def show_arsip():
#     # Import modul arsip data
#     try:
#         from modules import arsip_data
#         arsip_data.show()
#     except Exception as e:
#         st.error(f"Gagal memuat modul arsip data: {str(e)}")
#         st.info("""
#         **Pastikan:**
#         1. File `modules/arsip_data.py` ada
#         2. Library `pymongo` dan `pandas` terinstall
#         3. File `secrets.toml` berisi connection string MongoDB
#         """)

# # ====== ROUTER UTAMA ======
# page = st.session_state.current_page

# if page == "dashboard":
#     show_dashboard()
# elif page == "rumah_dinas":
#     show_rumah_dinas()
# elif page == "container":
#     show_container()
# elif page == "kantor":
#     show_kantor()
# elif page == "mess":
#     show_mess()
# elif page == "lahan":
#     show_lahan()
# elif page == "arsip":
#     show_arsip()

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: #666;'>"
#     "Created by: Departemen Optimasi Aset dan Infrastruktur • © 2025 • Sistem Pembuatan Surat Otomatis"
#     "</div>",
#     unsafe_allow_html=True
# )

import streamlit as st
import os
import sys

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="AutoSurat",
    page_icon="📄",
    layout="wide"
)

# =========================
# SET PATH MODULES
# =========================
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(current_dir, "modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)

# =========================
# CSS STYLING
# =========================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E3A8A;
        padding: 20px 0;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    .card-title {
        color: #1E3A8A;
        font-size: 1.3em;
        margin-bottom: 10px;
    }
    .card-desc {
        color: #666;
        font-size: 0.9em;
        flex-grow: 1;
    }
    .card-icon {
        font-size: 1.8em;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
def show_dashboard():
    st.markdown("<h1 class='main-header'>Sistem Pembuatan Surat Otomatis</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Silahkan pilih menu di bawah ini:</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>🚢</div>
            <div class='card-title'>Peti Kemas (Container)</div>
            <div class='card-desc'>Perjanjian pendayagunaan container.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Surat Container"):
            st.query_params["page"] = "container"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>🏢</div>
            <div class='card-title'>Kantor</div>
            <div class='card-desc'>Perjanjian pendayagunaan ruang kantor.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Surat Kantor"):
            st.query_params["page"] = "kantor"
            st.rerun()

    with col3:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>🏠</div>
            <div class='card-title'>Rumah Dinas</div>
            <div class='card-desc'>Perjanjian pendayagunaan rumah dinas.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Surat Rumah Dinas"):
            st.query_params["page"] = "rumah_dinas"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>🏘️</div>
            <div class='card-title'>Mess Menanggal</div>
            <div class='card-desc'>Perjanjian kontribusi mess.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Surat Mess"):
            st.query_params["page"] = "mess"
            st.rerun()

    with col5:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>🌱</div>
            <div class='card-title'>Lahan</div>
            <div class='card-desc'>Perjanjian pendayagunaan lahan.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buat Surat Lahan"):
            st.query_params["page"] = "lahan"
            st.rerun()

    with col6:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>📂</div>
            <div class='card-title'>Arsip Data</div>
            <div class='card-desc'>Lihat arsip surat.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Lihat Arsip"):
            st.query_params["page"] = "arsip"
            st.rerun()

# =========================
# HALAMAN-HALAMAN
# =========================
def back_button():
    if st.button("← Dashboard"):
        st.query_params.clear()
        st.rerun()

def show_container():
    back_button()
    from modules import container
    container.show()

def show_kantor():
    back_button()
    from modules import kantor
    kantor.show()

def show_mess():
    back_button()
    from modules import mess
    mess.show()

def show_lahan():
    back_button()
    from modules import lahan
    lahan.show()

def show_rumah_dinas():
    back_button()
    from modules import rumahdinas
    rumahdinas.show()

def show_arsip():
    back_button()
    from modules import arsip_data
    arsip_data.show()

# =========================
# ROUTER UTAMA (QUERY PARAM)
# =========================
page = st.query_params.get("page", "dashboard")

if page == "dashboard":
    show_dashboard()
elif page == "container":
    show_container()
elif page == "kantor":
    show_kantor()
elif page == "mess":
    show_mess()
elif page == "lahan":
    show_lahan()
elif page == "rumah_dinas":
    show_rumah_dinas()
elif page == "arsip":
    show_arsip()
else:
    st.warning("Halaman tidak ditemukan.")
    back_button()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#666'>"
    "Departemen Optimasi Aset dan Infrastruktur • © 2025 • Sistem Pembuatan Surat Otomatis"
    "</div>",
    unsafe_allow_html=True
)

