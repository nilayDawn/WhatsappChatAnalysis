import streamlit as st
import plotly.express as px
import features.chat_streak as chat_streak
import styles


def render(df):
    """Chapter 5: Chat Streaks — Duolingo-style streak experience."""

    styles.render_chapter_divider("05", "Chat Streaks")

    styles.render_section_header("🔥", "Friendship Consistency",
                                 "How dedicated are you to keeping the conversation alive?")

    streak = chat_streak.chat_streak_analysis(df)

    if not streak:
        st.info("Not enough data to compute streak analysis.")
        return

    # ── Streak cards ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        styles.render_streak_card("🔥", "Longest Streak", streak["longest_streak"], "days", "#F59E0B")
    with col2:
        styles.render_streak_card("⚡", "Current Streak", streak["current_streak"], "days", "#8B5CF6")
    with col3:
        styles.render_streak_card("💔", "Biggest Break", streak["biggest_break"], "days", "#EF4444")
    with col4:
        styles.render_streak_card("🏆", "Most Active Day", streak["most_active_count"], "messages", "#10B981")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.caption(f"📅 Most active day: {streak['most_active_day']}")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── Streak history chart ──
    fig = px.line(
        streak["streak_df"], x="date", y="streak", markers=True,
        title="Chat Streak History",
        color_discrete_sequence=["#F59E0B"],
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6, line=dict(width=1, color="#F59E0B")),
    )
    styles.style_plotly_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ── Relationship badge ──
    days = streak["longest_streak"]
    if days >= 365:
        badge, color, desc = "💍 Basically Married", "#F59E0B", "365+ days? Just merge your bank accounts and move in together. This bond is clinically inseparable."
    elif days >= 100:
        badge, color, desc = "❤️ Mutual Obsession", "#EF4444", "Triple digits! Someone is definitely checking their     phone every 5 seconds just to see if a new message dropped."
    elif days >= 30:
        badge, color, desc = "🔥 Heavy Chemistry", "#10B981", "A whole month straight? The tension is real. Someone     definitely blushes when this chat lights up."
    elif days >= 10:
        badge, color, desc = "😏 Separation Anxiety", "#3B82F6", "The polite, boring phase is officially dead. You  guys are hooked on each other's updates."
    elif days >= 5:
        badge, color, desc = "🌱 Dangerous Spark", "#94a3b8", "Five days running! There is a little fire cooking    here. Don't ruin the vibe by going quiet now."
    else:
        badge, color, desc = "🪦 Ghosted?", "#6B7280", "Radio silence. Did someone get left on read, or are we  playing hard to get? Go break the ice."

    st.markdown(f"""
    <div class="cr-metric-card" style="--accent:{color};display:flex;align-items:center;gap:20px;padding:24px 32px;">
        <span style="font-size:48px;">{badge.split()[0]}</span>
        <div>
            <div style="font-size:11px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:{color};margin-bottom:6px;">
                RELATIONSHIP CONSISTENCY
            </div>
            <div style="font-size:24px;font-weight:900;color:#f1f5f9;margin-bottom:4px;">{badge}</div>
            <div style="font-size:14px;color:#94a3b8;font-style:italic;">{desc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
