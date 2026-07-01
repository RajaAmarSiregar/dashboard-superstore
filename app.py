import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# KONFIGURASI
# =====================================================

st.set_page_config(
    page_title="Interaksi Visualisasi Data",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#F6F3EC;
}

.block-container{
    max-width:1250px;
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#082338;
    font-weight:800;
}

h2{
    color:#082338;
    font-weight:700;
}

.stTabs [data-baseweb="tab-list"]{
    gap:15px;
}

.stTabs [data-baseweb="tab"]{

    background:#ffffff;

    color:#082338 !important;

    border-radius:12px;

    padding:12px 25px;

    font-size:17px;

    font-weight:700;

    border:2px solid #082338;

    transition:0.3s;

}

/* Saat mouse diarahkan */
.stTabs [data-baseweb="tab"]:hover{

    background:#0f4c81 !important;

    color:white !important;

}

/* Tab aktif */
.stTabs [aria-selected="true"]{

    background:#082338 !important;

    color:white !important;

}

/* Paksa warna tulisan */
.stTabs [data-baseweb="tab"] p{

    color:inherit !important;

    font-weight:700;

}

div[data-testid="stPlotlyChart"]{

    border-radius:18px;

    overflow:hidden;

    box-shadow:0 8px 25px rgba(0,0,0,.15);

}

.stInfo{

    border-radius:15px;

}

.stSuccess{

    border-radius:15px;

}

.stMultiSelect{

    margin-bottom:15px;

}

.stSelectbox{

    margin-bottom:15px;

}

footer{

    visibility:hidden;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# JUDUL
# =====================================================

st.title("📊 Teknik Interaksi Visualisasi Data")

st.write(
"""
Contoh implementasi berbagai teknik interaksi visualisasi
menggunakan dataset **Sample Superstore**.
"""
)

# =====================================================
# DATASET
# =====================================================

df = pd.read_csv(
    "Sample - Superstore.csv",
    encoding="latin1"
)

df["Order Date"] = pd.to_datetime(df["Order Date"])

df["Month"] = df["Order Date"].dt.strftime("%b")

bulan = [
    "Jan","Feb","Mar","Apr",
    "May","Jun","Jul","Aug",
    "Sep","Oct","Nov","Dec"
]

df["Month"] = pd.Categorical(
    df["Month"],
    categories=bulan,
    ordered=True
)
# =====================================================
# TAB
# =====================================================

hover_tab, filter_tab, zoom_tab, drill_tab, map_tab = st.tabs([
    "🖱 Hover",
    "🔍 Filter",
    "🔎 Zoom",
    "📌 Drill-down",
    "🗺 Peta"
])

# =====================================================
# HOVER
# =====================================================

with hover_tab:

    st.markdown("## 🖱 Hover — Detail Tepat Saat Dibutuhkan")

    st.write(
        """
        Menyembunyikan nilai detail hingga pengguna mengarahkan
        kursor ke titik data. Teknik ini menjaga visual tetap bersih
        namun informasi lengkap tetap tersedia melalui **hover**.
        """
    )

    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True
    )

    fig.update_traces(
        line=dict(
            color="#11c5d9",
            width=4
        ),
        marker=dict(
            size=9,
            color="#11c5d9"
        ),
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Sales : <b>$%{y:,.2f}</b>" +
        "<extra></extra>"
    )

    fig.update_layout(

        height=480,

        paper_bgcolor="#082338",
        plot_bgcolor="#082338",

        font=dict(
            color="white",
            size=16
        ),

        hovermode="x unified",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            title="",
            showgrid=False
        ),

        yaxis=dict(
            title="Sales",
            gridcolor="#1d425d"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Arahkan kursor ke titik mana pun pada grafik untuk melihat detail penjualan."
    )

# =====================================================
# FILTER
# =====================================================

with filter_tab:

    st.markdown("## 🔍 Filter — Mempersempit Tanpa Menghapus Konteks")

    st.write(
        """
        Filter memungkinkan pengguna memfokuskan visualisasi
        pada kategori tertentu tanpa kehilangan konteks keseluruhan data.
        """
    )

    kategori = st.multiselect(
        "Pilih Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    region = st.multiselect(
        "Pilih Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    df_filter = df[
        (df["Category"].isin(kategori)) &
        (df["Region"].isin(region))
    ]

    sales = (
        df_filter
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s"
    )

    fig2.update_traces(

        hovertemplate=
        "<b>%{x}</b><br>" +
        "Sales : $%{y:,.2f}" +
        "<extra></extra>"

    )

    fig2.update_layout(

        height=500,

        paper_bgcolor="#082338",
        plot_bgcolor="#082338",

        font=dict(
            color="white",
            size=16
        ),

        showlegend=False,

        xaxis_title="",

        yaxis_title="Sales",

        yaxis=dict(
            gridcolor="#1d425d"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.caption(
        "Gunakan filter di atas untuk mengubah isi grafik."
    )

# =====================================================
# ZOOM
# =====================================================

with zoom_tab:

    st.markdown("## 🔎 Zoom — Fokus pada Detail Data")

    st.write(
        """
        Plotly menyediakan fitur zoom secara otomatis.
        Pengguna dapat melakukan **drag**, **scroll**, dan **pan**
        untuk melihat bagian tertentu dari grafik dengan lebih detail.
        """
    )

    monthly_sales = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.area(
        monthly_sales,
        x="Month",
        y="Sales"
    )

    fig3.update_traces(
        line=dict(
            color="#20d6c7",
            width=3
        ),
        fillcolor="rgba(32,214,199,0.35)",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Sales : $%{y:,.2f}<extra></extra>"
    )

    fig3.update_layout(

        height=500,

        paper_bgcolor="#082338",
        plot_bgcolor="#082338",

        font=dict(
            color="white",
            size=16
        ),

        hovermode="x unified",

        xaxis=dict(
            title="Month",
            showgrid=False
        ),

        yaxis=dict(
            title="Sales",
            gridcolor="#1d425d"
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "scrollZoom": True,
            "displaylogo": False
        }
    )

    st.info(
        "💡 Coba drag grafik untuk Zoom, double-click untuk kembali ke tampilan awal."
    )
# =====================================================
# DRILL DOWN
# =====================================================

with drill_tab:

    st.markdown("## 📌 Drill-down — Dari Category ke Sub-Category")

    st.write(
        """
        Drill-down memungkinkan pengguna berpindah dari data yang
        bersifat umum ke data yang lebih rinci.
        """
    )

    col1, col2 = st.columns([1,3])

    with col1:

        selected_category = st.selectbox(
            "Category",
            sorted(df["Category"].unique())
        )

    drill = (
        df[df["Category"] == selected_category]
        .groupby("Sub-Category", as_index=False)
        .agg({
            "Sales":"sum",
            "Profit":"sum"
        })
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    fig4 = px.bar(

        drill,

        x="Sub-Category",

        y="Sales",

        color="Profit",

        color_continuous_scale="Tealgrn",

        text_auto=".2s"

    )

    fig4.update_traces(

        hovertemplate=
        "<b>%{x}</b><br>" +
        "Sales : $%{y:,.2f}<br>" +
        "Profit : %{marker.color:,.2f}<extra></extra>"

    )

    fig4.update_layout(

        height=520,

        paper_bgcolor="#082338",

        plot_bgcolor="#082338",

        font=dict(
            color="white",
            size=16
        ),

        xaxis_title="",

        yaxis_title="Sales",

        yaxis=dict(
            gridcolor="#1d425d"
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================================
# MAP
# =====================================================

with map_tab:

    st.markdown("## 🗺️ Peta Persebaran Penjualan")

    st.write(
        """
        Visualisasi geografis memperlihatkan persebaran total
        penjualan pada setiap negara bagian di Amerika Serikat.
        """
    )

    state_sales = (
        df.groupby("State", as_index=False)["Sales"]
        .sum()
    )

    fig5 = px.scatter_geo(

        state_sales,

        locations="State",

        locationmode="USA-states",

        scope="usa",

        size="Sales",

        color="Sales",

        hover_name="State",

        color_continuous_scale="Tealgrn"

    )

    fig5.update_layout(

        height=650,

        paper_bgcolor="#082338",

        plot_bgcolor="#082338",

        font=dict(
            color="white",
            size=15
        ),

        geo=dict(

            bgcolor="#082338",

            lakecolor="#082338",

            landcolor="#082338",

            showland=True

        )
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.caption(
        "Ukuran lingkaran menunjukkan besarnya total penjualan pada masing-masing state."
    )

    st.divider()

st.markdown(
"""
<div style='text-align:center;
padding:20px;
color:gray;
font-size:15px;'>



</div>
""",
unsafe_allow_html=True
)
