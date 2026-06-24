import streamlit as st

def load_css():
    """Injects custom CSS to apply high-end dark glassmorphic styling to the Streamlit app."""
    css_content = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global settings and app background */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 70%) !important;
        color: #f8fafc !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    /* Header adjustments */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f1f5f9 !important;
    }

    /* Target specific headings for styled looks */
    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #a5b4fc, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #6366f1;
        padding-left: 12px;
    }

    /* Card Layout for Custom Metrics */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin: 24px 0;
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 0 20px rgba(99, 102, 241, 0.2);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-icon {
        font-size: 1.75rem;
        margin-bottom: 12px;
    }

    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.075em;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(to right, #a5b4fc, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin: 4px 0;
    }

    .metric-user {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Styled Instructions / Onboarding Card */
    .instruction-card {
        background: rgba(30, 41, 59, 0.25);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }

    .instruction-step {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 0.95rem;
        color: #cbd5e1;
    }

    .instruction-step:last-child {
        margin-bottom: 0;
    }

    .step-number {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 14px;
        font-size: 0.85rem;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
        flex-shrink: 0;
    }

    /* Glassmorphism containers for dataframes / lists */
    .glass-container {
        background: rgba(30, 41, 59, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
    }

    /* Tabs Styling Overrides */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 12px 24px !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-baseweb="tab"]:hover {
        color: #f1f5f9 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a5b4fc !important;
        border-bottom: 3px solid #6366f1 !important;
    }
    
    div[data-testid="stTab"] {
        background-color: rgba(15, 23, 42, 0.3) !important;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Customize Expander Header */
    div[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    div[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }

    /* Alert / Notifications styling overrides */
    div[data-testid="stNotification"] {
        border-radius: 12px !important;
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(8px);
        color: #f1f5f9 !important;
    }
    
    /* Input element tweaks */
    div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
    }

    div.stButton > button:active {
        transform: translateY(0px) !important;
    }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)

def render_header():
    """Renders the top banner of the application."""
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 32px; padding: 12px 0;">
        <div style="font-size: 3.5rem; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 10px rgba(37,211,102,0.2));">💬</div>
        <div>
            <h1 style="margin: 0; font-size: 2.75rem; font-weight: 800; background: linear-gradient(to right, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">WhatsApp Chat Analyzer</h1>
            <p style="margin: 0; color: #94a3b8; font-size: 1.1rem; font-weight: 400;">Unlock beautiful insights, timelines, and interaction patterns from your conversations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_instructions():
    """Renders user-friendly step-by-step export instructions."""
    st.markdown("""
    <div class="instruction-card">
        <div style="font-weight: 700; margin-bottom: 16px; font-size: 1.25rem; color: #a5b4fc; display: flex; align-items: center; gap: 8px;">
            📖 Quick Guide: How to Export & Analyze
        </div>
        <div class="instruction-step">
            <div class="step-number">1</div>
            <div>Open the desired group or individual chat in <b>WhatsApp</b>.</div>
        </div>
        <div class="instruction-step">
            <div class="step-number">2</div>
            <div>Tap the three dots menu <b>⋮ (Android)</b> or tap the group name <b>(iOS)</b> > <b>More</b> > <b>Export Chat</b>.</div>
        </div>
        <div class="instruction-step">
            <div class="step-number">3</div>
            <div>Crucial: Select <b>Without Media</b> to generate a clean txt log.</div>
        </div>
        <div class="instruction-step">
            <div class="step-number">4</div>
            <div>If exported as a ZIP, extract the <b>.txt</b> file.</div>
        </div>
        <div class="instruction-step">
            <div class="step-number">5</div>
            <div>Drag and drop or browse to upload the <b>.txt</b> file below.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, user, icon="📈"):
    """Renders a beautiful glassmorphic metric card using HTML/CSS."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-user">👤 Filter: {user}</div>
    </div>
    """, unsafe_allow_html=True)

def style_plotly_fig(fig, title=None):
    """Applies standard aesthetics to Plotly charts to match the dark theme."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#cbd5e1"),
        title=dict(
            text=title if title else fig.layout.title.text if fig.layout.title else "",
            font=dict(size=18, family="Plus Jakarta Sans, sans-serif", color="#a5b4fc", weight="bold")
        ) if (title or (fig.layout.title and fig.layout.title.text)) else None,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.1)",
            zeroline=False,
            title_font=dict(size=12, color="#94a3b8"),
            tickfont=dict(size=10, color="#94a3b8")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.1)",
            zeroline=False,
            title_font=dict(size=12, color="#94a3b8"),
            tickfont=dict(size=10, color="#94a3b8")
        )
    )
    return fig
