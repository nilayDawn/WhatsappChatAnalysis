import streamlit as st
import plotly.express as px
import chat_streak
import styles


def render(df):
    """Renders the Chat Streak Analysis page (Group-only)."""

    st.markdown(
        '<div class="section-title">🔥 Chat Streak Analysis</div>',
        unsafe_allow_html=True,
    )

    streak = chat_streak.chat_streak_analysis(df)

    if not streak:
        st.info("Not enough data to compute streak analysis.")
        return

    # ── Metric cards ──────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        styles.render_metric_card(
            "🔥 Longest Streak", f"{streak['longest_streak']}", "days", icon="🔥"
        )
    with col2:
        styles.render_metric_card(
            "⚡ Current Streak", f"{streak['current_streak']}", "days", icon="⚡"
        )
    with col3:
        styles.render_metric_card(
            "💔 Biggest Break", f"{streak['biggest_break']}", "days", icon="💔"
        )
    with col4:
        styles.render_metric_card(
            "🏆 Most Active Day",
            f"{streak['most_active_count']}",
            str(streak["most_active_day"]),
            icon="🏆",
        )

    # ── Streak history chart ──────────────────────────────────────────────────
    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
    fig = px.line(
        streak["streak_df"],
        x="date",
        y="streak",
        markers=True,
        title="Chat Streak History",
        color_discrete_sequence=["#f97316"],
    )
    styles.style_plotly_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ── Relationship badge ────────────────────────────────────────────────────
    days = streak["longest_streak"]
    if days >= 365:
        badge, color = "💍 Soulmates", "#f59e0b"
    elif days >= 100:
        badge, color = "❤️ Best Friends", "#ef4444"
    elif days >= 30:
        badge, color = "🤝 Close Friends", "#22c55e"
    elif days >= 10:
        badge, color = "😊 Good Connection", "#3b82f6"
    else:
        badge, color = "🌱 Growing Bond", "#a3a3a3"

    st.markdown(
        f"""
<div style="
    background: rgba(30,41,59,0.5);
    border: 1px solid {color};
    border-radius: 14px;
    padding: 16px 24px;
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 14px;
">
    <span style="font-size:2rem;">{badge.split()[0]}</span>
    <div>
        <div style="font-weight:700; font-size:1.1rem; color:#f1f5f9;">Relationship Consistency</div>
        <div style="color:{color}; font-weight:600; font-size:1.4rem;">{badge}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
