import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Dashboard Superstore",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Dashboard Sample Superstore")
st.markdown("Dashboard interaktif menggunakan dataset **Sample Superstore**.")

# =====================================================
# MEMBACA DATA
# =====================================================

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Ubah Order Date menjadi format datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Tambahkan kolom bulan
df["MonthNum"] = df["Order Date"].dt.month
df["Month"] = df["Order Date"].dt.strftime("%b")

# =====================================================
# SIDEBAR FILTER
# =====================================================

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📊 Dashboard")

    st.markdown("---")

    st.markdown("""

### 👨‍🎓 Informasi
**Nama :** Raja Amar Siregar

**NPM :** 2024210111P

**Mata Kuliah :** Analisis Visualisasi Data

**Dataset :** Sample Superstore
""")

    st.markdown("---")

    st.subheader("🔎 Filter Data")

    region = st.multiselect(
        "🌍 Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.multiselect(
        "📦 Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    segment = st.multiselect(
        "👥 Segment",
        options=df["Segment"].unique(),
        default=df["Segment"].unique()
    )

# =====================================================
# FILTER DATA
# =====================================================

df_filter = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

# Ringkasan Sidebar

with st.sidebar:

    st.markdown("---")

    st.caption("© 2026 Dashboard Superstore by Raja")

# =====================================================
# KPI
# =====================================================

total_sales = df_filter["Sales"].sum()
total_profit = df_filter["Profit"].sum()
total_orders = len(df_filter)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)

st.divider()

# =====================================================
# VISUALISASI 1
# BAR CHART
# =====================================================

st.subheader("📊 Visualisasi 1 : Total Sales per Category")
st.success("✅ Fitur Interaktif : Hover & Zoom")

sales_category = (
    df_filter.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "count")
    )
    .reset_index()
)

fig = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    text_auto=".2s",
    title="Total Sales per Category",
    hover_data={
        "Sales": ":,.2f",
        "Profit": ":,.2f",
        "Orders": True
    }
)

fig.update_layout(
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# DATA UNTUK VISUALISASI 2
# =====================================================

monthly_sales = (
    df_filter.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

# =====================================================
# VISUALISASI 2
# LINE CHART
# =====================================================

st.subheader("📈 Visualisasi 2 : Sales Trend per Month")

st.success("✅ Fitur Interaktif : Hover & Zoom")

fig2 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
)

fig2.update_traces(
    line=dict(width=3),
    marker=dict(size=8),
    hovertemplate="<b>Bulan : %{x}</b><br>Total Sales : $%{y:,.2f}<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Sales ($)"
)

st.plotly_chart(fig2, use_container_width=True)


# =====================================================
# VISUALISASI 3
# DRILL DOWN
# =====================================================

st.subheader("📌 Visualisasi 3 : Drill Down Category → Sub-Category")

st.success("✅ Fitur Interaktif : Drill Down + Hover + Zoom")

selected_category = st.selectbox(
    "Pilih Category",
    df_filter["Category"].unique()
)

drill_data = (
    df_filter[df_filter["Category"] == selected_category]
    .groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    drill_data,
    x="Sub-Category",
    y="Sales",
    color="Sub-Category",
    text_auto=".2s",
    title=f"Sales Sub-Category ({selected_category})"
)

fig3.update_traces(
    hovertemplate="<b>%{x}</b><br>Sales : $%{y:,.2f}<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# DATA UNTUK MAPS
# =====================================================

state_sales = (
    df_filter.groupby("State")["Sales"]
    .sum()
    .reset_index()
)

# =====================================================
# VISUALISASI 4
# INTERACTIVE MAP
# =====================================================

st.subheader("🗺️ Visualisasi 4 : Sales by State")

st.success("✅ Fitur Interaktif : Hover + Zoom + Maps")

fig4 = px.scatter_geo(
    state_sales,
    locations="State",
    locationmode="USA-states",
    scope="usa",
    size="Sales",
    color="Sales",
    hover_name="State",
    title="Sales Distribution Across States"
)

fig4.update_layout(
    geo=dict(
        showland=True
    )
)

st.plotly_chart(fig4, use_container_width=True)



# =====================================================
# DATASET
# =====================================================

with st.expander("📄 Lihat Dataset"):
    st.dataframe(df_filter)