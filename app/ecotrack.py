import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="EcoTrack AI",
    page_icon="🌱",
    layout="wide"
)

# =====================================================
# CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071b19, #102c27);
    color: #e8f5e9;
}

section[data-testid="stSidebar"] {
    background-color: #0b211e;
}

h1, h2, h3 {
    color: #a5e6b2 !important;
}

div[data-testid="stMetric"] {
    background: #153b32;
    border: 1px solid #28634e;
    padding: 18px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #c5e8d0;
}

.stButton button {
    background-color: #24865c;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("🌱 EcoTrack AI")

st.subheader(
    "AI-Powered Sustainable Inventory & Waste Reduction System"
)

st.caption(
    "Smarter demand forecasting | Surplus monitoring | "
    "Responsible inventory management"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/raw/supply_chain_dataset1.csv"
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Units_Sold",
        "Inventory_Level",
        "Demand_Forecast",
        "Reorder_Point",
        "Order_Quantity",
        "Unit_Cost"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    return df


try:
    df = load_data()
except Exception as error:
    st.error(f"Dataset loading failed: {error}")
    st.stop()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("🌿 EcoTrack Controls")

regions = ["All"] + sorted(
    df["Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

skus = ["All"] + sorted(
    df["SKU_ID"].dropna().unique().tolist()
)

selected_sku = st.sidebar.selectbox(
    "Select Product SKU",
    skus
)

filtered = df.copy()

if selected_region != "All":
    filtered = filtered[
        filtered["Region"] == selected_region
    ]

if selected_sku != "All":
    filtered = filtered[
        filtered["SKU_ID"] == selected_sku
    ]

if filtered.empty:
    st.warning("No records found for these filters.")
    st.stop()

# =====================================================
# LATEST INVENTORY SNAPSHOT
# =====================================================

latest_snapshot = (
    filtered.dropna(subset=["Date"])
    .sort_values("Date")
    .drop_duplicates(
        subset=["SKU_ID", "Warehouse_ID"],
        keep="last"
    )
    .copy()
)

if latest_snapshot.empty:
    st.error("No valid dated inventory records found.")
    st.stop()

# =====================================================
# SURPLUS AND RISK CALCULATIONS
# =====================================================

# Assumption: Demand_Forecast represents daily demand.
# Initial planning target: 30 days of stock coverage.
COVERAGE_DAYS = 30

latest_snapshot["Target_Stock"] = (
    latest_snapshot["Demand_Forecast"].clip(lower=0)
    * COVERAGE_DAYS
)

latest_snapshot["Potential_Surplus"] = (
    latest_snapshot["Inventory_Level"]
    - latest_snapshot["Target_Stock"]
).clip(lower=0)

latest_snapshot["Surplus_Value"] = (
    latest_snapshot["Potential_Surplus"]
    * latest_snapshot["Unit_Cost"]
)

latest_snapshot["Stock_Coverage_Ratio"] = (
    latest_snapshot["Inventory_Level"]
    / latest_snapshot["Target_Stock"].clip(lower=1)
)

latest_snapshot["Risk_Level"] = "Low"

latest_snapshot.loc[
    latest_snapshot["Stock_Coverage_Ratio"] > 1,
    "Risk_Level"
] = "Medium"

latest_snapshot.loc[
    latest_snapshot["Stock_Coverage_Ratio"] > 1.5,
    "Risk_Level"
] = "High"

# =====================================================
# DASHBOARD TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Risk Analysis",
    "Smart Recommendations",
    "What-If Simulation"
])

# =====================================================
# TAB 1: OVERVIEW
# =====================================================

with tab1:
    st.markdown("## 🌱 Inventory Sustainability Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Latest Inventory",
        f"{latest_snapshot['Inventory_Level'].sum():,.0f} units"
    )

    col2.metric(
        "Potential Surplus",
        f"{latest_snapshot['Potential_Surplus'].sum():,.0f} units"
    )

    col3.metric(
        "High-Risk Records",
        int((latest_snapshot["Risk_Level"] == "High").sum())
    )

    col4.metric(
        "Potential Surplus Value",
        f"₹{latest_snapshot['Surplus_Value'].sum():,.2f}"
    )

    st.info(
        "Planning assumption: target stock is based on "
        "30 days of forecast demand. Potential surplus is "
        "an estimate, not confirmed waste."
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            latest_snapshot,
            x="SKU_ID",
            y=["Inventory_Level", "Target_Stock"],
            title="Current Inventory vs Target Stock",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        risk_counts = latest_snapshot["Risk_Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Records"]

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Records",
            title="Inventory Risk Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Latest Inventory Details")

    st.dataframe(
        latest_snapshot[
            [
                "SKU_ID",
                "Warehouse_ID",
                "Inventory_Level",
                "Demand_Forecast",
                "Target_Stock",
                "Potential_Surplus",
                "Risk_Level"
            ]
        ],
        use_container_width=True
    )

# =====================================================
# TAB 2: RISK ANALYSIS
# =====================================================

with tab2:
    st.markdown("## Potential Surplus Risk Analysis")

    st.info(
        "Risk is calculated by comparing latest inventory "
        "with forecasted demand. It indicates potential "
        "surplus, not confirmed waste."
    )

    risk_filter = st.selectbox(
        "Choose Risk Category",
        ["All", "High", "Medium", "Low"]
    )

    risk_data = latest_snapshot.copy()

    if risk_filter != "All":
        risk_data = risk_data[
            risk_data["Risk_Level"] == risk_filter
        ]

    st.metric(
        "Records in Selected Risk Category",
        len(risk_data)
    )

    st.dataframe(
        risk_data[
            [
                "Date",
                "SKU_ID",
                "Warehouse_ID",
                "Region",
                "Inventory_Level",
                "Demand_Forecast",
                "Potential_Surplus",
                "Surplus_Value",
                "Risk_Level"
            ]
        ].sort_values(
            "Potential_Surplus",
            ascending=False
        ),
        use_container_width=True
    )

    risk_csv = risk_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Risk Analysis",
        data=risk_csv,
        file_name="ecotrack_risk_analysis.csv",
        mime="text/csv"
    )

# =====================================================
# TAB 3: SMART RECOMMENDATIONS
# =====================================================

with tab3:
    st.markdown("## 🤖 Smart Inventory Recommendations")

    st.info(
        "These recommendations are based on the estimated "
        "30-day stock coverage target."
    )

    summary = latest_snapshot[
        [
            "SKU_ID",
            "Warehouse_ID",
            "Inventory_Level",
            "Demand_Forecast",
            "Reorder_Point",
            "Stock_Coverage_Ratio",
            "Potential_Surplus",
            "Surplus_Value"
        ]
    ].copy()

    summary = summary.rename(
        columns={
            "Inventory_Level": "Current_Inventory",
            "Demand_Forecast": "Forecasted_Demand"
        }
    )

    def recommend(row):
        if row["Stock_Coverage_Ratio"] > 1.5:
            return "High Stock - Review New Orders"
        elif row["Stock_Coverage_Ratio"] > 1:
            return "Moderate Surplus - Monitor Stock"
        elif row["Current_Inventory"] < row["Reorder_Point"]:
            return "Low Stock - Consider Replenishment"
        else:
            return "Stock Level - Monitor Regularly"

    summary["Recommendation"] = summary.apply(
        recommend,
        axis=1
    )

    # Additional sustainability action suggestions
    def sustainability_action(row):
        if row["Potential_Surplus"] > 0:
            return "Review redistribution, discounts or future orders"
        elif row["Current_Inventory"] < row["Reorder_Point"]:
            return "Plan replenishment based on demand"
        else:
            return "Maintain stock and monitor demand"

    summary["Sustainability_Action"] = summary.apply(
        sustainability_action,
        axis=1
    )

    st.dataframe(
        summary,
        use_container_width=True
    )

    recommendation_csv = summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Smart Recommendations",
        data=recommendation_csv,
        file_name="ecotrack_recommendations.csv",
        mime="text/csv"
    )

# =====================================================
# CLIMATE ACTION SECTION
# =====================================================

st.divider()

st.markdown("## 🌍 Our Climate Action Goal")

st.write(
    "EcoTrack AI aims to support sustainable inventory "
    "management through better demand planning and "
    "responsible stock decisions."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Our Objectives")

    st.write("""
    - Identify potential excess inventory.
    - Support demand-based replenishment.
    - Reduce avoidable over-ordering.
    - Encourage better use of existing stock.
    """)

with col2:
    st.markdown("### Expected Benefits")

    st.write("""
    - Better inventory visibility.
    - Improved stock planning.
    - Reduced risk of surplus accumulation.
    - Support for responsible business decisions.
    """)

st.success(
    "Supporting UN Sustainable Development Goal 13: Climate Action"
)

st.caption(
    "EcoTrack AI | Sustainable Inventory Intelligence"
)

# =====================================================
# TAB 4: WHAT-IF SIMULATION
# =====================================================

with tab4:
    st.markdown("## 🌍 Surplus Reduction Simulation")

    st.write(
        "Explore the possible impact of reducing estimated "
        "surplus inventory."
    )

    reduction = st.slider(
        "Assumed Surplus Reduction (%)",
        min_value=0,
        max_value=50,
        value=20,
        step=5
    )

    total_units = latest_snapshot["Potential_Surplus"].sum()
    total_value = latest_snapshot["Surplus_Value"].sum()

    estimated_units = total_units * reduction / 100
    estimated_value = total_value * reduction / 100

    col1, col2 = st.columns(2)

    col1.metric(
        "Illustrative Units",
        f"{estimated_units:,.0f}"
    )

    col2.metric(
        "Illustrative Stock Value",
        f"₹{estimated_value:,.2f}"
    )

    st.progress(reduction / 100)

    st.warning(
        "This is a hypothetical simulation, not measured "
        "waste prevention or carbon-emission reduction."
    )
