import streamlit as st
import pandas as pd
from datetime import datetime
import io

from db import (
    get_mess_collection,
    get_container_collection,
    get_kantor_collection,
    get_lahan_collection,
    get_rumah_dinas_collection
)

SCHEMA_MESS = [
    "Lokasi",
    "Nomor Surat Perjanjian",
    "Penyewa",
    "NIP",
    "Unit Kerja",
    "Tanggal Mulai",
    "Tanggal Selesai",
    "Biaya Sewa Perbulan",
    "created_at"
]

SCHEMA_CONTAINER = [
    "Lokasi",
    "Nomor Surat Perjanjian",
    "Penyewa",
    "Volume (Feet)",
    "Luas (m²)",
    "Tanggal Mulai",
    "Tanggal Selesai",
    "Biaya Sewa Perbulan",
    "created_at"
]

SCHEMA_KANTOR = [
    "Lokasi",
    "Nomor Surat Perjanjian",
    "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai",
    "Tanggal Selesai",
    "Biaya Sewa Perbulan",
    "created_at"
]

SCHEMA_RUMAH_DINAS = [
    "Lokasi",
    "Nomor Surat Perjanjian",
    "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai",
    "Tanggal Selesai",
    "Biaya Sewa Pertahun",
    "created_at"
]

SCHEMA_LAHAN = [
    "Lokasi",
    "Nomor Surat Perjanjian",
    "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai",
    "Tanggal Selesai",
    "Biaya Sewa Pertahun",
    "created_at"
]

# Mapping schema ke tab
SCHEMA_MAP = {
    "🏘️ Mess": SCHEMA_MESS,
    "🚢 Container": SCHEMA_CONTAINER,
    "🏢 Kantor": SCHEMA_KANTOR,
    "🏠 Rumah Dinas": SCHEMA_RUMAH_DINAS,
    "🌱 Lahan": SCHEMA_LAHAN
}

# Mapping tab ke collection MongoDB
COLLECTION_MAP = {
    "🏘️ Mess": get_mess_collection,
    "🚢 Container": get_container_collection,
    "🏢 Kantor": get_kantor_collection,
    "🏠 Rumah Dinas": get_rumah_dinas_collection,
    "🌱 Lahan": get_lahan_collection
}


def show():
    """Halaman Arsip Data Surat"""

    st.title("📂 Arsip Data Surat - MongoDB")

    tabs = st.tabs(list(COLLECTION_MAP.keys()))

    for tab, (tab_name, get_collection) in zip(tabs, COLLECTION_MAP.items()):
        with tab:
            collection = get_collection()
            data = list(collection.find({}, {"_id": 0}))

            if not data:
                st.info("📭 Belum ada data pada kategori ini.")
                continue

            df = pd.DataFrame(data)

            # PAKSA SCHEMA PATEN
            schema = SCHEMA_MAP.get(tab_name)
            if schema:
                df = df.reindex(columns=schema)

            # FORMAT CREATED_AT
            if "created_at" in df.columns:
                df["created_at"] = pd.to_datetime(
                    df["created_at"], errors="coerce"
                ).dt.strftime("%d-%m-%Y %H:%M")

            # FORMAT BIAYA
            if "Biaya Sewa Perbulan" in df.columns:
                df["Biaya Sewa Perbulan"] = df["Biaya Sewa Perbulan"].apply(
                    lambda x: f"{int(x):,}".replace(",", ".")
                    if pd.notna(x) else ""
                )

            # TAMPILKAN TABEL
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(f"Total data: {len(df)}")
            
            # Buat 2 kolom untuk tombol download
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Download CSV
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    file_name=f"{tab_name.replace(' ', '_').lower()}_arsip.csv",
                    mime="text/csv",
                    key=f"download_csv_{tab_name}",
                    use_container_width=True
                )
            
            with col_dl2:
                # Download Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Data')
                
                st.download_button(
                    "📊 Download Excel",
                    buffer.getvalue(),
                    file_name=f"{tab_name.replace(' ', '_').lower()}_arsip.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_excel_{tab_name}",
                    use_container_width=True
                )
            
            # with col_dl3:
            #     # Download JSON (opsional)
            #     json_str = df.to_json(orient='records', indent=2, force_ascii=False)
            #     st.download_button(
            #         "📄 Download JSON",
            #         json_str,
            #         file_name=f"{tab_name.replace(' ', '_').lower()}_arsip.json",
            #         mime="application/json",
            #         key=f"download_json_{tab_name}",
            #         use_container_width=True

            #     )
