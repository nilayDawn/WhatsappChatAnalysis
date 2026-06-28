import streamlit as st
import pandas as pd
import plotly.express as px
import late_night
import styles


def render(df):
    """Renders the Sleep Deprivation Report page (Group-only)."""

    st.markdown(
        '<div class="section-title">🌙 Sleep Deprivation Report</div>',
        unsafe_allow_html=True,
    )

    night = late_night.late_night_analysis(df)

    if not night:
        st.info("No late-night activity found.")
        return

    # ── Row 1: Hero metrics ───────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        styles.render_metric_card(
            "Night Owl", night["night_owl"], night["night_owl_count"], icon="🌙"
        )
        st.caption("Sleep remains theoretical.")

    with col2:
        styles.render_metric_card(
            "Best Sleeper", night["best_sleeper"], f"{night['best_score']}%", icon="☀️"
        )
        st.caption("Still connected to reality.")

    with col3:
        styles.render_metric_card(
            "Worst Sleeper",
            night["worst_sleeper"],
            f"{night['worst_score']}%",
            icon="🧟",
        )
        st.caption("Has defeated circadian rhythm.")

    with col4:
        styles.render_metric_card(
            "Demon Hour",
            f"{night['demon_hour']}:00",
            night["demon_count"],
            icon="😈",
        )
        st.caption("Peak chaos time.")

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

    # ── Longest Session ───────────────────────────────────────────────────────
    if night["longest_session"]:
        s = night["longest_session"]
        st.markdown(
            "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:12px;'>🔥 Longest Night Session</div>",
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Start", s["start"].strftime("%d %b %I:%M %p"))
        c2.metric("End", s["end"].strftime("%d %b %I:%M %p"))
        c3.metric("Messages", s["messages"])
        c4.metric("Duration", str(s["duration"]))

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

    # ── Sleep Debt ────────────────────────────────────────────────────────────
    st.info(
        f"😭 **Sleep Debt Calculator**\n\n"
        f"Estimated sleep lost: **{night['sleep_hours']} hours** ({night['sleep_days']} days)\n\n"
        "Verdict: Nobody in this group believes in healthy sleep schedules."
    )

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

    # ── Night Activity Heatmap ────────────────────────────────────────────────
    st.markdown(
        "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:10px;'>🌙 Night Activity Heatmap</div>",
        unsafe_allow_html=True,
    )
    fig = px.imshow(
        night["heatmap"],
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Night Activity (Hour × Day)",
    )
    styles.style_plotly_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ── Tables row ────────────────────────────────────────────────────────────
    col_p, col_l = st.columns(2)

    with col_p:
        st.markdown(
            "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:8px;'>🎭 Night Personalities</div>",
            unsafe_allow_html=True,
        )
        personality_df = pd.DataFrame(
            list(night["personalities"].items()), columns=["User", "Personality"]
        )
        st.dataframe(personality_df, use_container_width=True)

    with col_l:
        st.markdown(
            "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:8px;'>🌃 Midnight Leaderboard</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(night["leaderboard"], use_container_width=True)
