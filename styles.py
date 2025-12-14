"""
Shared Styles Module - Modern UI Design
Dengue Surveillance System - Zamboanga Sibugay
"""

# Modern color palette
COLORS = {
    'primary': '#0066FF',
    'primary_dark': '#0052CC',
    'secondary': '#6B7280',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    'dark': '#1F2937',
    'light': '#F9FAFB',
    'white': '#FFFFFF',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2',
}

# Shared CSS for all pages
SHARED_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Keep header visible for sidebar toggle button */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Ensure sidebar collapse button is always visible */
    button[kind="header"] {
        visibility: visible !important;
    }
    
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Modern Header */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .app-header h1 {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        color: white;
        margin-top: 0.75rem;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1F2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1F2937;
        line-height: 1.2;
    }
    
    .metric-card .label {
        font-size: 0.875rem;
        color: #6B7280;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    .metric-card .delta {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        display: inline-block;
    }
    
    .delta-positive {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .delta-negative {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    /* Prediction Cards */
    .prediction-card {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
        transition: transform 0.2s ease;
    }
    
    .prediction-card:hover {
        transform: scale(1.02);
    }
    
    .prediction-card .value {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .prediction-card .label {
        font-size: 0.95rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .prediction-card .sublabel {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }
    
    .prediction-card.high-risk {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        box-shadow: 0 10px 40px rgba(239, 68, 68, 0.3);
    }
    
    .prediction-card.medium-risk {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        box-shadow: 0 10px 40px rgba(245, 158, 11, 0.3);
    }
    
    .prediction-card.low-risk {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
    }
    
    /* Info Box */
    .info-box {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 4px solid #0EA5E9;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #0C4A6E;
    }
    
    .info-box strong {
        color: #075985;
    }
    
    /* Warning Box */
    .warning-box {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 4px solid #F59E0B;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #92400E;
    }
    
    /* Success Box */
    .success-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 4px solid #10B981;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #166534;
    }
    
    /* Card Container */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin: 1rem 0;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
    }
    
    /* Data Table Styling */
    .dataframe {
        font-size: 0.875rem !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background: #F9FAFB;
        border-right: 1px solid #E5E7EB;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-header h2 {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .sidebar-header p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.8rem;
        margin: 0.25rem 0 0 0;
    }
    
    /* Filter Section */
    .filter-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    
    .filter-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    /* Performance Metric */
    .perf-metric {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
    
    .perf-metric .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1F2937;
    }
    
    .perf-metric .label {
        font-size: 0.75rem;
        color: #6B7280;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Risk Badge */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .risk-critical {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    .risk-high {
        background: #FFEDD5;
        color: #9A3412;
    }
    
    .risk-moderate {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .risk-low {
        background: #D1FAE5;
        color: #065F46;
    }
    
    /* Footer */
    .app-footer {
        margin-top: 3rem;
        padding: 1.5rem;
        background: #F9FAFB;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
    
    .app-footer p {
        color: #6B7280;
        font-size: 0.8rem;
        margin: 0.25rem 0;
    }
    
    /* Streamlit Element Overrides */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        border: 1px solid #E5E7EB;
    }
    
    .stMetric label {
        color: #6B7280 !important;
        font-weight: 500 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1F2937 !important;
        font-weight: 700 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #374151;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #F3F4F6;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
"""

def render_header(title: str, subtitle: str = None, badge: str = None):
    """Render a modern header component"""
    badge_html = f'<span class="header-badge">{badge}</span>' if badge else ''
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    
    return f"""
    <div class="app-header">
        <h1>{title}</h1>
        {subtitle_html}
        {badge_html}
    </div>
    """

def render_section_header(title: str):
    """Render a section header"""
    return f'<div class="section-header">{title}</div>'

def render_metric_card(value: str, label: str, delta: str = None, delta_type: str = "positive"):
    """Render a metric card"""
    delta_html = ""
    if delta:
        delta_class = "delta-positive" if delta_type == "positive" else "delta-negative"
        delta_html = f'<div class="delta {delta_class}">{delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
        {delta_html}
    </div>
    """

def render_prediction_card(value: str, label: str, sublabel: str = None, risk_level: str = "low"):
    """Render a prediction card"""
    sublabel_html = f'<div class="sublabel">{sublabel}</div>' if sublabel else ''
    
    return f"""
    <div class="prediction-card {risk_level}-risk">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
        {sublabel_html}
    </div>
    """

def render_info_box(content: str):
    """Render an info box"""
    return f'<div class="info-box">{content}</div>'

def render_warning_box(content: str):
    """Render a warning box"""
    return f'<div class="warning-box">{content}</div>'

def render_success_box(content: str):
    """Render a success box"""
    return f'<div class="success-box">{content}</div>'

def render_footer():
    """Render the app footer"""
    return """
    <div class="app-footer">
        <p><strong>Dengue Epidemiological Surveillance System</strong></p>
        <p>Zamboanga Sibugay Province, Philippines</p>
        <p>Data Source: DOH-IHSS & NASA POWER API</p>
        <hr style="margin: 1rem 0; border-color: rgba(255,255,255,0.2);">
        <p style="font-size: 0.75rem;"><strong>Lead Researcher:</strong><br>Brent Jason M. Dequina<br>BS Information Systems</p>
        <p style="font-size: 0.75rem; margin-top: 0.5rem;"><strong>Advisor:</strong><br>Assoc. Prof. Joseph C. Sieras, MSc.</p>
    </div>
    """

def render_sidebar_header():
    """Render sidebar header"""
    return """
    <div class="sidebar-header">
        <h2>Dengue Surveillance</h2>
        <p>Zamboanga Sibugay</p>
        <p style="font-size: 0.7rem; margin-top: 0.5rem; opacity: 0.9;">by Brent Jason M. Dequina</p>
    </div>
    """
