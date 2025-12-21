import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_db():
    """
    Inisialisasi koneksi MongoDB Atlas
    Database: surat_pal
    """
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["surat_pal"]

def get_mess_collection():
    return get_db()["mess"]

def get_container_collection():
    return get_db()["container"]

def get_kantor_collection():
    return get_db()["kantor"]

def get_lahan_collection():
    return get_db()["lahan"]

def get_rumah_dinas_collection():
    return get_db()["rumah_dinas"]


