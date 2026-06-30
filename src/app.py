import sys
import streamlit as st
import pandas as pd

# Ensure the src directory is on the path when running via `streamlit run src/app.py`
sys.path.insert(0, "src")

from preprocessing import preprocess
import styles

# Page configuration
st.set_page_config(
    page_title="Chat Rewind — Your WhatsApp Story",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.load_css()

# Page definitions
CORE_PAGES = {
    "📊 The Overview":         "overview",
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

# Initialize session state
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "show_analysis" not in st.session_state:
    st.session_state["show_analysis"] = False
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "📊 The Overview"
if "scroll_to_top" not in st.session_state:
    st.session_state["scroll_to_top"] = False

# ── Scroll to top trigger (fires at the very start of each run) ──
if st.session_state.get("scroll_to_top", False):
    import time
    _t = int(time.time() * 1000)
    st.markdown(f"""
    <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7?t={_t}"
         onerror="this.onerror=null;"
         onload="
            (function() {{
                function doScroll() {{
                    var targets = [
                        document.querySelector('.main'),
                        document.querySelector('[data-testid=\'stMain\']'),
                        document.querySelector('[data-testid=\'stAppViewContainer\']'),
                        document.querySelector('.block-container'),
                        document.documentElement,
                        document.body
                    ];
                    targets.forEach(function(t) {{
                        if (t) {{ t.scrollTop = 0; if (t.scrollTo) t.scrollTo({{top:0,behavior:'instant'}}); }}
                    }});
                    window.scrollTo({{top:0,behavior:'instant'}});
                }}
                doScroll();
                setTimeout(doScroll, 50);
                setTimeout(doScroll, 150);
                setTimeout(doScroll, 400);
            }})();
         "
         style="position:fixed;width:0;height:0;opacity:0;pointer-events:none;">
    """, unsafe_allow_html=True)
    st.session_state["scroll_to_top"] = False




@st.cache_data(show_spinner=False)
def cached_preprocess(text):
    return preprocess(text)


@st.cache_data(show_spinner=False)
def get_users(df):
    users = df["Sender"].unique().tolist()
    users.sort()
    return users



# LANDING PAGE — Cinematic Hero Experience


if st.session_state["uploaded_file"] is None or not st.session_state["show_analysis"]:

    # Sidebar: Locked state
    with st.sidebar:
        st.markdown("""
        <div style="padding:24px 0;text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:8px;">💬</div>
            <h2 style="margin:0;font-size:1.4rem;font-weight:900;
                       background:linear-gradient(135deg,#8B5CF6,#EC4899);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                CHAT REWIND
            </h2>
            <p style="color:#64748b;font-size:0.75rem;margin:4px 0 0;">
                Your friendship story, visualized
            </p>
        </div>
        <div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:20px;
                    border:1px solid rgba(255,255,255,0.08);text-align:center;margin-top:24px;">
            <div style="font-size:1.5rem;margin-bottom:10px;">🔒</div>
            <div style="font-size:0.85rem;font-weight:700;color:#94a3b8;margin-bottom:6px;">
                Sections Locked
            </div>
            <p style="font-size:0.75rem;color:#64748b;margin:0;">
                Upload a chat file to unlock your personalized story.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Cinematic Hero ──
    st.markdown("""
    <div class="cr-hero">
        <div class="cr-hero-emoji">💬</div>
        <h1 class="cr-hero-title">CHAT REWIND</h1>
        <p class="cr-hero-sub">
            Discover the hidden story inside your WhatsApp chats.
            Uncover friendships, expose ghosters, and unlock achievements.
        </p>
        <div class="cr-hero-divider"></div>
        <div class="cr-hero-features">
            <div class="cr-hero-chip">✨ Roast Friends</div>
            <div class="cr-hero-chip">👻 Detect Ghosters</div>
            <div class="cr-hero-chip">🌙 Sleep Habits</div>
            <div class="cr-hero-chip">🏆 Unlock Awards</div>
            <div class="cr-hero-chip">❤️ Relationships</div>
            <div class="cr-hero-chip">🔥 Chat Streaks</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload + Instructions row ──
    col_upload, col_guide = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("""
        <div class="cr-upload-zone">
            <div style="font-size:3rem;margin-bottom:12px;">📤</div>
            <div style="font-weight:700;font-size:1.2rem;color:#8B5CF6;margin-bottom:8px;">
                Upload Your Chat
            </div>
            <p style="font-size:0.85rem;color:#94a3b8;margin-bottom:24px;">
                Drop your exported <b>.txt</b> file below to begin
            </p>
        </div>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "", type=["txt"],
            key="initial_uploader", label_visibility="collapsed",
        )
        if uploaded is not None:
            st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
            if st.button("🚀 Start Your Rewind", use_container_width=True):
                st.session_state["uploaded_file"] = uploaded
                st.session_state["show_analysis"] = True
                st.rerun()
        else:
            st.session_state["uploaded_file"] = None
            st.session_state["show_analysis"] = False

    with col_guide:
        styles.render_instructions()

    # ── Feature showcase ──
    st.markdown("""
    <div style="text-align:center;margin-top:60px;margin-bottom:20px;">
        <h3 style="font-weight:800;font-size:22px;
                   background:linear-gradient(135deg,#8B5CF6,#EC4899);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            ✨ What Your Rewind Unlocks
        </h3>
    </div>
    <div class="cr-features-grid">
        <div class="cr-feature-card">
            <div class="cr-feature-icon">🏆</div>
            <div class="cr-feature-title">Chat Awards</div>
            <div class="cr-feature-desc">Steam-style achievements for your group's most notable personalities.</div>
        </div>
        <div class="cr-feature-card">
            <div class="cr-feature-icon">😂</div>
            <div class="cr-feature-title">Roast Report</div>
            <div class="cr-feature-desc">AI-powered comedic takedowns based on real chat behaviour.</div>
        </div>
        <div class="cr-feature-card">
            <div class="cr-feature-icon">👻</div>
            <div class="cr-feature-title">Ghosting Files</div>
            <div class="cr-feature-desc">Detective-style case files exposing every disappearance.</div>
        </div>
        <div class="cr-feature-card">
            <div class="cr-feature-icon">🌙</div>
            <div class="cr-feature-title">Sleep Report</div>
            <div class="cr-feature-desc">Who's texting at 3AM? Neon-lit sleep deprivation analysis.</div>
        </div>
        <div class="cr-feature-card">
            <div class="cr-feature-icon">🔥</div>
            <div class="cr-feature-title">Chat Streaks</div>
            <div class="cr-feature-desc">Duolingo-style streak tracking for your friendships.</div>
        </div>
        <div class="cr-feature-card">
            <div class="cr-feature-icon">🕸️</div>
            <div class="cr-feature-title">Reply Network</div>
            <div class="cr-feature-desc">Interactive social graph revealing who talks to whom.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()



# DASHBOARD MODE — Story Navigation


uploaded_file = st.session_state["uploaded_file"]
content = uploaded_file.getvalue()
text = content.decode("utf-8-sig")
df = cached_preprocess(text)
user_list = get_users(df)

# ── Sidebar Navigation ──
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0;text-align:center;">
        <div style="font-size:2rem;margin-bottom:4px;">💬</div>
        <h2 style="margin:0;font-size:1.3rem;font-weight:900;
                   background:linear-gradient(135deg,#8B5CF6,#EC4899);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            CHAT REWIND
        </h2>
        <p style="color:#64748b;font-size:0.72rem;margin:4px 0 0;">
            Your friendship story
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.8rem;font-weight:600;color:#94a3b8;margin-bottom:6px;'>👤 Filter by User</div>",
        unsafe_allow_html=True,
    )
    selected_user = st.selectbox(
        "Select User", options=["All"] + user_list,
        index=0, key="user_filter", label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.72rem;font-weight:700;color:#64748b;letter-spacing:.1em;margin-bottom:8px;'>YOUR STORY</div>",
        unsafe_allow_html=True,
    )
    for label in CORE_PAGES:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state["active_page"] = label
            st.session_state["scroll_to_top"] = True

    if selected_user == "All":
        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.72rem;font-weight:700;color:#64748b;letter-spacing:.1em;margin-bottom:8px;'>GROUP CHAPTERS</div>",
            unsafe_allow_html=True,
        )
        for label in GROUP_PAGES:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state["active_page"] = label
                st.session_state["scroll_to_top"] = True

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background:rgba(255,255,255,0.04);border-radius:12px;padding:10px 14px;"
        f"font-size:0.8rem;border:1px solid rgba(255,255,255,0.06);'>"
        f"<span style='color:#64748b;'>Messages: </span>"
        f"<span style='color:#8B5CF6;font-weight:700;'>{len(df):,}</span></div>",
        unsafe_allow_html=True,
    )

# ── Top bar ──
styles.render_header()

# ── Active file controls ──
with st.expander(f"📁 Active Chat: {uploaded_file.name}", expanded=False):
    col_uploader_active, col_remove_btn = st.columns([3, 1])
    with col_uploader_active:
        change_val = st.file_uploader(
            "Change active file", type=["txt"],
            key="active_uploader", label_visibility="collapsed",
        )
        if change_val is not None:
            st.session_state["uploaded_file"] = change_val
            st.rerun()
    with col_remove_btn:
        st.markdown("<div style='padding-top:5px;'></div>", unsafe_allow_html=True)
        if st.button("❌ Reset"):
            st.session_state["uploaded_file"] = None
            st.session_state["active_page"] = "📊 The Overview"
            st.rerun()

# ── Page routing ──
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "📊 The Overview"

active = st.session_state["active_page"]

if active in GROUP_PAGES and selected_user != "All":
    st.session_state["active_page"] = "📊 The Overview"
    active = "📊 The Overview"

# Breadcrumb
filter_label = f"👤 {selected_user}" if selected_user != "All" else "👥 All Users"
st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;padding-bottom:12px;
            border-bottom:1px solid rgba(255,255,255,0.05);">
    <span style="color:#64748b;font-size:0.85rem;">Chat Rewind</span>
    <span style="color:#334155;">›</span>
    <span style="color:#8B5CF6;font-size:0.85rem;font-weight:600;">{active}</span>
    <span style="margin-left:auto;background:rgba(139,92,246,0.12);
                 border:1px solid rgba(139,92,246,0.25);border-radius:20px;
                 padding:3px 14px;font-size:0.78rem;color:#8B5CF6;">{filter_label}</span>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading your story..."):
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

# Bottom Navigation for scrolling experience
if selected_user == "All":
    available_pages = list(CORE_PAGES.keys()) + list(GROUP_PAGES.keys())
else:
    available_pages = list(CORE_PAGES.keys())

if active in available_pages:
    current_index = available_pages.index(active)
    
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin-bottom: 28px;'>", unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2, gap="medium")
    
    with col_prev:
        if current_index > 0:
            prev_page = available_pages[current_index - 1]
            if st.button(f"👈 Previous: {prev_page}", key="bottom_nav_prev", use_container_width=True):
                st.session_state["active_page"] = prev_page
                st.session_state["scroll_to_top"] = True
                st.rerun()
                
    with col_next:
        if current_index < len(available_pages) - 1:
            next_page = available_pages[current_index + 1]
            if st.button(f"Next: {next_page} 👉", key="bottom_nav_next", use_container_width=True):
                st.session_state["active_page"] = next_page
                st.session_state["scroll_to_top"] = True
                st.rerun()