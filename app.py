# Import libraries including streamlit and other necessary packages
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Steel Plant Dashboard",
    page_icon="🏭",
    layout="wide"
)

# Title and description
st.title("Global Steel Plant Dashboard")
st.write(
    "Explore steel plants, company capacity, and LitPop exposure data."
)

# Load data
plants = pd.read_csv("dashboard_data/plants_litpop.csv")
companies = pd.read_csv("dashboard_data/company_summary.csv")

# Sidebar for filters
st.sidebar.header("Filters")

# Company selector
company_options = sorted(plants["Owner"].dropna().unique())
selected_companies = st.sidebar.multiselect(
    "Company",
    company_options
)

# Country filter
country_options = sorted(plants["Country/area"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Country",
    country_options
)

# Capacity range slider
min_capacity = float(plants["Total capacity (ttpa)"].min())
max_capacity = float(plants["Total capacity (ttpa)"].max())

capacity_range = st.sidebar.slider(
    "Capacity range",
    min_value=min_capacity,
    max_value=max_capacity,
    value=(min_capacity, max_capacity)
)

# Apply filters
filtered = plants[
    plants["Total capacity (ttpa)"].between(
        capacity_range[0],
        capacity_range[1]
    )
].copy()

if selected_companies:
    filtered = filtered[filtered["Owner"].isin(selected_companies)]

if selected_countries:
    filtered = filtered[filtered["Country/area"].isin(selected_countries)]

# Main content area
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Plants",
    len(filtered)
)

col2.metric(
    "Total Capacity",
    f"{filtered['Total capacity (ttpa)'].sum():,.0f} ttpa"
)

col3.metric(
    "Companies",
    filtered["Owner"].nunique()
)

# Interactive map
st.subheader("Steel Plant Map")

map_df = filtered.dropna(
    subset=["Latitude", "Longitude", "Total capacity (ttpa)", "LitPop_value"]
)

fig = px.scatter_geo(
    map_df,
    lat="Latitude",
    lon="Longitude",
    size="Total capacity (ttpa)",
    color="LitPop_value",
    hover_name="Plant name (English)",
    hover_data={
        "Owner": True,
        "Country/area": True,
        "Total capacity (ttpa)": ":,.0f",
        "LitPop_value": ":,.0f",
        "Latitude": False,
        "Longitude": False
    },
    size_max=30,
    title="Steel Plants by Capacity and LitPop Exposure"
)

fig.update_geos(
    showland=True,
    showcountries=True,
    showcoastlines=True,
    fitbounds="locations"
)

st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Plant Data")

# Data table
st.subheader("Plant Data")

table_data = filtered[
    [
        "Plant name (English)",
        "Owner",
        "Country/area",
        "Total capacity (ttpa)",
        "LitPop_value"
    ]
]

st.markdown(
    table_data.head(100).to_html(index=False),
    unsafe_allow_html=True
)

# Footer
st.divider()
st.caption(
    "Data sources: Global steel plant data and LitPop exposure data."
)