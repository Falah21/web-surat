import streamlit as st
import os
import sys

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sistem Otomatisasi Surat",
    page_icon="📄",
    layout="wide"
)

# =========================
# SESSION STATE LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# MODULE PATH
# =========================
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(current_dir, "modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main-header { text-align:center; color:#1E3A8A; }
.card {
    border:1px solid #ddd;
    border-radius:10px;
    padding:20px;
    background:white;
    box-shadow:0 2px 5px rgba(0,0,0,0.1);
    height:180px;
}
.card-icon { font-size:2em; }
.card-title { font-size:1.2em; color:#1E3A8A; }
.card-desc { font-size:0.9em; color:#555; }
.stButton>button { width:100%; }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo_pal (2).png", width=180)
        st.markdown(
            "<h2 style='text-align:center;color:#1E3A8A;'>Sistem Otomatisasi Pembuatan Surat</h2>",
            unsafe_allow_html=True
        )
        st.caption("Silakan login untuk masuk sistem")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Masuk", use_container_width=True):
            if (
                username == st.secrets["ADMIN_USERNAME"]
                and password == st.secrets["ADMIN_PASSWORD"]
            ):
                st.session_state.logged_in = True
                st.query_params.clear()
                st.rerun()
            else:
                st.error("Username atau password salah")

# =========================
# NAV BUTTONS
# =========================
def nav_buttons():
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Menu Utama"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.query_params.clear()
            st.rerun()

# =========================
# MENU UTAMA (3 MENU)
# =========================
def show_main_menu():
    st.markdown("<h1 class='main-header'>Menu Utama</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Silakan pilih menu</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>📝</div>
            <div class='card-title'>Buat Surat</div>
            <div class='card-desc'>Pembuatan surat perjanjian.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Masuk Buat Surat"):
            st.query_params["menu"] = "buat_surat"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>📂</div>
            <div class='card-title'>Lihat Arsip</div>
            <div class='card-desc'>Arsip surat yang telah dibuat.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Lihat Arsip"):
            st.query_params["menu"] = "arsip"
            st.rerun()

    with col3:
        st.markdown("""
        <div class='card'>
            <div class='card-icon'>📊</div>
            <div class='card-title'>Dashboard</div>
            <div class='card-desc'>Ringkasan dan analitik.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Dashboard"):
            st.query_params["menu"] = "dashboard"
            st.rerun()

# =========================
# SUBMENU BUAT SURAT
# =========================
def show_buat_surat_menu():
    nav_buttons()
    st.subheader("Buat Surat")

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
            <div class='card-icon'>📩</div>
            <div class='card-title'>Surat Kuasa</div>
            <div class='card-desc'>Penandatangan surat kuasa.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Surat Kuasa"):
            st.query_params["page"] = "surat_kuasa"
            st.rerun()

# =========================
# PAGE WRAPPERS
# =========================
def show_container():
    nav_buttons()
    from modules import container
    container.show()

def show_kantor():
    nav_buttons()
    from modules import kantor
    kantor.show()

def show_lahan():
    nav_buttons()
    from modules import lahan
    lahan.show()

def show_mess():
    nav_buttons()
    from modules import mess
    mess.show()

def show_rumah_dinas():
    nav_buttons()
    from modules import rumahdinas
    rumahdinas.show()

def show_surat_kuasa():
    nav_buttons()
    from modules import surat_kuasa
    surat_kuasa.show()

def show_arsip():
    nav_buttons()
    from modules import arsip_data
    arsip_data.show()

# =========================
# AUTH GUARD
# =========================
if not st.session_state.logged_in:
    show_login()
    st.stop()

# =========================
# ROUTER
# =========================
menu = st.query_params.get("menu", "home")
page = st.query_params.get("page", "")

if menu == "home":
    show_main_menu()

elif menu == "buat_surat":
    if page == "":
        show_buat_surat_menu()
    elif page == "container":
        show_container()
    elif page == "kantor":
        show_kantor()
    elif page == "lahan":
        show_lahan()
    elif page == "mess":
        show_mess()
    elif page == "rumah_dinas":
        show_rumah_dinas()
    elif page == "surat_kuasa":
        show_surat_kuasa()
    else:
        st.warning("Halaman tidak ditemukan")

elif menu == "arsip":
    show_arsip()

elif menu == "dashboard":
    nav_buttons()
    # # st.info("Dashboard analitik (akan dikembangkan)")
    # from modules import dashboard
    # dashboard.show()
    st.subheader("📊 Dashboard Aset PT PAL Indonesia")
    st.components.v1.iframe(
        src="https://lookerstudio.google.com/embed/reporting/e857cbdf-24a0-408e-b717-1d39a7fcf606/page/p_x332rxz6xd",
        height=900,
        scrolling=True
    )

else:
    show_main_menu()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#666'>"
    "Departemen Optimasi Aset dan Infrastruktur • © 2025"
    "</div>",
    unsafe_allow_html=True
)







