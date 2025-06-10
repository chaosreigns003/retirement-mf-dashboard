
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("Comprehensive_Retirement_MF_Suitability_200Clients.xlsx")

st.set_page_config(page_title="Retirement MF Suitability Dashboard", layout="wide")

st.title("📊 Retirement-Oriented Mutual Fund Suitability Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Clients")
    age_range = st.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (30, 60))
    risk_profile = st.multiselect("Select Risk Profile", options=df["Risk Profile"].unique(), default=df["Risk Profile"].unique())
    fund_category = st.multiselect("Select Fund Category", options=df["Fund Category"].unique(), default=df["Fund Category"].unique())
    suitability_filter = st.radio("Suitability", ["All", "Yes", "No"], index=0)

# Filtered data
filtered_df = df[
    (df["Age"] >= age_range[0]) & 
    (df["Age"] <= age_range[1]) &
    (df["Risk Profile"].isin(risk_profile)) &
    (df["Fund Category"].isin(fund_category))
]

if suitability_filter != "All":
    filtered_df = filtered_df[filtered_df["Suitability"] == suitability_filter]

st.markdown(f"### Showing {len(filtered_df)} clients after filtering")

# Suitability distribution
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(filtered_df, names='Suitability', title="Suitability Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(filtered_df, x="Risk Profile", color="Suitability", barmode="group",
                        title="Risk Profile vs Suitability")
    st.plotly_chart(fig2, use_container_width=True)

# Fund Metrics Analysis
st.subheader("📈 Fund Metrics Analysis")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric("Avg. 3-Year CAGR", f"{filtered_df['Fund 3-Year CAGR (%)'].mean():.2f}%")

with metric_col2:
    st.metric("Avg. Sharpe Ratio", f"{filtered_df['Sharpe Ratio'].mean():.2f}")

with metric_col3:
    st.metric("Avg. Expense Ratio", f"{filtered_df['Expense Ratio (%)'].mean():.2f}%")

# Fund performance scatter
st.plotly_chart(
    px.scatter(filtered_df, x="Fund 3-Year CAGR (%)", y="Sharpe Ratio", 
               color="Suitability", hover_data=["Fund Name", "Risk Profile", "Fund Category"],
               title="Fund Performance: CAGR vs Sharpe Ratio"),
    use_container_width=True
)

# Show table
with st.expander("🔍 View Detailed Data Table"):
    st.dataframe(filtered_df)
