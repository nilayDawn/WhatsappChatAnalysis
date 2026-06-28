import sys
import streamlit as st
import pandas as pd

# Ensure the src directory is on the path when running via `streamlit run src/app.py`
sys.path.insert(0, "src")

from preprocessing import preprocess
import styles

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.load_css()

# Page definitions
CORE_PAGES = {
    "📊 Who Talks the Most?":  "overview",
    "🔤 Slang & Catchphrases": "vocabulary",
    "🎭 Emoji & Vibe Check":   "emoji_analysis",
    "📈 When Are We Active?":  "timelines",
}

GROUP_PAGES = {
    "🏆 Chat Awards":          "awards",
    "⚡ Response Time":         "response_time",
    "🕸️ Reply Network":         "network",
    "🔥 Chat Streaks":          "streaks",
    "😂 Roast Report":          "roast",
    "👻 Ghosting Analysis":     "ghosting",
    "🌙 Sleep Deprivation":     "sleep",
}

# Initialize session state for uploaded file and analysis state
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "show_analysis" not in st.session_state:
    st.session_state["show_analysis"] = False

# Preprocessing cache
@st.cache_data(show_spinner=False)
def cached_preprocess(text):
    return preprocess(text)


@st.cache_data(show_spinner=False)
def get_users(df):
    users = df["Sender"].unique().tolist()
    users.sort()
    return users


# Onboarding / Landing Page State
if st.session_state["uploaded_file"] is None or not st.session_state["show_analysis"]:
    # Sidebar: Locked Nav info
    with st.sidebar:
        st.markdown(
            """
            <div style="padding:16px 0 24px; text-align: center;">
                <div style="font-size:2rem; margin-bottom:4px;">💬</div>
                <h2 style="margin:0; font-size:1.3rem; font-weight:800;
                           background:linear-gradient(to right,#a5b4fc,#818cf8);
                           -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                    WA Analyzer
                </h2>
                <p style="color:#475569; font-size:0.75rem; margin:4px 0 0;">
                    Chat Intelligence Dashboard
                </p>
            </div>
            <div style="background: rgba(30,41,59,0.3); border-radius: 12px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center; margin-top: 30px;">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">🔒</div>
                <div style="font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Navigation Locked</div>
                <p style="font-size: 0.75rem; color: #475569; margin: 0;">Upload a WhatsApp chat file in the main area to unlock dashboard features.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main Page UI decoration
    st.markdown(
        """
        <div class="welcome-hero">
            <div class="hero-badge">⚡ INSTANT CONVERSATION INSIGHTS</div>
            <h1>WhatsApp Chat Analyzer</h1>
            <p>Transform your plain text WhatsApp chat logs into a highly interactive visual dashboard. Explore communication timelines, response dynamics, relationship streaks, sleep reports, and AI roast profiles.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_guide = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown(
            """
            <div class="upload-container">
                <div style="font-size: 3rem; margin-bottom: 12px;">📤</div>
                <div style="font-weight: 700; font-size: 1.25rem; color: #a5b4fc; margin-bottom: 8px;">Upload Chat Log</div>
                <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 24px;">Drag and drop your exported <b>.txt</b> file below</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "Upload Chat (.txt)",
            type=["txt"],
            key="initial_uploader",
            label_visibility="collapsed",
        )
        if uploaded is not None:
            st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
            if st.button("📊 Show Analysis", use_container_width=True):
                st.session_state["uploaded_file"] = uploaded
                st.session_state["show_analysis"] = True
                st.rerun()
        else:
            st.session_state["uploaded_file"] = None
            st.session_state["show_analysis"] = False

    with col_guide:
        styles.render_instructions()

    # Feature showcase grid
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; margin-bottom: 20px;">
            <h3 style="font-weight: 800; font-size: 1.5rem; background: linear-gradient(to right, #a5b4fc, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">✨ Unlock Advanced Analytics</h3>
        </div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-card-icon">🏆</div>
                <div class="feature-card-title">Chat Awards</div>
                <div class="feature-card-desc">Recognize individual personalities: the Spammer, the Emoji King, or the Link Sharer.</div>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">⚡</div>
                <div class="feature-card-title">Response Times</div>
                <div class="feature-card-desc">Calculate average reply latency, longest ignore durations, and response rankings.</div>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">🕸️</div>
                <div class="feature-card-title">Reply Network</div>
                <div class="feature-card-desc">Map out and visualize direct replies in a dynamic interactive node connection graph.</div>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">🌙</div>
                <div class="feature-card-title">Circadian Sleep</div>
                <div class="feature-card-desc">Discover midnight activity levels, estimated sleep debt, night owls, and demon hours.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()



# State: File Uploaded (Dashboard Mode)

uploaded_file = st.session_state["uploaded_file"]

content = uploaded_file.getvalue()
text = content.decode("utf-8-sig")
df = cached_preprocess(text)
user_list = get_users(df)

# Sidebar navigation & filters
with st.sidebar:
    st.markdown(
        """
<div style="padding:16px 0 24px;">
    <div style="font-size:2rem; text-align:center; margin-bottom:4px;">💬</div>
    <h2 style="text-align:center; margin:0; font-size:1.3rem; font-weight:800;
               background:linear-gradient(to right,#a5b4fc,#818cf8);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        WA Analyzer
    </h2>
    <p style="text-align:center; color:#475569; font-size:0.75rem; margin:4px 0 0;">
        Chat Intelligence Dashboard
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-size:0.8rem; font-weight:600; color:#94a3b8; margin-bottom:6px;'>👤 Filter by User</div>",
        unsafe_allow_html=True,
    )
    selected_user = st.selectbox(
        "Select User",
        options=["All"] + user_list,
        index=0,
        key="user_filter",
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);'>", unsafe_allow_html=True)

    # Navigation buttons
    st.markdown(
        "<div style='font-size:0.78rem; font-weight:700; color:#64748b; letter-spacing:0.08em; margin-bottom:8px;'>CORE ANALYSIS</div>",
        unsafe_allow_html=True,
    )
    for label in CORE_PAGES:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state["active_page"] = label

    if selected_user == "All":
        st.markdown(
            "<hr style='border-color:rgba(255,255,255,0.06);'>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='font-size:0.78rem; font-weight:700; color:#64748b; letter-spacing:0.08em; margin-bottom:8px;'>GROUP INSIGHTS</div>",
            unsafe_allow_html=True,
        )
        for label in GROUP_PAGES:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state["active_page"] = label

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background:rgba(30,41,59,0.5); border-radius:10px; padding:10px 14px; font-size:0.8rem;'>"
        f"<span style='color:#475569;'>Messages parsed: </span>"
        f"<span style='color:#a5b4fc; font-weight:700;'>{len(df):,}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

# Main area header
styles.render_header()

# Active file options expander at the top of the main area
with st.expander(f"📁 Active Chat Session: {uploaded_file.name}", expanded=False):
    col_uploader_active, col_remove_btn = st.columns([3, 1])
    with col_uploader_active:
        change_val = st.file_uploader(
            "Change active file",
            type=["txt"],
            key="active_uploader",
            label_visibility="collapsed",
        )
        if change_val is not None:
            st.session_state["uploaded_file"] = change_val
            st.rerun()
    with col_remove_btn:
        st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
        if st.button("❌ Reset Upload"):
            st.session_state["uploaded_file"] = None
            st.session_state["active_page"] = "📊 Who Talks the Most?"
            st.rerun()

# Default page setup
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "📊 Who Talks the Most?"

active = st.session_state["active_page"]

# Safety redirect if user switches away from "All" while in group-only pages
if active in GROUP_PAGES and selected_user != "All":
    st.session_state["active_page"] = "📊 Who Talks the Most?"
    active = "📊 Who Talks the Most?"

# Breadcrumb
filter_label = f"👤 {selected_user}" if selected_user != "All" else "👥 All Users"
st.markdown(
    f"""
<div style="
    display:flex; align-items:center; gap:10px;
    margin-bottom:20px; padding-bottom:12px;
    border-bottom:1px solid rgba(255,255,255,0.05);
">
    <span style="color:#475569; font-size:0.85rem;">Dashboard</span>
    <span style="color:#334155;">›</span>
    <span style="color:#a5b4fc; font-size:0.85rem; font-weight:600;">{active}</span>
    <span style="margin-left:auto; background:rgba(99,102,241,0.15);
                 border:1px solid rgba(99,102,241,0.3); border-radius:20px;
                 padding:2px 12px; font-size:0.78rem; color:#818cf8;">{filter_label}</span>
</div>
""",
    unsafe_allow_html=True,
)

# Route to page module
with st.spinner("Loading..."):
    if active in CORE_PAGES:
        module_name = CORE_PAGES[active]
        import importlib
        page_mod = importlib.import_module(f"pages.{module_name}")
        page_mod.render(selected_user, df)

    elif active in GROUP_PAGES and selected_user == "All":
        module_name = GROUP_PAGES[active]
        import importlib
        page_mod = importlib.import_module(f"pages.{module_name}")
        page_mod.render(df)