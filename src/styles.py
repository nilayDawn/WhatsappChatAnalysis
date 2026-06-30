import streamlit as st
import os

CSS_DIR = os.path.join(os.path.dirname(__file__), "css")


def _read_css(filename):
    path = os.path.join(CSS_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def load_css():
    """Injects the Chat Rewind premium design system CSS."""
    base = _read_css("base.css")
    fix = _read_css("fix_file_uploader.css")
    st.markdown(f"<style>{base}{fix}</style>", unsafe_allow_html=True)


def load_page_css(page_name):
    """Loads page-specific CSS on top of base."""
    css = _read_css(f"{page_name}.css")
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def style_plotly_fig(fig, title=None):
    """Applies Chat Rewind dark theme to Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Manrope, sans-serif", color="#cbd5e1"),
        title=dict(
            text=title or (fig.layout.title.text if fig.layout.title else ""),
            font=dict(size=18, color="#c4b5fd", weight="bold"),
        ) if (title or (fig.layout.title and fig.layout.title.text)) else None,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.08)", zeroline=False,
            title_font=dict(size=12, color="#94a3b8"),
            tickfont=dict(size=10, color="#94a3b8"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.08)", zeroline=False,
            title_font=dict(size=12, color="#94a3b8"),
            tickfont=dict(size=10, color="#94a3b8"),
        ),
    )
    return fig


# ── Reusable HTML card renderers ─────────────────────────────────────────────

def render_metric_card(label, value, subtitle="", icon="📊", color="#8B5CF6"):
    st.markdown(f"""
<div class="cr-metric-card" style="--accent:{color}">
    <div class="cr-metric-icon">{icon}</div>
    <div class="cr-metric-label">{label}</div>
    <div class="cr-metric-value">{value}</div>
    <div class="cr-metric-sub">{subtitle}</div>
</div>""", unsafe_allow_html=True)


def render_award_card(icon, title, winner, stat, description=""):
    st.markdown(f"""
<div class="cr-award-card">
    <div class="cr-award-badge">{icon}</div>
    <div class="cr-award-title">{title}</div>
    <div class="cr-award-winner">{winner}</div>
    <div class="cr-award-stat">{stat}</div>
    <div class="cr-award-desc">{description}</div>
</div>""", unsafe_allow_html=True)


def render_roast_card(icon, title, winner, stat, roast_text, color="#EC4899"):
    st.markdown(f"""
<div class="cr-roast-card" style="--accent:{color}">
    <div class="cr-roast-header">
        <span class="cr-roast-icon">{icon}</span>
        <span class="cr-roast-title">{title}</span>
    </div>
    <div class="cr-roast-winner">{winner}</div>
    <div class="cr-roast-stat">{stat}</div>
    <div class="cr-roast-text">"{roast_text}"</div>
</div>""", unsafe_allow_html=True)


def render_ghost_card(icon, title, suspect, avg_time, evidence_lines=None, color="#06B6D4"):
    evidence_html = ""
    if evidence_lines:
        items = "".join(f'<div class="cr-ghost-evidence-line">{l}</div>' for l in evidence_lines[:4])
        evidence_html = f'<div class="cr-ghost-evidence">{items}</div>'
    st.markdown(f"""
<div class="cr-ghost-card" style="--accent:{color}">
    <div class="cr-ghost-badge">{icon}</div>
    <div class="cr-ghost-title">{title}</div>
    <div class="cr-ghost-suspect">{suspect}</div>
    <div class="cr-ghost-time">{avg_time}</div>
    {evidence_html}
</div>""", unsafe_allow_html=True)


def render_streak_card(icon, label, value, unit="days", color="#F59E0B"):
    st.markdown(f"""
<div class="cr-streak-card" style="--accent:{color}">
    <div class="cr-streak-icon">{icon}</div>
    <div class="cr-streak-value">{value}</div>
    <div class="cr-streak-unit">{unit}</div>
    <div class="cr-streak-label">{label}</div>
</div>""", unsafe_allow_html=True)


def render_rank_card(rank, name, value, icon="⚡", color="#3B82F6"):
    medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"#{rank}"
    st.markdown(f"""
<div class="cr-rank-card" style="--accent:{color}">
    <div class="cr-rank-medal">{medal}</div>
    <div class="cr-rank-info">
        <div class="cr-rank-name">{name}</div>
        <div class="cr-rank-value">{icon} {value}</div>
    </div>
</div>""", unsafe_allow_html=True)


def render_sleep_card(icon, label, name, stat, verdict="", color="#8B5CF6"):
    st.markdown(f"""
<div class="cr-sleep-card" style="--accent:{color}">
    <div class="cr-sleep-icon">{icon}</div>
    <div class="cr-sleep-label">{label}</div>
    <div class="cr-sleep-name">{name}</div>
    <div class="cr-sleep-stat">{stat}</div>
    <div class="cr-sleep-verdict">{verdict}</div>
</div>""", unsafe_allow_html=True)


def render_section_header(icon, title, subtitle=""):
    st.markdown(f"""
<div class="cr-section-header">
    <div class="cr-section-icon">{icon}</div>
    <h2 class="cr-section-title">{title}</h2>
    <p class="cr-section-subtitle">{subtitle}</p>
</div>""", unsafe_allow_html=True)


def render_chapter_divider(number, title):
    st.markdown(f"""
<div class="cr-chapter-divider">
    <div class="cr-chapter-num">CHAPTER {number}</div>
    <div class="cr-chapter-title">{title}</div>
    <div class="cr-chapter-line"></div>
</div>""", unsafe_allow_html=True)


def render_header():
    """Renders the top banner for dashboard mode."""
    st.markdown("""
<div class="cr-topbar">
    <div class="cr-topbar-brand">
        <span class="cr-topbar-logo">💬</span>
        <span class="cr-topbar-name">CHAT REWIND</span>
    </div>
    <div class="cr-topbar-tagline">Your friendship story, visualized</div>
</div>""", unsafe_allow_html=True)


def render_instructions():
    """Renders cinematic export instructions."""
    st.markdown("""
<div class="cr-instructions">
    <div class="cr-instructions-title">📖 How to Export Your Chat</div>
    <div class="cr-instruction-step">
        <div class="cr-step-num">1</div>
        <div>Open the chat in <b>WhatsApp</b></div>
    </div>
    <div class="cr-instruction-step">
        <div class="cr-step-num">2</div>
        <div>Tap <b>⋮</b> → <b>More</b> → <b>Export Chat</b></div>
    </div>
    <div class="cr-instruction-step">
        <div class="cr-step-num">3</div>
        <div>Select <b>Without Media</b></div>
    </div>
    <div class="cr-instruction-step">
        <div class="cr-step-num">4</div>
        <div>If ZIP, extract the <b>.txt</b> file</div>
    </div>
    <div class="cr-instruction-step">
        <div class="cr-step-num">5</div>
        <div>Upload the <b>.txt</b> file here</div>
    </div>
</div>""", unsafe_allow_html=True)


def render_disclaimer(title, text_html, icon="⚠️", color="#8B5CF6"):
    st.markdown(f"""
<div class="cr-disclaimer-card" style="--accent:{color}">
    <div class="cr-disclaimer-header">
        <span class="cr-disclaimer-icon">{icon}</span>
        <span class="cr-disclaimer-title">{title}</span>
    </div>
    <div class="cr-disclaimer-body">
        {text_html}
    </div>
</div>""", unsafe_allow_html=True)

