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

# All chapters in order
ALL_CHAPTERS = [
    {"label": "📊 The Overview",         "module": "overview",       "group_only": False, "num": "01", "icon": "📊"},
    {"label": "🔤 Slang & Catchphrases", "module": "vocabulary",     "group_only": False, "num": "02", "icon": "🔤"},
    {"label": "🎭 Emoji & Vibe Check",   "module": "emoji_analysis", "group_only": False, "num": "03", "icon": "🎭"},
    {"label": "📈 When Are We Active?",  "module": "timelines",      "group_only": False, "num": "04", "icon": "📈"},
    {"label": "🏆 Chat Awards",          "module": "awards",         "group_only": True,  "num": "05", "icon": "🏆"},
    {"label": "⚡ Response Time",         "module": "response_time",  "group_only": True,  "num": "06", "icon": "⚡"},
    {"label": "🕸️ Reply Network",         "module": "network",        "group_only": True,  "num": "07", "icon": "🕸️"},
    {"label": "🔥 Chat Streaks",          "module": "streaks",        "group_only": True,  "num": "08", "icon": "🔥"},
    {"label": "😂 Roast Report",          "module": "roast",          "group_only": True,  "num": "09", "icon": "😂"},
    {"label": "👻 Ghosting Analysis",     "module": "ghosting",       "group_only": True,  "num": "10", "icon": "👻"},
    {"label": "🌙 Sleep Deprivation",     "module": "sleep",          "group_only": True,  "num": "11", "icon": "🌙"},
]

# Initialize session state
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "show_analysis" not in st.session_state:
    st.session_state["show_analysis"] = False
if "unlocked_up_to" not in st.session_state:
    st.session_state["unlocked_up_to"] = 0





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

unlocked = st.session_state["unlocked_up_to"]

# ── Sidebar ──
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

    # Progress tracker — computed here after selected_user is known
    _visible_chapters = ALL_CHAPTERS if selected_user == "All" else [ch for ch in ALL_CHAPTERS if not ch["group_only"]]
    _total_visible = len(_visible_chapters)
    _unlocked_visible = sum(1 for ch in _visible_chapters if ALL_CHAPTERS.index(ch) <= unlocked)
    _pct = int((_unlocked_visible / _total_visible) * 100) if _total_visible > 0 else 0
    st.markdown(
        f"<div class='cr-progress-label'>📖 Your Progress &nbsp; <span style='color:#8B5CF6;font-weight:900;'>{_unlocked_visible}/{_total_visible}</span></div>"
        f"<div class='cr-progress-bar-wrap'><div class='cr-progress-bar-fill' style='width:{_pct}%'></div></div>",
        unsafe_allow_html=True,
    )

    _items_html = ""
    for ch in _visible_chapters:
        idx = ALL_CHAPTERS.index(ch)
        is_unlocked = idx <= unlocked
        cls = "unlocked" if is_unlocked else ""
        check = "✓" if is_unlocked else ""
        _items_html += (
            f"<div class='cr-progress-item {cls}'>"
            f"<div class='cr-progress-check'>{check}</div>"
            f"<span>{ch['label']}</span>"
            f"</div>"
        )
    st.markdown(_items_html, unsafe_allow_html=True)

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
            st.session_state["unlocked_up_to"] = 0
            st.rerun()
    with col_remove_btn:
        st.markdown("<div style='padding-top:5px;'></div>", unsafe_allow_html=True)
        if st.button("❌ Reset"):
            st.session_state["uploaded_file"] = None
            st.session_state["unlocked_up_to"] = 0
            st.rerun()

# ── Sequential chapter rendering ──
import importlib

for i, ch in enumerate(ALL_CHAPTERS):
    # Only render up to the unlocked chapter
    if i > unlocked:
        break
    # Skip group-only chapters when a specific user is selected
    if ch["group_only"] and selected_user != "All":
        continue

    # Chapter separator (not before the first chapter)
    if i > 0:
        st.markdown("""
        <div class="cr-chapter-sep">
            <div class="cr-chapter-sep-line"></div>
            <div class="cr-chapter-sep-dot"></div>
            <div class="cr-chapter-sep-line"></div>
        </div>
        """, unsafe_allow_html=True)

    # Render the chapter content
    page_mod = importlib.import_module(f"pages.{ch['module']}")
    if ch["group_only"]:
        page_mod.render(df)
    else:
        page_mod.render(selected_user, df)

# ── Unlock CTA (shown after the last rendered chapter) ──
next_idx = unlocked + 1

if next_idx < len(ALL_CHAPTERS):
    next_ch = ALL_CHAPTERS[next_idx]

    if next_ch["group_only"] and selected_user != "All":
        # Teaser: group chapters need All Users filter
        st.markdown("""
        <div class="cr-chapter-sep">
            <div class="cr-chapter-sep-line"></div>
            <div class="cr-chapter-sep-dot"></div>
            <div class="cr-chapter-sep-line"></div>
        </div>
        <div class="cr-group-teaser">
            <div class="cr-group-teaser-icon">👥</div>
            <div class="cr-group-teaser-text">
                <b>Group Chapters are waiting!</b><br>
                Switch the filter to <b>All Users</b> in the sidebar to unlock
                group analysis chapters like Chat Awards, Ghosting Files, and more.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Unlock CTA
        st.markdown("""
        <div class="cr-chapter-sep">
            <div class="cr-chapter-sep-line"></div>
            <div class="cr-chapter-sep-dot"></div>
            <div class="cr-chapter-sep-line"></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="cr-unlock-cta">
            <div class="cr-unlock-orb">{next_ch['icon']}</div>
            <div class="cr-unlock-eyebrow">Chapter {next_ch['num']} Awaits</div>
            <div class="cr-unlock-title">{next_ch['label']}</div>
        </div>
        """, unsafe_allow_html=True)
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            if st.button(
                f"✨ Unlock: {next_ch['label']}",
                key="unlock_next_chapter",
                use_container_width=True,
            ):
                st.session_state["unlocked_up_to"] = next_idx
                st.rerun()
else:
    # All chapters complete
    st.markdown("""
    <div class="cr-chapter-sep">
        <div class="cr-chapter-sep-line"></div>
        <div class="cr-chapter-sep-dot"></div>
        <div class="cr-chapter-sep-line"></div>
    </div>
    <div class="cr-completed">
        <div class="cr-completed-icon">🎉</div>
        <div class="cr-completed-title">Your Rewind is Complete!</div>
        <div class="cr-completed-sub">You've explored every chapter of your chat story. Scroll up to revisit any moment.</div>
    </div>
    """, unsafe_allow_html=True)