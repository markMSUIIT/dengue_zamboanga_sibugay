"""
Data Entry Module
Dengue Surveillance System - Zamboanga Sibugay
"""

import streamlit as st
import pandas as pd
import sys
sys.path.append('..')

try:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box, render_success_box, render_warning_box
except:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box, render_success_box, render_warning_box

# Page configuration
st.set_page_config(
    page_title="Data Entry - Dengue Surveillance",
    page_icon="📝",
    layout="wide"
)

# Apply shared styles
st.markdown(SHARED_CSS, unsafe_allow_html=True)

DATA_FILE = 'sibugay_dengue_cases_dataset.csv'

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown(render_sidebar_header(), unsafe_allow_html=True)
    st.markdown("### Quick Actions")
    st.markdown("""
    - Add new weekly data
    - Review pending entries
    - Save to database
    """)
    st.markdown("---")
    st.markdown(f"**Total Records:** {len(df):,}")

# Header
st.markdown(render_header(
    title="Data Entry",
    subtitle="Add and manage weekly dengue case reports",
    badge="Admin Panel"
), unsafe_allow_html=True)

# Info
st.markdown("""
<div class="info-box">
    <strong>Instructions:</strong> Use this form to enter new weekly dengue case data. 
    Entries are first stored in memory and can be saved to the CSV file when ready.
</div>
""", unsafe_allow_html=True)

# Data Entry Form
st.markdown(render_section_header("Add New Entry"), unsafe_allow_html=True)

with st.form("data_entry_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Location & Time**")
        municipality = st.selectbox(
            "Municipality",
            sorted(df['MUNICIPALITY'].dropna().unique())
        )
        year = st.number_input("Year", min_value=2018, max_value=2030, value=2024)
        month = st.number_input("Month", min_value=1, max_value=12, value=1)
        week = st.number_input("Morbidity Week", min_value=1, max_value=53, value=1)
        quarter = st.selectbox("Quarter", [1, 2, 3, 4])
    
    with col2:
        st.markdown("**Case Data**")
        cases = st.number_input("Number of Cases", min_value=0, value=0)
        morbidity_week = st.number_input("Morbidity Rate", min_value=0.0, value=0.0, step=0.01)
        st.markdown("**Temperature**")
        t2m_max = st.number_input("Max Temp (°C)", min_value=0.0, value=32.0, step=0.1)
        t2m_min = st.number_input("Min Temp (°C)", min_value=0.0, value=24.0, step=0.1)
    
    with col3:
        st.markdown("**Environmental**")
        rh2m = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        prectotcorr = st.number_input("Precipitation (mm)", min_value=0.0, value=5.0, step=0.1)
        st.markdown("**Administrative**")
        province = st.text_input("Province", value="Zamboanga Sibugay")
        region = st.text_input("Region", value="Region IX")

    submitted = st.form_submit_button("Add Entry", use_container_width=True)

    if submitted:
        # Get the municipality's geometry and other static info from existing data
        muni_row = df[df['MUNICIPALITY'] == municipality].iloc[0] if len(df[df['MUNICIPALITY'] == municipality]) > 0 else None
        
        # Calculate next ID safely (handle NaN)
        max_id = df['id'].dropna().max() if 'id' in df.columns else 0
        next_id = int(max_id) + 1 + len(st.session_state.get('new_entries', [])) if pd.notna(max_id) else len(df) + 1 + len(st.session_state.get('new_entries', []))
        
        # Create new row with ALL columns in proper order matching CSV
        new_row = {
            'id': next_id,
            'ID_0': muni_row['ID_0'] if muni_row is not None else 177,
            'ISO': muni_row['ISO'] if muni_row is not None else 'PHL',
            'NAME_0': muni_row['NAME_0'] if muni_row is not None else 'Philippines',
            'ID_1': muni_row['ID_1'] if muni_row is not None else 17,
            'NAME_1': muni_row['NAME_1'] if muni_row is not None else 'Zamboanga Peninsula',
            'ID_2': muni_row['ID_2'] if muni_row is not None else 0,
            'NAME_2': muni_row['NAME_2'] if muni_row is not None else municipality,
            'TYPE_2': muni_row['TYPE_2'] if muni_row is not None else 'Province',
            'ENGTYPE_2': muni_row['ENGTYPE_2'] if muni_row is not None else 'Province',
            'NL_NAME_2': muni_row['NL_NAME_2'] if muni_row is not None else '',
            'VARNAME_2': muni_row['VARNAME_2'] if muni_row is not None else '',
            'geometry': muni_row['geometry'] if muni_row is not None else '',
            'PROVINCE': province,
            'MUNICIPALITY': municipality,
            'MUNICIPALITY_2': muni_row['MUNICIPALITY_2'] if muni_row is not None else municipality,
            'YEAR_2': year - 2000,  # Store as 2-digit year
            'DOY': week * 7,  # Day of year approximation
            'MONTH': month,
            'QUARTER': quarter,
            'WEEK': 7,  # Fixed value in dataset
            'CASES': cases,
            'MORBIDITY_WEEK': week,
            'ALLSKY_SFC_UVA': muni_row['ALLSKY_SFC_UVA'] if muni_row is not None else 0.0,
            'ALLSKY_SFC_UVB': muni_row['ALLSKY_SFC_UVB'] if muni_row is not None else 0.0,
            'T2M_MAX': t2m_max,
            'T2M_MIN': t2m_min,
            'PRECTOTCORR': prectotcorr,
            'RH2M': rh2m,
            'QV2M': muni_row['QV2M'] if muni_row is not None else 0.0,
            'GWETTOP': muni_row['GWETTOP'] if muni_row is not None else 0.0,
        }
        
        if 'new_entries' not in st.session_state:
            st.session_state['new_entries'] = []
        st.session_state['new_entries'].append(new_row)
        st.success(f"Entry added for {municipality}, Week {week}, {year}")

# Pending Entries
st.markdown(render_section_header("Pending Entries"), unsafe_allow_html=True)

if 'new_entries' in st.session_state and st.session_state['new_entries']:
    pending_df = pd.DataFrame(st.session_state['new_entries'])
    
    # Display count
    st.markdown(f"""
    <div class="warning-box">
        <strong>{len(pending_df)} entries pending</strong> — Review and save when ready.
    </div>
    """, unsafe_allow_html=True)
    
    # Show only relevant columns for display
    display_cols = ['MUNICIPALITY', 'YEAR_2', 'MORBIDITY_WEEK', 'CASES', 'T2M_MAX', 'T2M_MIN', 'RH2M', 'PRECTOTCORR']
    display_df = pending_df[display_cols].copy()
    display_df.columns = ['Municipality', 'Year', 'Week', 'Cases', 'Max Temp', 'Min Temp', 'Humidity', 'Precip']
    
    st.dataframe(
        display_df.style.format({
            'Cases': '{:.0f}',
            'Max Temp': '{:.1f}°C',
            'Min Temp': '{:.1f}°C',
            'Humidity': '{:.1f}%',
            'Precip': '{:.1f}mm'
        }),
        use_container_width=True, 
        hide_index=True
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Save All to CSV", type="primary", use_container_width=True):
            # Ensure columns are in correct order matching the CSV
            csv_columns = list(df.columns)
            save_df = pending_df[csv_columns]
            save_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
            st.success(f"{len(pending_df)} entries saved!")
            st.session_state['new_entries'] = []
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state['new_entries'] = []
            st.info("Pending entries cleared.")
            st.rerun()
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: #F9FAFB; border-radius: 12px; border: 2px dashed #E5E7EB;">
        <p style="color: #6B7280; margin: 0;">No pending entries</p>
        <p style="color: #9CA3AF; font-size: 0.85rem; margin: 0.5rem 0 0 0;">Use the form above to add new data</p>
    </div>
    """, unsafe_allow_html=True)

# Recent Data
st.markdown(render_section_header("Recent Records"), unsafe_allow_html=True)

# Show last entries
recent_df = df.tail(15)[['MUNICIPALITY', 'YEAR_2', 'MORBIDITY_WEEK', 'CASES', 'T2M_MAX', 'RH2M']].copy()
recent_df.columns = ['Municipality', 'Year', 'Week', 'Cases', 'Max Temp', 'Humidity']

st.dataframe(
    recent_df.style.format({
        'Cases': '{:.0f}',
        'Max Temp': '{:.1f}°C',
        'Humidity': '{:.1f}%'
    }),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown(render_footer(), unsafe_allow_html=True)
