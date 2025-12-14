"""
Descriptive Analysis Module
Dengue Surveillance System - Zamboanga Sibugay
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import sys
sys.path.append('..')

try:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box
except:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box

# Try imports for mapping
try:
    from shapely import wkt
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Descriptive Analysis - Dengue Surveillance",
    page_icon="📊",
    layout="wide"
)

# Apply shared styles
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Data loading
@st.cache_data
def load_data():
    df = pd.read_csv('sibugay_dengue_cases_dataset.csv')
    # Convert columns
    numeric_cols = ['YEAR_2', 'MONTH', 'WEEK', 'QUARTER', 'CASES', 'MORBIDITY_WEEK', 
                    'T2M_MAX', 'T2M_MIN', 'RH2M', 'PRECTOTCORR']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df[df['QUARTER'].isin([1, 2, 3, 4])]
    return df

@st.cache_data
def load_geojson():
    if not GEOPANDAS_AVAILABLE:
        return None
    try:
        df = pd.read_csv('sibugay_dengue_cases_dataset.csv')
        muni_geo = df.drop_duplicates(subset=['MUNICIPALITY'])[['MUNICIPALITY', 'geometry']].copy()
        muni_geo['geometry'] = muni_geo['geometry'].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(muni_geo, geometry='geometry', crs="EPSG:4326")
        geojson = json.loads(gdf.to_json())
        return geojson
    except:
        return None

# Load data
df = load_data()
geojson = load_geojson()

# Sidebar
with st.sidebar:
    st.markdown(render_sidebar_header(), unsafe_allow_html=True)
    
    st.markdown("### Filters")
    
    # Municipality filter
    municipalities = sorted(df['MUNICIPALITY'].dropna().unique())
    selected_municipality = st.multiselect(
        "Municipality",
        municipalities,
        default=municipalities,
        key="desc_municipality"
    )
    
    # Year range
    min_year = int(df['YEAR_2'].min())
    max_year = int(df['YEAR_2'].max())
    year_range = st.slider(
        "Year Range",
        min_year,
        max_year,
        (min_year, max_year),
        key="desc_year_range"
    )
    
    # Quarter filter
    quarters = st.multiselect(
        "Quarter",
        [1, 2, 3, 4],
        default=[1, 2, 3, 4],
        key="desc_quarter"
    )

# Filter data
filtered_df = df[
    (df['MUNICIPALITY'].isin(selected_municipality)) &
    (df['YEAR_2'].between(year_range[0], year_range[1])) &
    (df['QUARTER'].isin(quarters))
].dropna(subset=['CASES'])

# Header
st.markdown(render_header(
    title="Descriptive Analysis",
    subtitle="Explore dengue case distributions, temporal trends, and environmental correlations",
    badge="Data Analytics"
), unsafe_allow_html=True)

# Summary Metrics
st.markdown(render_section_header("Summary Statistics"), unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_cases = filtered_df['CASES'].sum()
    st.metric("Total Cases", f"{total_cases:,.0f}")

with col2:
    avg_weekly = filtered_df.groupby(['YEAR_2', 'MORBIDITY_WEEK'])['CASES'].sum().mean()
    st.metric("Avg Weekly Cases", f"{avg_weekly:.1f}")

with col3:
    peak_cases = filtered_df.groupby(['YEAR_2', 'MORBIDITY_WEEK'])['CASES'].sum().max()
    st.metric("Peak Weekly Cases", f"{peak_cases:.0f}")

with col4:
    avg_temp = filtered_df['T2M_MAX'].mean()
    st.metric("Avg Max Temp", f"{avg_temp:.1f}°C")

with col5:
    avg_humidity = filtered_df['RH2M'].mean()
    st.metric("Avg Humidity", f"{avg_humidity:.1f}%")

# Choropleth Map
st.markdown(render_section_header("Spatial Distribution"), unsafe_allow_html=True)

if geojson:
    # Aggregate cases by municipality
    muni_cases = filtered_df.groupby('MUNICIPALITY')['CASES'].sum().reset_index()
    
    fig_map = px.choropleth_mapbox(
        muni_cases,
        geojson=geojson,
        locations='MUNICIPALITY',
        featureidkey='properties.MUNICIPALITY',
        color='CASES',
        color_continuous_scale='YlOrRd',
        mapbox_style='carto-positron',
        zoom=8,
        center={"lat": 7.8, "lon": 122.5},
        opacity=0.75,
        labels={'CASES': 'Total Cases'},
        hover_name='MUNICIPALITY',
        hover_data={'CASES': ':,.0f'}
    )
    fig_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=450,
        coloraxis_colorbar=dict(
            title="Cases",
            tickformat=",d"
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Map visualization requires geopandas. Showing table view instead.")
    muni_cases = filtered_df.groupby('MUNICIPALITY')['CASES'].sum().sort_values(ascending=False).reset_index()
    st.dataframe(muni_cases, use_container_width=True, hide_index=True)

# Temporal Trends
st.markdown(render_section_header("Temporal Analysis"), unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Yearly Trend", "Quarterly Pattern", "Monthly Breakdown"])

with tab1:
    yearly_data = filtered_df.groupby('YEAR_2')['CASES'].sum().reset_index()
    yearly_data['YEAR_FULL'] = yearly_data['YEAR_2'].apply(lambda x: 2000 + int(x))
    
    fig_yearly = px.bar(
        yearly_data,
        x='YEAR_FULL',
        y='CASES',
        labels={'YEAR_FULL': 'Year', 'CASES': 'Total Cases'},
        color='CASES',
        color_continuous_scale='Blues'
    )
    fig_yearly.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(tickmode='linear', dtick=1)
    )
    fig_yearly.update_traces(marker_line_width=0)
    st.plotly_chart(fig_yearly, use_container_width=True)

with tab2:
    quarterly_data = filtered_df.groupby(['YEAR_2', 'QUARTER'])['CASES'].sum().reset_index()
    quarterly_data['Period'] = quarterly_data['YEAR_2'].astype(str) + '-Q' + quarterly_data['QUARTER'].astype(str)
    
    fig_quarterly = px.area(
        quarterly_data.sort_values(['YEAR_2', 'QUARTER']),
        x='Period',
        y='CASES',
        labels={'CASES': 'Number of Cases'},
        color_discrete_sequence=['#667eea']
    )
    fig_quarterly.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(tickangle=45, tickfont=dict(size=10))
    )
    st.plotly_chart(fig_quarterly, use_container_width=True)

with tab3:
    monthly_data = filtered_df.groupby('MONTH')['CASES'].sum().reset_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data['Month_Name'] = monthly_data['MONTH'].apply(lambda x: month_names[int(x)-1] if pd.notna(x) else '')
    
    fig_monthly = px.bar(
        monthly_data,
        x='Month_Name',
        y='CASES',
        labels={'Month_Name': 'Month', 'CASES': 'Total Cases'},
        color='CASES',
        color_continuous_scale='Oranges'
    )
    fig_monthly.update_layout(
        height=350,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# Geographic Distribution
st.markdown(render_section_header("Municipality Comparison"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    muni_data = filtered_df.groupby('MUNICIPALITY')['CASES'].sum().sort_values(ascending=True)
    
    fig_muni = px.bar(
        x=muni_data.values,
        y=muni_data.index,
        orientation='h',
        labels={'x': 'Total Cases', 'y': 'Municipality'},
        color=muni_data.values,
        color_continuous_scale='Viridis'
    )
    fig_muni.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(tickfont=dict(size=10)),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_muni, use_container_width=True)

with col2:
    # Top municipalities pie chart
    top_muni = filtered_df.groupby('MUNICIPALITY')['CASES'].sum().nlargest(8)
    
    fig_pie = px.pie(
        values=top_muni.values,
        names=top_muni.index,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_pie.update_layout(
        height=450,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=10)
        )
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig_pie, use_container_width=True)

# Environmental Correlation
st.markdown(render_section_header("Environmental Factors"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Temperature vs Cases
    temp_cases = filtered_df.groupby('MONTH').agg({
        'CASES': 'sum',
        'T2M_MAX': 'mean',
        'T2M_MIN': 'mean'
    }).reset_index()
    
    fig_temp = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_temp.add_trace(
        go.Bar(x=temp_cases['MONTH'], y=temp_cases['CASES'], name='Cases', 
               marker_color='#667eea', opacity=0.7),
        secondary_y=False
    )
    
    fig_temp.add_trace(
        go.Scatter(x=temp_cases['MONTH'], y=temp_cases['T2M_MAX'], name='Max Temp',
                   line=dict(color='#ef4444', width=2), mode='lines+markers'),
        secondary_y=True
    )
    
    fig_temp.update_layout(
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig_temp.update_xaxes(title_text="Month")
    fig_temp.update_yaxes(title_text="Cases", secondary_y=False)
    fig_temp.update_yaxes(title_text="Temperature (°C)", secondary_y=True)
    
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    # Humidity and Precipitation vs Cases
    env_cases = filtered_df.groupby('MONTH').agg({
        'CASES': 'sum',
        'RH2M': 'mean',
        'PRECTOTCORR': 'mean'
    }).reset_index()
    
    fig_env = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_env.add_trace(
        go.Bar(x=env_cases['MONTH'], y=env_cases['CASES'], name='Cases',
               marker_color='#667eea', opacity=0.7),
        secondary_y=False
    )
    
    fig_env.add_trace(
        go.Scatter(x=env_cases['MONTH'], y=env_cases['RH2M'], name='Humidity',
                   line=dict(color='#10b981', width=2), mode='lines+markers'),
        secondary_y=True
    )
    
    fig_env.update_layout(
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig_env.update_xaxes(title_text="Month")
    fig_env.update_yaxes(title_text="Cases", secondary_y=False)
    fig_env.update_yaxes(title_text="Humidity (%)", secondary_y=True)
    
    st.plotly_chart(fig_env, use_container_width=True)

# Data Summary
with st.expander("View Raw Data Summary"):
    st.markdown("**Filtered Dataset Overview**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        st.metric("Date Range", f"20{year_range[0]} - 20{year_range[1]}")
    with col3:
        st.metric("Municipalities", len(selected_municipality))
    
    st.dataframe(
        filtered_df.head(100).style.format({
            'CASES': '{:.0f}',
            'T2M_MAX': '{:.1f}',
            'T2M_MIN': '{:.1f}',
            'RH2M': '{:.1f}',
            'PRECTOTCORR': '{:.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )

# Footer
st.markdown(render_footer(), unsafe_allow_html=True)
