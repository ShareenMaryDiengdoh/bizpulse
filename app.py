import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data
DATA_PATH = "data/bizpulse_data.csv"
Z_ANOMALY_PATH = "output/revenue_anomalies.csv"
IF_ANOMALY_PATH = "output/iforest_anomalies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
    z_anom = pd.read_csv(Z_ANOMALY_PATH, parse_dates=['Date']) if os.path.exists(Z_ANOMALY_PATH) else pd.DataFrame()
    if_anom = pd.read_csv(IF_ANOMALY_PATH, parse_dates=['Date']) if os.path.exists(IF_ANOMALY_PATH) else pd.DataFrame()
    return df, z_anom, if_anom

df, z_anomalies, if_anomalies = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filter Data")
regions = st.sidebar.multiselect("Select Region(s):", df['Region'].unique(), default=df['Region'].unique())
products = st.sidebar.multiselect("Select Product(s):", df['Business_Unit'].unique(), default=df['Business_Unit'].unique())

filtered_df = df[(df['Region'].isin(regions)) & (df['Business_Unit'].isin(products))]

# --- Dashboard Header ---
st.title("📊 BizPulse – Business Health & Risk Analyzer")
st.markdown("Real-time performance insights and anomaly detection for business KPIs.")

# --- KPI Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("📈 Avg. Profit", f"${filtered_df['Profit'].mean():,.0f}")
col3.metric("🚨 Anomalies (ML)", f"{len(if_anomalies)} points")

# --- Time Series Plot ---
st.subheader("📉 Revenue Trend Over Time")
fig1 = px.line(filtered_df, x='Date', y='Revenue', color='Region', title="Revenue Trend")
st.plotly_chart(fig1, use_container_width=True)

# --- Anomaly Overlay ---
st.subheader("🚨 Anomaly Detection Overlay")
fig2 = px.line(df, x='Date', y='Revenue', color='Region', title="Revenue with ML Anomalies")
if not if_anomalies.empty:
    fig2.add_scatter(x=if_anomalies['Date'], y=if_anomalies['Revenue'],
                     mode='markers', name='ML Anomaly', marker=dict(color='red', size=6))
st.plotly_chart(fig2, use_container_width=True)

# --- Profit by Region ---
st.subheader("💼 Profit Distribution by Region")
fig3 = px.box(filtered_df, x='Region', y='Profit', color='Region', title="Profit Distribution")
st.plotly_chart(fig3, use_container_width=True)

# --- Download Option ---
st.subheader("📥 Download Detected Anomalies")
if not if_anomalies.empty:
    st.download_button("Download ML Anomalies CSV", data=if_anomalies.to_csv(index=False), file_name="iforest_anomalies.csv")
