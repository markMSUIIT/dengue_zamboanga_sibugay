"""
Dengue Epidemiological Surveillance System
Zamboanga Sibugay Province
Main Landing Page
"""

import streamlit as st
import pandas as pd
from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header

# Page configuration
st.set_page_config(
    page_title="Dengue Surveillance System - Zamboanga Sibugay",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply shared styles
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Custom CSS to hide default page name and style navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        padding-top: 0rem;
    }
    [data-testid="stSidebarNav"]::before {
        content: "";
        display: block;
        margin-bottom: 0;
    }
    /* Style the first nav item */
    [data-testid="stSidebarNav"] li:first-child a span {
        visibility: hidden;
    }
    [data-testid="stSidebarNav"] li:first-child a::after {
        content: "Welcome";
        visibility: visible;
        position: absolute;
        left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Title card at TOP first
with st.sidebar:
    # Put the branding header first (before navigation)
    st.markdown(render_sidebar_header(), unsafe_allow_html=True)

# Main Header
st.markdown(render_header(
    title="Dengue Epidemiological Surveillance System",
    subtitle="Interactive Analytics Dashboard for Public Health Decision Support",
    badge="Zamboanga Sibugay Province"
), unsafe_allow_html=True)

# Load data for quick stats
@st.cache_data
def load_quick_stats():
    try:
        df = pd.read_csv('sibugay_dengue_cases_dataset.csv')
        total_cases = df['CASES'].sum()
        municipalities = df['MUNICIPALITY'].nunique()
        years = f"{int(df['YEAR_2'].min()) + 2000} - {int(df['YEAR_2'].max()) + 2000}"
        records = len(df)
        return total_cases, municipalities, years, records
    except:
        return 0, 0, "N/A", 0

total_cases, municipalities, years, records = load_quick_stats()

# Welcome Section
st.markdown(render_section_header("Welcome"), unsafe_allow_html=True)

st.markdown("""
This comprehensive surveillance dashboard provides **real-time analytics** and **predictive insights** 
for dengue epidemiology in Zamboanga Sibugay Province. Developed as part of thesis research, 
this system integrates epidemiological data with environmental variables to support evidence-based 
public health decision-making.
""")

# Quick Stats
st.markdown(render_section_header("Quick Statistics"), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Cases",
        value=f"{total_cases:,.0f}",
        delta="All time"
    )

with col2:
    st.metric(
        label="Municipalities",
        value=municipalities,
        delta="Coverage"
    )

with col3:
    st.metric(
        label="Data Period",
        value=years,
        delta="13 years"
    )

with col4:
    st.metric(
        label="Records",
        value=f"{records:,}",
        delta="Observations"
    )

# Features Section
st.markdown(render_section_header("Dashboard Features"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Descriptive Analysis</div>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Explore dengue case distributions across municipalities, time periods, 
            and environmental conditions. Interactive choropleth maps and temporal 
            trend visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">📝 Data Entry</div>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Administrative interface for entering weekly dengue case reports. 
            Supports data validation and CSV export for continuous surveillance.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔮 Predictive Analysis</div>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Advanced forecasting using Negative Binomial and Zero-Inflated 
            Negative Binomial regression models. Risk stratification and 
            outbreak prediction capabilities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">ℹ️ Project Information</div>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Detailed documentation including methodology, data dictionary, 
            team information, and academic references.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Methodology Preview
st.markdown(render_section_header("Analytical Approach"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
        <div class="card-title" style="text-align: center;">Negative Binomial</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            Count regression model for overdispersed data accounting for 
            variance exceeding the mean.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <div class="card-title" style="text-align: center;">Zero-Inflated NB</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            Extended model handling excess zeros common in epidemiological 
            surveillance data.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🗺️</div>
        <div class="card-title" style="text-align: center;">Spatiotemporal</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            Choropleth mapping with municipality-level risk assessment 
            and temporal trend analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Getting Started
st.markdown(render_section_header("Getting Started"), unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>How to use this dashboard:</strong><br>
    Use the <strong>sidebar navigation</strong> to access different modules. Start with 
    <strong>Descriptive Analysis</strong> for an overview of the data, then explore 
    <strong>Predictive Analysis</strong> for forecasting and risk assessment.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(render_footer(), unsafe_allow_html=True)
