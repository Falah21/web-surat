import streamlit as st
import os
import sys

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Otomatisasi Surat",
    page_icon="📄",
    layout="wide"
)

# =========================
# SESSION STATE LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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
# LOGIN PAGE
# =========================
# def show_login():
#     st.markdown("<h2 style='text-align:center'>🔐 Login Sistem</h2>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):
#             if (
#                 username == st.secrets["ADMIN_USERNAME"]
#                 and password == st.secrets["ADMIN_PASSWORD"]
#             ):
#                 st.session_state.logged_in = True
#                 st.success("Login berhasil!")
#                 st.query_params.clear()
#                 st.rerun()
#             else:
#                 st.error("Username atau password salah")

def show_login():
    st.markdown("""
    <div style="text-align:center; margin-top:60px;">
        <div style="font-size:64px;">📄</div>
        <h1 style="color:#1E3A8A; margin-bottom:0;">Otomatisasi Surat Aset</h1>
        <p style="color:#555; margin-top:4px;">
            Departemen Optimasi Aset dan Infrastruktur
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("### 🔐 Login ke Sistem")

        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")

        if st.button("Masuk", use_container_width=True):
            if (
                username == st.secrets["ADMIN_USERNAME"]
                and password == st.secrets["ADMIN_PASSWORD"]
            ):
                st.session_state.logged_in = True
                st.success("Login berhasil")
                st.query_params.clear()
                st.rerun()
            else:
                st.error("Username atau password salah")

# =========================
# AUTH GUARD (KUNCI SISTEM)
# =========================
if not st.session_state.logged_in:
    show_login()
    st.stop()

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
# NAVIGASI ATAS (BACK + LOGOUT)
# =========================
def nav_buttons():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Dashboard"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.query_params.clear()
            st.rerun()

# =========================
# HALAMAN-HALAMAN
# =========================
def show_container():
    nav_buttons()
    from modules import container
    container.show()

def show_kantor():
    nav_buttons()
    from modules import kantor
    kantor.show()

def show_mess():
    nav_buttons()
    from modules import mess
    mess.show()

def show_lahan():
    nav_buttons()
    from modules import lahan
    lahan.show()

def show_rumah_dinas():
    nav_buttons()
    from modules import rumahdinas
    rumahdinas.show()

def show_arsip():
    nav_buttons()
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
    nav_buttons()

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


