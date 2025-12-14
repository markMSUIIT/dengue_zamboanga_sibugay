"""
Project Information Module
Dengue Surveillance System - Zamboanga Sibugay
"""

import streamlit as st
import pandas as pd
import sys
sys.path.append('..')

try:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header
except:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header

# Page configuration
st.set_page_config(
    page_title="Project Information - Dengue Surveillance",
    page_icon="ℹ️",
    layout="wide"
)

# Apply shared styles
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(render_sidebar_header(), unsafe_allow_html=True)
    st.markdown("### Contents")
    st.markdown("""
    - About
    - Methodology
    - Data Dictionary
    - Team
    - References
    """)

# Header
st.markdown(render_header(
    title="Project Information",
    subtitle="Documentation, methodology, and research details",
    badge="Documentation"
), unsafe_allow_html=True)

# About Section
st.markdown(render_section_header("About This Project"), unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <p style="color: #374151; line-height: 1.7; margin: 0;">
        This dashboard is developed as part of <strong>thesis research</strong> on dengue epidemiology 
        in <strong>Zamboanga Sibugay Province</strong>, Philippines. It integrates epidemiological 
        surveillance data with environmental variables to support evidence-based public health 
        decision-making and outbreak prediction.
    </p>
</div>
""", unsafe_allow_html=True)

# Research Team
st.markdown(render_section_header("Research Team"), unsafe_allow_html=True)

col_team1, col_team2 = st.columns(2)

with col_team1:
    st.markdown("""
    <div class="card" style="text-align: center; border-left: 4px solid #667eea;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👨‍💻</div>
        <div class="card-title" style="text-align: center; color: #667eea;">Lead Researcher</div>
        <p style="color: #1F2937; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">
            Brent Jason M. Dequina
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            BS Information Systems Student
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_team2:
    st.markdown("""
    <div class="card" style="text-align: center; border-left: 4px solid #764ba2;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👨‍🏫</div>
        <div class="card-title" style="text-align: center; color: #764ba2;">Thesis Advisor</div>
        <p style="color: #1F2937; font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">
            Assoc. Prof. Joseph C. Sieras, MSc.
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">
            Faculty Advisor
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features Section
st.markdown(render_section_header("System Features"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <div class="card-title" style="text-align: center;">Descriptive Analytics</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            Spatiotemporal mapping, trend analysis, and environmental correlation
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔮</div>
        <div class="card-title" style="text-align: center;">Predictive Modeling</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            NB and ZINB regression for outbreak forecasting
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🗺️</div>
        <div class="card-title" style="text-align: center;">Risk Assessment</div>
        <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">
            Municipality-level risk stratification and hotspot identification
        </p>
    </div>
    """, unsafe_allow_html=True)

# Methodology
st.markdown(render_section_header("Methodology"), unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Data Collection", "Statistical Models", "Evaluation"])

with tab1:
    st.markdown("""
    ### Data Sources
    
    | Source | Description | Variables |
    |--------|-------------|-----------|
    | DOH-IHSS | Integrated Health Surveillance System | Weekly dengue cases by municipality |
    | NASA POWER | Meteorological data API | Temperature, humidity, precipitation |
    | GADM | Administrative boundaries | Municipality polygons |
    
    ### Data Processing
    
    1. **Temporal Aggregation**: Weekly case counts by municipality
    2. **Spatial Integration**: Linking cases to geographic boundaries
    3. **Feature Engineering**: Lag variables, rolling averages
    4. **Quality Control**: Missing value handling, outlier detection
    """)

with tab2:
    st.markdown("""
    ### Negative Binomial (NB) Regression
    
    Appropriate for overdispersed count data where the variance exceeds the mean.
    The probability mass function is:
    
    $$P(Y = y) = \\binom{y + r - 1}{y} p^r (1-p)^y$$
    
    **Advantages:**
    - Handles overdispersion in case counts
    - Accounts for clustering during outbreaks
    - Well-established in epidemiological research
    
    ### Zero-Inflated Negative Binomial (ZINB)
    
    Extends NB to handle excess zeros in the data:
    
    $$P(Y = 0) = \\pi + (1-\\pi) \\cdot NB(0)$$
    $$P(Y = y) = (1-\\pi) \\cdot NB(y), \\quad y > 0$$
    
    **Advantages:**
    - Models structural zeros (true absence of disease)
    - Better fit for sparse surveillance data
    - Separate processes for zero and count generation
    """)

with tab3:
    st.markdown("""
    ### Model Evaluation
    
    **Train/Test Split**: 80% training, 20% testing
    
    | Metric | Description | Interpretation |
    |--------|-------------|----------------|
    | MSE | Mean Squared Error | Average squared prediction error |
    | RMSE | Root MSE | Error in original units |
    | MAE | Mean Absolute Error | Average absolute deviation |
    | MASE | Mean Absolute Scaled Error | Relative to naive forecast |
    | Accuracy | Within ±20% tolerance | Practical prediction accuracy |
    
    ### Feature Variables
    
    - **Time Index**: Captures secular trends
    - **Lag-1**: Previous week's case count
    - **Rolling Mean (4 weeks)**: Smoothed recent average
    """)

# Data Dictionary
st.markdown(render_section_header("Data Dictionary"), unsafe_allow_html=True)

data_dict = pd.DataFrame({
    'Variable': ['MUNICIPALITY', 'YEAR_2', 'MONTH', 'QUARTER', 'MORBIDITY_WEEK', 
                 'CASES', 'T2M_MAX', 'T2M_MIN', 'RH2M', 'PRECTOTCORR', 'geometry'],
    'Type': ['String', 'Integer', 'Integer', 'Integer', 'Integer', 
             'Integer', 'Float', 'Float', 'Float', 'Float', 'WKT'],
    'Description': [
        'Municipality name in Zamboanga Sibugay',
        'Year of observation (2-digit: 11=2011)',
        'Month of observation (1-12)',
        'Quarter of observation (1-4)',
        'Epidemiological week (1-52)',
        'Number of confirmed dengue cases',
        'Maximum temperature at 2m (°C)',
        'Minimum temperature at 2m (°C)',
        'Relative humidity at 2m (%)',
        'Corrected precipitation (mm)',
        'Municipality boundary polygon (MULTIPOLYGON)'
    ]
})

st.dataframe(data_dict, use_container_width=True, hide_index=True)

# References
st.markdown(render_section_header("References"), unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <ol style="color: #374151; line-height: 2; margin: 0; padding-left: 1.5rem;">
        <li>World Health Organization. (2023). <em>Dengue and Severe Dengue Fact Sheet.</em></li>
        <li>Department of Health, Philippines. <em>National Dengue Prevention and Control Program.</em></li>
        <li>Cameron, A. C., & Trivedi, P. K. (2013). <em>Regression Analysis of Count Data.</em> Cambridge University Press.</li>
        <li>Lambert, D. (1992). Zero-inflated Poisson regression. <em>Technometrics</em>, 34(1), 1-14.</li>
        <li>NASA POWER Project. <em>Meteorological Data API.</em> https://power.larc.nasa.gov/</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Citation
st.markdown(render_section_header("Citation"), unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>How to cite this work:</strong><br><br>
    Dequina, B. J. M. (2024). <em>Dengue Epidemiological Surveillance System for Zamboanga Sibugay: 
    Spatiotemporal Analysis and Predictive Modeling using Negative Binomial Regression.</em> 
    Undergraduate Thesis.
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="warning-box" style="margin-top: 2rem;">
    <strong>Disclaimer:</strong> This dashboard is developed for academic and research purposes only. 
    Official health guidance should be obtained from the Department of Health or local health authorities.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(render_footer(), unsafe_allow_html=True)
