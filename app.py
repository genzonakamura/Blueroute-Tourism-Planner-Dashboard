import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Terengganu EcoTourism Dashboard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .title-text { font-size: 2.1rem; font-weight: 700; color: #1E293B; margin-bottom: 4px; }
    .subtitle-text { font-size: 1rem; color: #64748B; margin-bottom: 24px; }
    
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }
    
    .kpi-title { font-size: 0.85rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 1.8rem; color: #0F172A; font-weight: 700; margin-top: 4px; }
    .kpi-note { font-size: 0.8rem; color: #059669; margin-top: 4px; font-weight: 600; }
    .kpi-note-warn { font-size: 0.8rem; color: #DC2626; margin-top: 4px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA (TERENGGANU)
# ---------------------------------------------------------
@st.cache_data
def get_data():
    destinations = pd.DataFrame({
        'Destinasi': ['KTCC Mall / Pantai Miami', 'Pasar Besar Kedai Payang', 'Pantai Batu Buruk', 'Pulau Redang', 'Pulau Perhentian', 'Tasik Kenyir / Sekayu'],
        'Daerah': ['Kuala Terengganu', 'Kuala Terengganu', 'Kuala Terengganu', 'Kuala Nerus', 'Besut', 'Hulu Terengganu'],
        'Lat': [5.3323, 5.3364, 5.3210, 5.7600, 5.9082, 4.9680],
        'Lon': [103.1415, 103.1360, 103.1490, 103.0100, 102.7350, 102.8250],
        'Anggaran_Pelawat': [8500, 7200, 6800, 5400, 4800, 1500],
        'Kapasiti_Maksimum': [6000, 5500, 5000, 3500, 3000, 5000],
        'Risiko_Ekosistem': ['Rendah', 'Sederhana', 'Rendah', 'Tinggi (Terumbu Karang)', 'Tinggi (Terumbu Karang)', 'Sederhana'],
        'Anggaran_Sisa_Ton': [4.2, 3.8, 3.1, 2.7, 2.2, 0.8]
    })
    
    destinations['Nisbah_Kapasiti'] = destinations['Anggaran_Pelawat'] / destinations['Kapasiti_Maksimum']
    destinations['Skor_TPI'] = (destinations['Nisbah_Kapasiti'] * 70).clip(0, 100).round(1)
    
    def status_label(skor):
        if skor >= 81: return 'Tinggi (Tepu)'
        elif skor >= 61: return 'Sederhana Tinggi'
        elif skor >= 31: return 'Sederhana'
        else: return 'Tenteram'

    destinations['Status_Kesesakan'] = destinations['Skor_TPI'].apply(status_label)
    return destinations

df = get_data()

df_trend = pd.DataFrame({
    'Tahun': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    'Pelawat_Juta': [13.74, 14.16, 7.42, 3.72, 10.23, 11.76, 12.80, 13.90, 14.95],
    'Status_Data': ['Data Sejarah (DOSM)', 'Data Sejarah (DOSM)', 'Data Sejarah (DOSM)', 'Data Sejarah (DOSM)', 'Data Sejarah (DOSM)', 'Data Sejarah (DOSM)', 'Unjuran Trend', 'Unjuran Trend', 'Unjuran Trend']
})


st.sidebar.markdown("### 🌴 **Pelancongan Terengganu**")
st.sidebar.caption("Sistem Pemantauan & Perancangan Mampan")
st.sidebar.markdown("---")

pilihan_halaman = st.sidebar.radio("Pilih Paparan:", [
    "📊 Pemantauan Kawasan (Kerajaan)",
    "🗺️ Perancang Perjalanan (Pelancong)",
    "📈 Trend Unjuran & Impak SDG"
])

st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚙️ **Pelarasan Simulasi Musim Cuti**")
tambahan_pelawat = st.sidebar.slider("Jangkaan Pertambahan Pelawat (%):", 0, 50, 10, step=5)


if pilihan_halaman == "📊 Pemantauan Kawasan (Kerajaan)":
    st.markdown('<div class="title-text">📊 Pemantauan Kapasiti & Risiko Pelancongan</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Gambaran keseluruhan paras kesesakan destinasi utama di Terengganu untuk tindakan kawalan awam.</div>', unsafe_allow_html=True)

    df_live = df.copy()
    df_live['Anggaran_Pelawat'] = (df_live['Anggaran_Pelawat'] * (1 + tambahan_pelawat/100)).astype(int)
    df_live['Nisbah_Kapasiti'] = df_live['Anggaran_Pelawat'] / df_live['Kapasiti_Maksimum']
    df_live['Skor_TPI'] = (df_live['Nisbah_Kapasiti'] * 70).clip(0, 100).round(1)

    col1, col2, col3, col4 = st.columns(4)
    jum_pelawat = df_live['Anggaran_Pelawat'].sum()
    kawasan_padat = len(df_live[df_live['Skor_TPI'] >= 61])
    jum_sisa = df_live['Anggaran_Sisa_Ton'].sum() * (1 + tambahan_pelawat/100)

    with col1:
        st.markdown(f'''
        <div class="card">
            <div class="kpi-title">Jangkaan Pelawat Harian</div>
            <div class="kpi-value">{jum_pelawat:,}</div>
            <div class="kpi-note">+{tambahan_pelawat}% simulasi cuti</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="card">
            <div class="kpi-title">Zon Tumpuan Padat</div>
            <div class="kpi-value">{kawasan_padat} Destinasi</div>
            <div class="kpi-note-warn">Perlu pemantauan trafik</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
        <div class="card">
            <div class="kpi-title">Anggaran Sisa Pepejal</div>
            <div class="kpi-value">{jum_sisa:.1f} Ton/hari</div>
            <div class="kpi-note">Kapasiti pembersihan sedia ada</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown('''
        <div class="card">
            <div class="kpi-title">Zon Sensitif Marin</div>
            <div class="kpi-value">Pulau Utama</div>
            <div class="kpi-note-warn">Redang & Perhentian</div>
        </div>
        ''', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.markdown("##### 📍 Taburan Kesesakan Mengikut Lokasi")
        fig_map = px.scatter_map(
            df_live,
            lat="Lat", lon="Lon",
            color="Skor_TPI",
            size="Anggaran_Pelawat",
            hover_name="Destinasi",
            hover_data={"Daerah": True, "Skor_TPI": True, "Kapasiti_Maksimum": True, "Lat": False, "Lon": False},
            color_continuous_scale="YlOrRd",
            size_max=25,
            zoom=7.4,
            map_style="open-street-map"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=380)
        st.plotly_chart(fig_map, use_container_width=True)

    with col_right:
        st.markdown("##### ⚖️ Pelawat vs Kapasiti Had Destinasi")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(y=df_live['Destinasi'], x=df_live['Anggaran_Pelawat'], name='Pelawat Semasa', orientation='h', marker_color='#E07A5F'))
        fig_bar.add_trace(go.Bar(y=df_live['Destinasi'], x=df_live['Kapasiti_Maksimum'], name='Kapasiti Had', orientation='h', marker_color='#3D405B'))
        fig_bar.update_layout(barmode='group', height=380, margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.markdown("##### 📋 Langkah Pengurusan Disyorkan")
    pilih_dest = st.selectbox("Pilih lokasi untuk semak cadangan tindakan tempatan:", df_live['Destinasi'].tolist())
    info = df_live[df_live['Destinasi'] == pilih_dest].iloc[0]

    if info['Skor_TPI'] >= 80:
        st.error(f"🚨 **{pilih_dest} (Skor TPI: {info['Skor_TPI']}/100)**: Kawasan telah melebihi kapasiti selesa. Disyorkan menyalurkan makluman laluan alternatif kepada pemandu bas pelancong dan menambah jadual kutipan sisa di zon utama.")
    elif info['Skor_TPI'] >= 60:
        st.warning(f"⚠️ **{pilih_dest} (Skor TPI: {info['Skor_TPI']}/100)**: Kepadatan sederhana tinggi. Disyorkan menggalakkan pelancong melawat di luar waktu puncak.")
    else:
        st.success(f"✅ **{pilih_dest} (Skor TPI: {info['Skor_TPI']}/100)**: Keadaan persekitaran dan kepadatan berada dalam keadaan baik serta terkawal.")


elif pilihan_halaman == "🗺️ Perancang Perjalanan (Pelancong)":
    st.markdown('<div class="title-text">🗺️ Perancang Perjalanan Mesra Alam</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Bantu anda merancang percutian yang selesa sambil mengurangkan jejak karbon di Terengganu.</div>', unsafe_allow_html=True)

    col_bantu1, col_bantu2 = st.columns([1, 1.2])

    with col_bantu1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🧳 Maklumat Perjalanan")
        dest_pilihan = st.selectbox("Destinasi Utama Pilihan:", df['Destinasi'].tolist())
        hari = st.slider("Bilangan Hari Cutian:", 1, 7, 3)
        keutamaan = st.radio("Suasana Perjalanan Pilihan:", ["Lokasi Popular & Ramai", "Lebih Tenang & Santai (Disyorkan)"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_bantu2:
        st.markdown("##### 💡 Cadangan & Syoran")
        tujuan = df[df['Destinasi'] == dest_pilihan].iloc[0]
        
        if tujuan['Skor_TPI'] >= 60 and keutamaan == "Lebih Tenang & Santai (Disyorkan)":
            st.warning(f"Lokasi **{dest_pilihan}** agak tumpuan buat masa ini (Tahap Kepadatan: {tujuan['Status_Kesesakan']}).")
            
            alternatif = df[df['Skor_TPI'] < 60].iloc[0]
            st.markdown(f'''
            <div class="card" style="border-left: 5px solid #2A9D8F;">
                <b style="color: #2A9D8F;">🌿 Cadangan Alternatif: {alternatif['Destinasi']} ({alternatif['Daerah']})</b><br>
                Lokasi ini menawarkan suasana yang lebih lapang, mengurangkan kesesakan lalulintas, dan membolehkan pengalaman pelancongan yang lebih santai.
            </div>
            ''', unsafe_allow_html=True)

            c_a, c_b, c_c = st.columns(3)
            c_a.metric("Indeks Keselesaan", "Sangat Baik", "90/100")
            c_b.metric("Anggaran Pelepasan CO2", f"{10.5 * hari:.1f} kg", "-28%")
            c_c.metric("Status Kepadatan", alternatif['Status_Kesesakan'])
        else:
            st.success(f"Pilihan yang baik! **{dest_pilihan}** berada dalam keadaan selesa untuk dikunjungi.")
            c_a, c_b, c_c = st.columns(3)
            c_a.metric("Indeks Keselesaan", "Baik", "82/100")
            c_b.metric("Anggaran Pelepasan CO2", f"{13.2 * hari:.1f} kg", "Normal")
            c_c.metric("Status Kepadatan", tujuan['Status_Kesesakan'])


elif pilihan_halaman == "📈 Trend Unjuran & Impak SDG":
    st.markdown('<div class="title-text">📈 Trend Ketibaan & Penjajaran SDG</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analisis trend pertumbuhan pelancongan domestik Terengganu dan sumbangannya kepada kelestarian.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📉 Unjuran Pertumbuhan Pelawat", "🎯 Penjajaran Matlamat SDG"])

    with tab1:
        st.markdown("##### Trend Ketibaan Pelawat Domestik Terengganu (2018–2026)")
        fig_trend = px.line(
            df_trend, x='Tahun', y='Pelawat_Juta', color='Status_Data', markers=True,
            color_discrete_map={'Data Sejarah (DOSM)': '#3D405B', 'Unjuran Trend': '#E07A5F'}
        )
        fig_trend.update_layout(yaxis_title="Jumlah Pelawat (Juta Orang)", height=380)
        st.plotly_chart(fig_trend, use_container_width=True)

        st.caption("Nota: Unjuran menunjukkan peningkatan berterusan pelawat pasca-pandemik, mengesahkan keutamaan perancangan pengurusan sisa dan kapasiti di kawasan pulau & marin.")

    with tab2:
        st.markdown("##### Matlamat Pembangunan Mampan (SDG) Yang Disokong")
        
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("""
            * **SDG 8 (Pekerjaan Layak & Pertumbuhan Ekonomi):** Menggalakkan penyebaran limpahan ekonomi ke kawasan luar bandar seperti Hulu Terengganu dan Besut.
            * **SDG 9 (Industri, Inovasi & Infrastruktur):** Pembangunan alat visualisasi data pelancongan berasaskan data rasmi kerajaan.
            """)
        with s2:
            st.markdown("""
            * **SDG 12 (Penggunaan & Pengeluaran Bertanggungjawab):** Membantu PBT menganggarkan pembuangan sisa pepejal di lokasi tumpuan.
            * **SDG 14 (Kehidupan Di Dalam Air):** Mengurangkan tekanan ekosistem di kawasan perairan sensitif Pulau Redang dan Perhentian.
            """)
