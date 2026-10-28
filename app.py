import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import linprog
import base64
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KPMG Capstone | Procurement Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FINAL DASHBOARD CSS
# ============================================================

st.markdown("""
<style>

/* HIDE STREAMLIT DEFAULT UI */

[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}


/* PAGE */

.stApp {
    background: #F3F7FC;
}

.block-container {
    max-width: 1550px;
    padding-top: 18px;
    padding-left: 24px;
    padding-right: 24px;
    padding-bottom: 30px;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #062B55 0%,
        #031D3A 100%
    );
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: white !important;
}


/* SIDEBAR BRAND */

.side-brand {
    font-size: 25px;
    font-weight: 800;
    color: white;
    letter-spacing: 0.5px;
}

.side-subtitle {
    color: #A9C9E8;
    font-size: 11px;
    margin-top: 4px;
}

.side-line {
    height: 3px;
    width: 80px;
    background: #4EB1FF;
    border-radius: 5px;
    margin-top: 10px;
    margin-bottom: 22px;
}


/* SIDEBAR NAVIGATION */

.nav-active {
    background: linear-gradient(
        90deg,
        #0879E6,
        #0563C5
    );

    color: white;
    padding: 11px 13px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 7px;
}

.nav-item {
    color: #D8E8F8;
    padding: 9px 13px;
    font-size: 13px;
    margin-bottom: 3px;
}


/* SIDEBAR INFO */

.side-info {
    margin-top: 25px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 10px;
    padding: 14px;
    color: #DCEBFA;
    font-size: 11px;
    line-height: 1.6;
}


/* HEADER */

.hero {
    background: linear-gradient(
        105deg,
        #082F62 0%,
        #0A568C 65%,
        #126FA5 100%
    );

    border-radius: 14px;
    padding: 22px 28px;
    min-height: 118px;

    box-shadow:
        0 5px 16px
        rgba(15, 60, 100, 0.12);
}

.hero-brand {
    color: #83C7FF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.hero-title {
    color: white;
    font-size: 29px;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 3px;
}

.hero-subtitle {
    color: #DCEEFF;
    font-size: 13px;
    margin-top: 7px;
}


/* HEADER STATUS */

.status-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 10px;
    padding: 13px 18px;
    text-align: center;
}

.status-label {
    color: #A9D8FF;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}

.status-value {
    color: white;
    font-size: 16px;
    font-weight: 800;
    margin-top: 3px;
}

.status-note {
    color: #D8EBFA;
    font-size: 9px;
    margin-top: 3px;
}


/* KPI CARDS */

.kpi-card {
    background: white;
    border: 1px solid #D8E5F2;
    border-radius: 12px;

    height: 122px;

    padding: 15px 17px;
    box-sizing: border-box;

    box-shadow:
        0 4px 12px
        rgba(25, 70, 110, 0.07);
}

.kpi-top {
    display: flex;
    align-items: center;
    gap: 9px;
}

.kpi-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;

    background: #DCEEFF;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 17px;
    font-weight: 800;

    color: #0A5EAA !important;

    opacity: 1 !important;
}

.kpi-label {
    color: #61758A;
    font-size: 11px;
    font-weight: 700;
}

.kpi-value {
    color: #082F62;
    font-size: 25px;
    font-weight: 800;
    margin-top: 11px;
}

.kpi-note {
    color: #18864D;
    font-size: 10px;
    font-weight: 700;
    margin-top: 3px;
}

.kpi-heading {
    color: #082F62;
    font-size: 13px;
    font-weight: 700;
    margin-top: 17px;
    margin-bottom: 8px;
}


/* TABLES */

[data-testid="stDataFrame"] {
    border-radius: 9px !important;
    overflow: hidden !important;
}


/* DOWNLOAD BUTTON */

.stDownloadButton button {
    background: #0877DF !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 700 !important;
}


/* EXPANDER */

[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D7E5F2 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] details summary,
[data-testid="stExpander"] details summary * {
    color: #082F62 !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] p,
[data-testid="stExpander"] span,
[data-testid="stExpander"] div,
[data-testid="stExpander"] li,
[data-testid="stExpander"] strong,
[data-testid="stExpander"] b,
[data-testid="stExpander"] label {
    color: #263F56 !important;
}

[data-testid="stExpander"] h1,
[data-testid="stExpander"] h2,
[data-testid="stExpander"] h3,
[data-testid="stExpander"] h4 {
    color: #082F62 !important;
    font-weight: 800 !important;
}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
    color: #263F56 !important;
}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] h4 {
    color: #082F62 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="side-brand">KPMG CAPSTONE</div>'
        '<div class="side-subtitle">'
        'Pomegranate Procurement Analytics'
        '</div>'
        '<div class="side-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-active">Dashboard</div>'
        '<div class="nav-item">Sourcing Plan</div>'
        '<div class="nav-item">Model Performance</div>'
        '<div class="nav-item">Assumptions</div>'
        '<div class="nav-item">Insights</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Procurement Settings")

    required_quantity = st.number_input(
        "Required Quantity (Tonnes)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )

    max_share = st.slider(
        "Maximum Share from One District (%)",
        min_value=20,
        max_value=100,
        value=50,
        step=5
    )

    usable_availability = st.slider(
        "Maximum Usable Market Availability (%)",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )

    st.markdown(
        '<div class="side-info">'
        '<b>ABOUT THIS TOOL</b><br><br>'
        'Decision-support prototype for pomegranate '
        'procurement using forecasting, logistics analysis '
        'and sourcing optimization.'
        '<br><br>'
        '<b>CORE DISTRICTS</b><br>'
        'Ahmednagar • Nashik • Pune • Sangli • Solapur'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================
# Load pomegranate banner image
banner_path = Path("4698df94-1724-45d7-9e27-a1b967f0f834.png")

with open(banner_path, "rb") as image_file:
    banner_base64 = base64.b64encode(
        image_file.read()
    ).decode()
header_html = (
    '<div style="'
    'position:relative;'
    'height:150px;'
    'border-radius:14px;'
    'overflow:hidden;'
    'background-image:'
    'linear-gradient(90deg, '
    'rgba(5,39,78,0.98) 0%, '
    'rgba(5,47,91,0.94) 35%, '
    'rgba(5,47,91,0.50) 62%, '
    'rgba(5,47,91,0.12) 100%), '
    f'url(data:image/png;base64,{banner_base64});'
    'background-size:cover;'
    'background-position:center;'
    'box-shadow:0 5px 16px rgba(15,60,100,0.14);'
    '">'

    '<div style="'
    'position:absolute;'
    'left:28px;'
    'top:20px;'
    'max-width:720px;'
    '">'

    '<div style="'
    'color:#83C7FF;'
    'font-size:11px;'
    'font-weight:800;'
    'letter-spacing:1.5px;'
    '">'
    'KPMG CAPSTONE'
    '</div>'

    '<div style="'
    'color:#FFFFFF;'
    'font-size:28px;'
    'font-weight:800;'
    'line-height:1.15;'
    'margin-top:4px;'
    '">'
    'Pomegranate Procurement Decision Support System'
    '</div>'

    '<div style="'
    'color:#E1F0FF;'
    'font-size:12px;'
    'margin-top:7px;'
    '">'
    'Data-driven sourcing for cost-efficient and reliable procurement'
    '</div>'

    '<div style="'
    'color:#D6E9FA;'
    'font-size:11px;'
    'margin-top:8px;'
    '">'
    'Price Forecasting &nbsp; • &nbsp; '
    'Availability Prediction &nbsp; • &nbsp; '
    'Logistics Cost Analysis &nbsp; • &nbsp; '
    'Procurement Optimization'
    '</div>'

    '</div>'

    '<div style="'
    'position:absolute;'
    'right:22px;'
    'top:28px;'
    'background:rgba(4,35,68,0.72);'
    'border:1px solid rgba(255,255,255,0.30);'
    'backdrop-filter:blur(4px);'
    'border-radius:10px;'
    'padding:13px 17px;'
    'text-align:center;'
    'min-width:155px;'
    '">'

    '<div style="'
    'color:#A9D8FF;'
    'font-size:8px;'
    'font-weight:700;'
    'letter-spacing:1px;'
    '">'
    'DECISION ENGINE'
    '</div>'

    '<div style="'
    'color:#FFFFFF;'
    'font-size:14px;'
    'font-weight:800;'
    'margin-top:4px;'
    '">'
    'OPTIMIZATION READY'
    '</div>'

    '<div style="'
    'color:#D8EBFA;'
    'font-size:9px;'
    'margin-top:4px;'
    '">'
    '5 sourcing districts'
    '</div>'

    '</div>'

    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


# ============================================================
# LOAD PROCUREMENT DATA
# ============================================================

@st.cache_data
def load_procurement_data():

    return pd.read_csv(
        "Final_Procurement_Recommendation.csv"
    )


data = load_procurement_data()


data = data.rename(
    columns={
        "District": "district",
        "Expected Landed Cost (₹/Tonne)": "landed_cost",
        "Predicted Arrivals (Tonnes)": "predicted_arrivals"
    }
)


district_data = data[
    [
        "district",
        "landed_cost",
        "predicted_arrivals"
    ]
].copy()


# ============================================================
# CALCULATE PROCUREMENT CAPACITY
# ============================================================

district_data["usable_capacity"] = (
    district_data["predicted_arrivals"]
    *
    usable_availability
    /
    100
)


max_quantity_per_district = (
    required_quantity
    *
    max_share
    /
    100
)


district_data["optimization_limit"] = np.minimum(
    district_data["usable_capacity"],
    max_quantity_per_district
)


total_available_capacity = (
    district_data["optimization_limit"].sum()
)


# ============================================================
# FEASIBILITY CHECK
# ============================================================

if total_available_capacity < required_quantity:

    st.error(
        f"Current settings can support only "
        f"{total_available_capacity:,.0f} tonnes, "
        f"while the requirement is "
        f"{required_quantity:,.0f} tonnes."
    )

    st.warning(
        "Increase usable market availability, increase "
        "maximum district share, or reduce required quantity."
    )

    st.stop()


# ============================================================
# RUN PROCUREMENT OPTIMIZATION
# ============================================================

optimization_result = linprog(

    c=district_data["landed_cost"].values,

    A_eq=[
        np.ones(
            len(district_data)
        )
    ],

    b_eq=[
        required_quantity
    ],

    bounds=[
        (0, limit)
        for limit in district_data["optimization_limit"]
    ],

    method="highs"
)


if not optimization_result.success:

    st.error(
        "The optimizer could not find "
        "a feasible sourcing plan."
    )

    st.stop()


district_data["recommended_quantity"] = (
    optimization_result.x
)


district_data["procurement_cost"] = (
    district_data["recommended_quantity"]
    *
    district_data["landed_cost"]
)


optimized_cost = (
    district_data["procurement_cost"].sum()
)


average_landed_cost = (
    optimized_cost
    /
    required_quantity
)


# ============================================================
# BENCHMARK & SAVINGS
# ============================================================

benchmark_quantity = (
    required_quantity
    /
    len(district_data)
)


benchmark_feasible = (
    benchmark_quantity
    <=
    district_data["usable_capacity"]
).all()


if benchmark_feasible:

    benchmark_cost = (
        district_data["landed_cost"]
        *
        benchmark_quantity
    ).sum()

    estimated_savings = (
        benchmark_cost
        -
        optimized_cost
    )

    savings_percentage = (
        estimated_savings
        /
        benchmark_cost
        *
        100
    )

else:

    benchmark_cost = np.nan
    estimated_savings = np.nan
    savings_percentage = np.nan


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="kpi-heading">'
    'PROCUREMENT OVERVIEW'
    '</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-top">'
        f'<div class="kpi-icon">📦</div>'
        f'<div class="kpi-label">Required Quantity</div>'
        f'</div>'
        f'<div class="kpi-value">'
        f'{required_quantity:,.0f} t'
        f'</div>'
        f'<div class="kpi-note">'
        f'Procurement requirement'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-top">'
        f'<div class="kpi-icon">◕</div>'
        f'<div class="kpi-label">Maximum District Share</div>'
        f'</div>'
        f'<div class="kpi-value">{max_share}%</div>'
        f'<div class="kpi-note">'
        f'Diversification constraint'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-top">'
        f'<div class="kpi-icon">📊</div>'
        f'<div class="kpi-label">Usable Availability</div>'
        f'</div>'
        f'<div class="kpi-value">'
        f'{usable_availability}%'
        f'</div>'
        f'<div class="kpi-note">'
        f'Of predicted arrivals'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        (
            '<div class="kpi-card">'
            '<div class="kpi-top">'
            '<div class="kpi-icon">₹</div>'
            '<div class="kpi-label">Optimized Cost</div>'
            '</div>'
            f'<div class="kpi-value">'
            f'₹{optimized_cost / 10000000:.2f} Cr'
            f'</div>'
            f'<div class="kpi-note">'
            f'₹{average_landed_cost:,.0f} per tonne'
            f'</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


with k5:

    if benchmark_feasible:

        savings_display = (
            f"₹{estimated_savings / 100000:.2f} L"
        )

        savings_note = (
            f"{savings_percentage:.1f}% vs benchmark"
        )

    else:

     savings_display = "N/A"
     savings_note = "Equal-allocation benchmark infeasible"

    st.markdown(
        (
            '<div class="kpi-card">'
            '<div class="kpi-top">'
            '<div class="kpi-icon">↓</div>'
            '<div class="kpi-label">Estimated Savings</div>'
            '</div>'
            f'<div class="kpi-value">'
            f'{savings_display}'
            f'</div>'
            f'<div class="kpi-note">'
            f'{savings_note}'
            f'</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


# ============================================================
# PREPARE RECOMMENDED SOURCING PLAN
# ============================================================

selected = district_data[
    district_data["recommended_quantity"] > 0.01
].copy()


selected["procurement_share"] = (
    selected["recommended_quantity"]
    /
    required_quantity
    *
    100
)


display_table = selected[
    [
        "district",
        "predicted_arrivals",
        "landed_cost",
        "usable_capacity",
        "recommended_quantity",
        "procurement_share"
    ]
].copy()


display_table.columns = [
    "District",
    "Predicted Arrivals",
    "Landed Cost ₹/Tonne",
    "Usable Capacity",
    "Recommended Tonnes",
    "Share %"
]


display_table = display_table.sort_values(
    "Recommended Tonnes",
    ascending=False
)


# ============================================================
# SOURCING PLAN SECTION
# ============================================================

st.markdown(
    "<div style='height:18px'></div>",
    unsafe_allow_html=True
)


st.markdown(
    '<div style="'
    'color:#082F62;'
    'font-size:20px;'
    'font-weight:800;'
    'margin-bottom:4px;'
    '">'
    'Recommended Sourcing Plan'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div style="'
    'color:#334E68;'
    'font-size:12px;'
    'font-weight:500;'
    'margin-bottom:12px;'
    '">'
    'Optimal allocation across sourcing districts based on '
    'expected landed cost, market availability and '
    'diversification constraints.'
    '</div>',
    unsafe_allow_html=True
)


st.dataframe(
    display_table.round(2),
    hide_index=True,
    use_container_width=True,
    height=150
)


download_data = (
    display_table
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    "Download Procurement Plan",
    data=download_data,
    file_name="Optimized_Procurement_Plan.csv",
    mime="text/csv"
)


# ============================================================
# PROCUREMENT ANALYSIS
# ============================================================

st.markdown(
    "<div style='height:15px'></div>",
    unsafe_allow_html=True
)


st.markdown(
    '<div style="'
    'color:#082F62;'
    'font-size:20px;'
    'font-weight:800;'
    'margin-bottom:12px;'
    '">'
    'Procurement Analysis'
    '</div>',
    unsafe_allow_html=True
)


chart1, chart2, chart3, chart4 = st.columns(4)


# ============================================================
# CHART 1 - PROCUREMENT ALLOCATION
# ============================================================

with chart1:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:16px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:5px;'
        '">'
        'Procurement Allocation'
        '</div>',
        unsafe_allow_html=True
    )

    allocation_colors = [
        "#0A5EAA",
        "#68B9EF",
        "#56A98A",
        "#F0AA58",
        "#8999AC"
    ]

    donut = go.Figure(
        data=[
            go.Pie(
                labels=display_table["District"],
                values=display_table["Recommended Tonnes"],
                hole=0.62,

                marker=dict(
                    colors=allocation_colors[
                        :len(display_table)
                    ]
                ),

                textinfo="percent",

                textfont=dict(
                    color="#17324D",
                    size=9
                ),

                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{value:.0f} tonnes<br>"
                    "%{percent}"
                    "<extra></extra>"
                )
            )
        ]
    )

    donut.update_layout(
        height=260,

        margin=dict(
            l=5,
            r=5,
            t=10,
            b=55
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Arial",
            color="#17324D",
            size=9
        ),

        showlegend=True,

        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.06,
            yanchor="top",

            font=dict(
                color="#17324D",
                size=8
            )
        ),

        annotations=[
            dict(
                text=(
                    f"<b>{required_quantity:,.0f}</b>"
                    "<br>tonnes"
                ),

                x=0.5,
                y=0.5,

                showarrow=False,

                font=dict(
                    color="#082F62",
                    size=12
                )
            )
        ]
    )

    st.plotly_chart(
        donut,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHART 2 - OPTIMIZED ALLOCATION
# ============================================================

with chart2:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:16px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:5px;'
        '">'
        'Optimized Allocation'
        '</div>',
        unsafe_allow_html=True
    )

    allocation_chart = go.Figure(
        data=[
            go.Bar(
                x=display_table["District"],

                y=display_table[
                    "Recommended Tonnes"
                ],

                text=display_table[
                    "Recommended Tonnes"
                ].round(0),

                textposition="outside",

                cliponaxis=False,

                marker_color="#4E9BD6"
            )
        ]
    )

    allocation_max = (
        display_table[
            "Recommended Tonnes"
        ].max()
    )

    allocation_chart.update_layout(
        height=260,

        margin=dict(
            l=35,
            r=10,
            t=25,
            b=40
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        showlegend=False,

        font=dict(
            color="#334E68",
            size=9
        )
    )

    allocation_chart.update_yaxes(
        title="Tonnes",

        range=[
            0,
            allocation_max * 1.25
        ],

        gridcolor="#E8EFF6",

        tickfont=dict(
            color="#334E68",
            size=8
        )
    )

    allocation_chart.update_xaxes(
        showgrid=False,

        tickfont=dict(
            color="#334E68",
            size=8
        )
    )

    st.plotly_chart(
        allocation_chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHART 3 - EXPECTED LANDED COST
# ============================================================

with chart3:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:16px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:5px;'
        '">'
        'Expected Landed Cost'
        '</div>',
        unsafe_allow_html=True
    )

    cost_data = (
        district_data
        .sort_values(
            "landed_cost"
        )
    )

    landed_chart = go.Figure(
        data=[
            go.Bar(
                x=cost_data["district"],
                y=cost_data["landed_cost"],

                text=cost_data[
                    "landed_cost"
                ].round(0),

                textposition="outside",

                cliponaxis=False,

                marker_color="#4E9BD6"
            )
        ]
    )

    landed_max = (
        cost_data[
            "landed_cost"
        ].max()
    )

    landed_chart.update_layout(
        height=260,

        margin=dict(
            l=40,
            r=10,
            t=25,
            b=40
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        showlegend=False,

        font=dict(
            color="#334E68",
            size=9
        )
    )

    landed_chart.update_yaxes(
        title="₹ / Tonne",

        range=[
            0,
            landed_max * 1.25
        ],

        gridcolor="#E8EFF6",

        tickfont=dict(
            color="#334E68",
            size=8
        )
    )

    landed_chart.update_xaxes(
        showgrid=False,

        tickfont=dict(
            color="#334E68",
            size=7
        )
    )

    st.plotly_chart(
        landed_chart,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHART 4 - COST COMPARISON
# ============================================================

with chart4:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:16px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:5px;'
        '">'
        'Cost Comparison'
        '</div>',
        unsafe_allow_html=True
    )

    if benchmark_feasible:

        comparison_chart = go.Figure(
            data=[
                go.Bar(
                    x=[
                        "Benchmark",
                        "Optimized"
                    ],

                    y=[
                        benchmark_cost / 10000000,
                        optimized_cost / 10000000
                    ],

                    text=[
                        f"₹{benchmark_cost / 10000000:.2f} Cr",
                        f"₹{optimized_cost / 10000000:.2f} Cr"
                    ],

                    textposition="outside",
                    cliponaxis=False,

                    marker_color=[
                        "#9BB9CE",
                        "#1A8395"
                    ]
                )
            ]
        )

        comparison_max = max(
            benchmark_cost / 10000000,
            optimized_cost / 10000000
        )

        comparison_chart.update_layout(
            height=260,

            margin=dict(
                l=35,
                r=10,
                t=25,
                b=40
            ),

            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            showlegend=False,

            font=dict(
                color="#334E68",
                size=9
            )
        )

        comparison_chart.update_yaxes(
            title="₹ Crore",

            range=[
                0,
                comparison_max * 1.25
            ],

            gridcolor="#E8EFF6",

            tickfont=dict(
                color="#334E68",
                size=8
            )
        )

        comparison_chart.update_xaxes(
            showgrid=False,

            tickfont=dict(
                color="#334E68",
                size=8
            )
        )

        st.plotly_chart(
            comparison_chart,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        benchmark_required_per_district = (
            required_quantity / len(district_data)
        )

        minimum_available_capacity = (
            district_data["usable_capacity"].min()
        )

        limiting_district = (
            district_data.loc[
                district_data["usable_capacity"].idxmin(),
                "district"
            ]
        )

        st.markdown(
            (
                '<div style="'
                'background:#FFFFFF;'
                'border:1px solid #D7E5F2;'
                'border-left:4px solid #E5A13B;'
                'border-radius:10px;'
                'padding:18px;'
                'margin-top:10px;'
                'min-height:185px;'
                'color:#17324D;'
                '">'

                '<div style="'
                'font-size:15px;'
                'font-weight:800;'
                'color:#082F62;'
                'margin-bottom:10px;'
                '">'
                'Benchmark Not Feasible'
                '</div>'

                '<div style="'
                'font-size:11px;'
                'line-height:1.6;'
                '">'

                f'At a requirement of <b>{required_quantity:,.0f} tonnes</b>, '
                f'equal allocation would require approximately '
                f'<b>{benchmark_required_per_district:,.0f} tonnes</b> '
                f'from each district.<br><br>'

                f'<b>{limiting_district}</b> has usable capacity of only '
                f'<b>{minimum_available_capacity:,.0f} tonnes</b> under '
                f'the current {usable_availability}% availability assumption.'

                '<br><br>'

                'The <b>optimized sourcing plan remains feasible</b>, '
                'but savings cannot be fairly calculated against an '
                'infeasible equal-allocation benchmark.'

                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    "<div style='height:18px'></div>",
    unsafe_allow_html=True
)


st.markdown(
    '<div style="'
    'color:#082F62;'
    'font-size:20px;'
    'font-weight:800;'
    'margin-bottom:12px;'
    '">'
    'Model Performance & Decision Insights'
    '</div>',
    unsafe_allow_html=True
)


price_performance = pd.DataFrame(
    {
        "Model": [
            "Baseline",
            "Linear Regression",
            "Random Forest",
            "Improved Random Forest"
        ],

        "MAE": [
            895.58,
            985.39,
            917.74,
            880.32
        ],

        "RMSE": [
            1141.86,
            1235.49,
            1186.78,
            1146.07
        ],

        "R²": [
            0.32,
            0.21,
            0.27,
            0.32
        ]
    }
)


arrival_performance = pd.DataFrame(
    {
        "Model": [
            "Baseline",
            "Linear Regression",
            "Random Forest"
        ],

        "MAE": [
            1299.01,
            1269.69,
            1234.80
        ],

        "RMSE": [
            2055.44,
            1795.96,
            1999.01
        ],

        "R²": [
            0.40,
            0.54,
            0.43
        ]
    }
)


cheapest_district = (
    district_data.loc[
        district_data[
            "landed_cost"
        ].idxmin(),
        "district"
    ]
)


highest_availability_district = (
    district_data.loc[
        district_data[
            "predicted_arrivals"
        ].idxmax(),
        "district"
    ]
)


model_col1, model_col2, insight_col = st.columns(
    [1.25, 1.25, 0.9]
)


# ============================================================
# PRICE MODEL
# ============================================================

with model_col1:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:17px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:8px;'
        '">'
        'Price Model Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        price_performance,
        hide_index=True,
        use_container_width=True,
        height=178
    )

    st.markdown(
        '<div style="'
        'background:#E8F7EF;'
        'border:1px solid #BDE5CE;'
        'border-radius:8px;'
        'padding:9px 12px;'
        'color:#17643A;'
        'font-size:11px;'
        'font-weight:700;'
        'text-align:center;'
        '">'
        'Selected Model: Improved Random Forest'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# ARRIVAL MODEL
# ============================================================

with model_col2:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:17px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:8px;'
        '">'
        'Arrival Model Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        arrival_performance,
        hide_index=True,
        use_container_width=True,
        height=178
    )

    st.markdown(
        '<div style="'
        'background:#E8F7EF;'
        'border:1px solid #BDE5CE;'
        'border-radius:8px;'
        'padding:9px 12px;'
        'color:#17643A;'
        'font-size:11px;'
        'font-weight:700;'
        'text-align:center;'
        '">'
        'Selected Model: Linear Regression'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

with insight_col:

    st.markdown(
        '<div style="'
        'color:#082F62;'
        'font-size:17px;'
        'font-weight:800;'
        'text-align:center;'
        'margin-bottom:8px;'
        '">'
        'Key Insights'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        (
            '<div style="'
            'background:#FFFFFF;'
            'border:1px solid #D7E5F2;'
            'border-left:4px solid #1677C8;'
            'border-radius:8px;'
            'padding:11px 12px;'
            'margin-bottom:8px;'
            'color:#17324D;'
            'font-size:11px;'
            'line-height:1.45;'
            '">'
            '<b>Lowest Expected Cost</b><br>'
            f'{cheapest_district} has the lowest '
            'expected landed cost.'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        (
            '<div style="'
            'background:#FFFFFF;'
            'border:1px solid #D7E5F2;'
            'border-left:4px solid #38A078;'
            'border-radius:8px;'
            'padding:11px 12px;'
            'margin-bottom:8px;'
            'color:#17324D;'
            'font-size:11px;'
            'line-height:1.45;'
            '">'
            '<b>Highest Availability</b><br>'
            f'{highest_availability_district} has the '
            'highest predicted market availability.'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    if benchmark_feasible:

        st.markdown(
            (
                '<div style="'
                'background:#FFFFFF;'
                'border:1px solid #D7E5F2;'
                'border-left:4px solid #E5A13B;'
                'border-radius:8px;'
                'padding:11px 12px;'
                'margin-bottom:8px;'
                'color:#17324D;'
                'font-size:11px;'
                'line-height:1.45;'
                '">'
                '<b>Estimated Cost Saving</b><br>'
                f'The optimized sourcing plan is estimated '
                f'to reduce procurement cost by '
                f'{savings_percentage:.1f}% versus the '
                'equal-allocation benchmark.'
                '</div>'
            ),
            unsafe_allow_html=True
        )


# ============================================================
# METHODOLOGY & ASSUMPTIONS
# ============================================================

st.markdown(
    "<div style='height:16px'></div>",
    unsafe_allow_html=True
)


st.markdown(
    '<div style="'
    'color:#082F62;'
    'font-size:20px;'
    'font-weight:800;'
    'margin-bottom:8px;'
    '">'
    'Methodology & Assumptions'
    '</div>',
    unsafe_allow_html=True
)


with st.expander(
    "View methodology, business assumptions and data notes"
):

    method_col1, method_col2, method_col3 = st.columns(3)

    with method_col1:

        st.markdown("### Forecasting")

        st.write(
            "**Price Model:** Improved Random Forest"
        )

        st.write(
            "**Arrival Model:** Linear Regression"
        )

        st.write(
            "Historical observations were evaluated "
            "using a chronological train/test approach "
            "to represent forecasting from past to future."
        )

    with method_col2:

        st.markdown("### Optimization")

        st.write(
            f"**Required Quantity:** "
            f"{required_quantity:,.0f} tonnes"
        )

        st.write(
            f"**Maximum District Share:** "
            f"{max_share}%"
        )

        st.write(
            f"**Usable Market Availability:** "
            f"{usable_availability}%"
        )

        st.write(
            "The optimization objective is to minimize "
            "expected landed procurement cost while "
            "meeting sourcing constraints."
        )

    with method_col3:

        st.markdown("### Cost & Benchmark")

        st.write(
            "**Expected Landed Cost = Predicted Commodity "
            "Cost + Estimated Freight Cost**"
        )

        st.write(
            "Savings are estimated against an "
            "equal-allocation sourcing benchmark."
        )

        st.write(
            "Predicted arrivals represent expected market "
            "availability and not guaranteed inventory."
        )

    st.divider()

    st.markdown("### Important Data Notes")

    st.write(
        "• Mandi, weather and rainfall information was "
        "integrated at the district-month level for modelling."
    )

    st.write(
        "• Missing historical months were not artificially "
        "filled with fabricated mandi-price observations."
    )

    st.write(
        "• Logistics and freight information is introduced "
        "at the procurement decision stage rather than being "
        "used as a core predictor of mandi price or arrivals."
    )

    st.write(
        "• The production-support dataset used elsewhere "
        "in the project is synthetic and is disclosed as such."
    )

    st.write(
        "• Usable availability and maximum district share "
        "are prototype business assumptions and can be "
        "changed from the sidebar."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<div style='height:10px'></div>",
    unsafe_allow_html=True
)


st.caption(
    "KPMG Capstone Project  |  "
    "Pomegranate Procurement Decision Support Prototype  |  "
    "Academic analysis only"
)
