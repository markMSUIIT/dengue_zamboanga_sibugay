"""
Shared styles and rendering functions for the Dengue Surveillance Dashboard
"""

# Shared CSS styles for the entire application
SHARED_CSS = """
<style>
    /* Global styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.75rem;
    }
    
    /* Info box styling */
    .info-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        color: #1e40af;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header .subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-bottom: 1rem;
    }
    
    .main-header .badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* Section header styling */
    .section-header {
        color: #DC2626;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #FCA5A5;
    }
    
    /* Sidebar header styling */
    .sidebar-header {
        background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
        color: white;
        padding: 1.5rem 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
    }
    
    .sidebar-header h2 {
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .sidebar-header .subtitle {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    .sidebar-header .icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        text-align: center;
        border-top: 3px solid #DC2626;
    }
    
    .footer .copyright {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    
    .footer .credits {
        font-size: 0.85rem;
        color: #9ca3af;
    }
    
    /* Additional utility styles */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
</style>
"""


def render_header(title, subtitle, badge=""):
    """
    Render the main page header with title, subtitle, and optional badge.
    
    Args:
        title (str): Main title text
        subtitle (str): Subtitle or description text
        badge (str, optional): Badge text to display (e.g., location, status)
    
    Returns:
        str: HTML string for the header
    """
    badge_html = f'<div class="badge">{badge}</div>' if badge else ''
    
    return f"""
    <div class="main-header">
        <h1>{title}</h1>
        <div class="subtitle">{subtitle}</div>
        {badge_html}
    </div>
    """


def render_section_header(title):
    """
    Render a section header with consistent styling.
    
    Args:
        title (str): Section title text
    
    Returns:
        str: HTML string for the section header
    """
    return f"""
    <div class="section-header">
        {title}
    </div>
    """


def render_footer():
    """
    Render the page footer with copyright and credits.
    
    Returns:
        str: HTML string for the footer
    """
    return """
    <div class="footer">
        <div class="copyright">
            <strong>Dengue Epidemiological Surveillance System</strong> | Zamboanga Sibugay Province
        </div>
        <div class="credits">
            Developed for Public Health Research | © 2025
        </div>
    </div>
    """


def render_sidebar_header():
    """
    Render the sidebar header with branding and icon.
    
    Returns:
        str: HTML string for the sidebar header
    """
    return """
    <div class="sidebar-header">
        <div class="icon">🦟</div>
        <h2>Dengue Dashboard</h2>
        <div class="subtitle">Zamboanga Sibugay</div>
    </div>
    """
