# # from pymongo import MongoClient
# # import streamlit as st

# # MONGODB_URI = "mongodb+srv://ahmadihdafalah:amdryzen1010@cluster0.10a3ead.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# # DB_NAME = "surat_pal"

# # client = MongoClient(MONGODB_URI)
# # db = client[DB_NAME]


# # surat_mess = db["surat_mess"]
# # surat_container = db["surat_container"]
# # surat_kantor = db["surat_kantor"]
# # surat_lahan = db["surat_lahan"]
# # surat_kuasa = db["surat_kuasa"]

# # db.py
# import os
# from pymongo import MongoClient
# from datetime import datetime

# # =============================
# # KONEKSI MONGODB
# # =============================

# def get_database():
#     """
#     Mengembalikan database surat_pal
#     """
#     MONGO_URI = os.getenv(
#         "MONGO_URI",
#         "mongodb://ahmadihdafalah:amdryzen1010@cluster0.10a3ead.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#     )

#     client = MongoClient(MONGO_URI)
#     return client["surat_pal"]

# def insert_mess_data(data: dict):
#     """
#     Simpan data sewa mess ke collection mess
#     """
#     db = get_database()
#     collection = db["mess"]

#     data["created_at"] = datetime.now()

#     collection.insert_one(data)

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

