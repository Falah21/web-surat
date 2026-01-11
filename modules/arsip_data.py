import os
import streamlit as st
import pandas as pd
import io

from db import (
    get_mess_collection,
    get_container_collection,
    get_kantor_collection,
    get_lahan_collection,
    get_rumah_dinas_collection
)

# ================= SCHEMA =================
SCHEMA_MESS = [
    "Lokasi", "Nomor Surat Perjanjian", "Penyewa",
    "NIP", "Unit Kerja",
    "Tanggal Mulai", "Tanggal Selesai",
    "Biaya Sewa Perbulan", "created_at", "file_path"
]

SCHEMA_CONTAINER = [
    "Lokasi", "Nomor Surat Perjanjian", "Penyewa",
    "Volume (Feet)", "Luas (m²)",
    "Tanggal Mulai", "Tanggal Selesai",
    "Biaya Sewa Perbulan", "created_at", "file_path"
]

SCHEMA_KANTOR = [
    "Lokasi", "Nomor Surat Perjanjian", "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai", "Tanggal Selesai",
    "Biaya Sewa Perbulan", "created_at", "file_path"
]

SCHEMA_RUMAH_DINAS = [
    "Lokasi", "Nomor Surat Perjanjian", "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai", "Tanggal Selesai",
    "Biaya Sewa Pertahun", "created_at", "file_path"
]

SCHEMA_LAHAN = [
    "Lokasi", "Nomor Surat Perjanjian", "Penyewa",
    "Luas (m²)",
    "Tanggal Mulai", "Tanggal Selesai",
    "Biaya Sewa Pertahun", "created_at", "file_path"
]

# ================= MAPPING =================
SCHEMA_MAP = {
    "🏘️ Mess": SCHEMA_MESS,
    "🚢 Container": SCHEMA_CONTAINER,
    "🏢 Kantor": SCHEMA_KANTOR,
    "🏠 Rumah Dinas": SCHEMA_RUMAH_DINAS,
    "🌱 Lahan": SCHEMA_LAHAN
}

COLLECTION_MAP = {
    "🏘️ Mess": get_mess_collection,
    "🚢 Container": get_container_collection,
    "🏢 Kantor": get_kantor_collection,
    "🏠 Rumah Dinas": get_rumah_dinas_collection,
    "🌱 Lahan": get_lahan_collection
}


def show():
    st.title("📂 Lihat Data Surat")

    tabs = st.tabs(list(COLLECTION_MAP.keys()))

    for tab, (tab_name, get_collection) in zip(tabs, COLLECTION_MAP.items()):
        with tab:
            collection = get_collection()
            data = list(collection.find({}, {"_id": 0}))

            if not data:
                st.info("📭 Belum ada data pada kategori ini.")
                continue

            df = pd.DataFrame(data)

            # ===== PAKSA SCHEMA =====
            schema = SCHEMA_MAP.get(tab_name)
            if schema:
                df = df.reindex(columns=schema)

            # ===== FORMAT TANGGAL =====
            for col in ["Tanggal Mulai", "Tanggal Selesai"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(
                        df[col], errors="coerce"
                    ).dt.strftime("%d-%m-%Y")

            if "created_at" in df.columns:
                df["created_at"] = pd.to_datetime(
                    df["created_at"], errors="coerce"
                ).dt.strftime("%d-%m-%Y")

            # ===== FORMAT BIAYA =====
            for biaya_col in ["Biaya Sewa Perbulan", "Biaya Sewa Pertahun"]:
                if biaya_col in df.columns:
                    df[biaya_col] = df[biaya_col].apply(
                        lambda x: f"{int(x):,}".replace(",", ".")
                        if pd.notna(x) else ""
                    )

            # ===== TAMPILKAN TABEL =====
            st.dataframe(
                df.drop(columns=["file_path"], errors="ignore"),
                use_container_width=True,
                hide_index=True
            )

            st.caption(f"Total data: {len(df)}")

            # ===== DOWNLOAD CSV & EXCEL =====
            col1, col2 = st.columns(2)

            with col1:
                csv = df.drop(columns=["file_path"], errors="ignore") \
                        .to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    file_name=f"{tab_name.replace(' ', '_').lower()}_arsip.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"csv_{tab_name}"
                )

            with col2:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.drop(columns=["file_path"], errors="ignore") \
                      .to_excel(writer, index=False, sheet_name="Data")

                st.download_button(
                    "📊 Download Excel",
                    buffer.getvalue(),
                    file_name=f"{tab_name.replace(' ', '_').lower()}_arsip.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key=f"xlsx_{tab_name}"
                )

            # ===== DOWNLOAD DOCX PER SURAT =====
            st.divider()
            st.subheader("📄 Download Dokumen Surat")

            for _, row in df.iterrows():
                file_path = row.get("file_path")

                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=row["Nomor Surat Perjanjian"],
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"docx_{tab_name}_{row['Nomor Surat Perjanjian']}"
                        )
                else:
                    st.warning(
                        f"File tidak ditemukan untuk: {row['Nomor Surat Perjanjian']}",
                        icon="⚠️"
                    )
