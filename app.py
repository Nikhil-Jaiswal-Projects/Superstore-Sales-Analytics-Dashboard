
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    df["Year"] = df["Order Date"].dt.year

    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Year"].isin(selected_year)) &
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📊 Superstore Analytics Dashboard")
st.markdown("---")

# -----------------------------
# KPI Section
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "Orders",
    total_orders
)

col4.metric(
    "Average Sale",
    f"${avg_sales:,.0f}"
)

st.markdown("---")

# -----------------------------
# Sales Trend
# -----------------------------
st.subheader("📈 Sales Trend")

sales_trend = (
    filtered_df
    .groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

fig_sales = px.line(
    sales_trend,
    x="Year",
    y="Sales",
    markers=True,
    title="Yearly Sales Trend"
)

st.plotly_chart(
    fig_sales,
    use_container_width=True
)

# -----------------------------
# Region Charts
# -----------------------------
col5, col6 = st.columns(2)

with col5:

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region_sales = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region_sales,
        use_container_width=True
    )

with col6:

    region_profit = (
        filtered_df
        .groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig_region_profit = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig_region_profit,
        use_container_width=True
    )

# -----------------------------
# Category & Top States
# -----------------------------
col7, col8 = st.columns(2)

with col7:

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Category Sales"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col8:

    top_states = (
        filtered_df
        .groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_states = px.bar(
        top_states,
        x="State",
        y="Sales",
        title="Top 10 States by Sales"
    )

    st.plotly_chart(
        fig_states,
        use_container_width=True
    )

# -----------------------------
# YoY Growth Chart
# -----------------------------
st.subheader("📊 Year-over-Year Growth")

yearly_sales = (
    filtered_df
    .groupby("Year")["Sales"]
    .sum()
)

yoy_growth = (
    yearly_sales
    .pct_change()
    * 100
)

yoy_df = yoy_growth.reset_index()
yoy_df.columns = ["Year", "Growth"]

fig_yoy = px.line(
    yoy_df,
    x="Year",
    y="Growth",
    markers=True,
    title="YoY Growth (%)"
)

st.plotly_chart(
    fig_yoy,
    use_container_width=True
)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

