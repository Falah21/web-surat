import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from db import (
    get_mess_collection,
    get_container_collection,
    get_kantor_collection,
    get_lahan_collection,
    get_rumah_dinas_collection
)

# =========================
# HELPER FUNCTIONS
# =========================
def normalize_biaya(row):
    if "Biaya Sewa Perbulan" in row:
        return row.get("Biaya Sewa Perbulan", 0)
    if "Biaya Sewa Pertahun" in row:
        return row.get("Biaya Sewa Pertahun", 0)
    return 0


def load_all_data():
    mess = list(get_mess_collection().find({}, {"_id": 0}))
    container = list(get_container_collection().find({}, {"_id": 0}))
    kantor = list(get_kantor_collection().find({}, {"_id": 0}))
    lahan = list(get_lahan_collection().find({}, {"_id": 0}))
    rumah = list(get_rumah_dinas_collection().find({}, {"_id": 0}))

    for d in mess:
        d["Kategori"] = "MESS"
    for d in container:
        d["Kategori"] = "KONTAINER"
    for d in kantor:
        d["Kategori"] = "KANTOR"
    for d in lahan:
        d["Kategori"] = "LAHAN"
    for d in rumah:
        d["Kategori"] = "RUMAH DINAS"

    all_data = mess + container + kantor + lahan + rumah

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)

    # Normalisasi biaya
    df["Biaya"] = df.apply(normalize_biaya, axis=1)

    # Parse tanggal
    df["Tanggal Mulai"] = pd.to_datetime(df["Tanggal Mulai"], errors="coerce")
    df["Tanggal Selesai"] = pd.to_datetime(df["Tanggal Selesai"], errors="coerce")

    # Tahun
    df["Tahun"] = df["Tanggal Mulai"].dt.year

    return df


# =========================
# DASHBOARD
# =========================
def show():
    st.markdown(
        "<h2 style='text-align:center;color:#1E3A8A;'>ASET PT PAL INDONESIA</h2>",
        unsafe_allow_html=True
    )

    df = load_all_data()

    if df.empty:
        st.warning("Belum ada data aset di database.")
        return

    # =========================
    # FILTER
    # =========================
    st.subheader("Pilihan Filter")

    col1, col2, col3 = st.columns(3)

    kategori = col1.selectbox(
        "Kategori",
        ["Semua"] + sorted(df["Kategori"].dropna().unique().tolist())
    )

    tahun = col2.selectbox(
        "Periode (Tahun)",
        ["Semua"] + sorted(df["Tahun"].dropna().astype(int).unique().tolist())
    )

    status = col3.selectbox(
        "Status Kontrak",
        ["Semua", "Aktif", "Akan Berakhir"]
    )

    df_filtered = df.copy()

    if kategori != "Semua":
        df_filtered = df_filtered[df_filtered["Kategori"] == kategori]

    if tahun != "Semua":
        df_filtered = df_filtered[df_filtered["Tahun"] == int(tahun)]

    today = pd.Timestamp.today()
    batas_berakhir = today + pd.DateOffset(months=3)

    if status == "Aktif":
        df_filtered = df_filtered[df_filtered["Tanggal Selesai"] >= today]
    elif status == "Akan Berakhir":
        df_filtered = df_filtered[
            (df_filtered["Tanggal Selesai"] >= today) &
            (df_filtered["Tanggal Selesai"] <= batas_berakhir)
        ]

    # =========================
    # KPI
    # =========================
    total_pendapatan = df_filtered["Biaya"].sum()
    total_aset = len(df_filtered)
    aset_terisi = df_filtered["Penyewa"].notna().sum()

    kontrak_aktif = df_filtered[df_filtered["Tanggal Selesai"] >= today]
    kontrak_akan_berakhir = df_filtered[
        (df_filtered["Tanggal Selesai"] >= today) &
        (df_filtered["Tanggal Selesai"] <= batas_berakhir)
    ]

    persentase_terisi = (
        (aset_terisi / total_aset) * 100 if total_aset > 0 else 0
    )

    st.subheader("Overview")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Pendapatan", f"{int(total_pendapatan):,}".replace(",", "."))
    c2.metric("Total Aset", total_aset)
    c3.metric("Kontrak Aktif", len(kontrak_aktif))
    c4.metric("Kontrak Akan Berakhir", len(kontrak_akan_berakhir))
    c5.metric("Aset Terisi", aset_terisi)
    c6.metric("Persentase Terisi", f"{persentase_terisi:.2f}%")

    st.markdown("---")

    # =========================
    # PIE CHART
    # =========================
    st.subheader("Persebaran Aset per Kategori")

    pie_df = (
        df_filtered.groupby("Kategori")
        .size()
        .reset_index(name="Jumlah")
    )

    pie = px.pie(
        pie_df,
        names="Kategori",
        values="Jumlah",
        hole=0.4
    )

    st.plotly_chart(pie, use_container_width=True)

    # =========================
    # LINE CHART
    # =========================
    st.subheader("Capaian Nilai Sewa per Tahun")

    line_df = (
        df_filtered.groupby("Tahun")["Biaya"]
        .sum()
        .reset_index()
        .sort_values("Tahun")
    )

    line = px.line(
        line_df,
        x="Tahun",
        y="Biaya",
        markers=True
    )

    st.plotly_chart(line, use_container_width=True)

    # =========================
    # TABLE (OPTIONAL)
    # =========================
    with st.expander("Lihat Data Detail"):
        st.dataframe(
            df_filtered[
                [
                    "Kategori",
                    "Lokasi",
                    "Penyewa",
                    "Tanggal Mulai",
                    "Tanggal Selesai",
                    "Biaya"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
