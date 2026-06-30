import streamlit as st
import pandas as pd
import plotly.express as px
import late_night
import styles


def render(df):
    """Chapter 8: Sleep Deprivation Report — Neon blue and purple."""

    styles.render_chapter_divider("08", "The Insomnia Chronicles")

    styles.render_section_header("🌙", "Who Needs Sleep When You Have WiFi?",
                                 "A brutal exposure of your group's circadian rhythm violations.")

    night = late_night.late_night_analysis(df)

    if not night:
        st.info("Wow, you guys actually sleep at night? No late-night activity found. Boring.")
        return

    # ── Hero cards ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        styles.render_sleep_card(
            "🧛‍♂️", "THE VAMPIRE", night["night_owl"],
            f'{night["night_owl_count"]} texts after midnight',
            "Literally has not seen the sun in years.",
            "#8B5CF6",
        )

    with col2:
        styles.render_sleep_card(
            "🛌", "RESPONSIBLE ADULT", night["best_sleeper"],
            f'{night["best_score"]}% day activity',
            "Probably has a 401(k) and drinks 8 glasses of water.",
            "#10B981",
        )

    with col3:
        styles.render_sleep_card(
            "🧟", "INSOMNIAC PRIME", night["worst_sleeper"],
            f'{night["worst_score"]}% night ratio',
            "Powered purely by anxiety and energy drinks.",
            "#EF4444",
        )

    with col4:
        styles.render_sleep_card(
            "😈", "THE DEMON HOUR", f'{night["demon_hour"]}:00',
            f'{night["demon_count"]} texts of pure chaos',
            "When brain cells die and the worst decisions are made.",
            "#EC4899",
        )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Longest Night Session ──
    if night["longest_session"]:
        s = night["longest_session"]
        styles.render_section_header("🔥", "The Marathon", "The 'Why are we still awake?' session that never ended.")

        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Started Making Mistakes", s["start"].strftime("%d %b %I:%M %p"))
        col_b.metric("Finally Passed Out", s["end"].strftime("%d %b %I:%M %p"))
        col_c.metric("Texts Exchanged", s["messages"])
        col_d.metric("Hours Wasted", str(s["duration"]))

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Sleep Debt ──
    st.markdown(f"""
    <div class="cr-metric-card" style="--accent:#8B5CF6;text-align:center;padding:32px;">
        <div class="cr-metric-icon">📉</div>
        <div class="cr-metric-label">COLLECTIVE SLEEP DEBT</div>
        <div class="cr-metric-value">{night['sleep_hours']} hours</div>
        <div class="cr-metric-sub">
            That is roughly {night['sleep_days']} full days of sleep lost to sending memes in the dark. 
            Y'all owe your bodies an apology.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Heatmap ──
    styles.render_section_header("🌃", "Crime Scene Map", "Exactly when you should have been asleep.")

    fig = px.imshow(
        night["heatmap"], aspect="auto",
        color_continuous_scale=["#070B14", "#1e1b4b", "#8B5CF6", "#EC4899"],
        title="Night Activity Pattern (aka The Insomnia Grid)",
    )
    styles.style_plotly_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ── Tables ──
    col_p, col_l = st.columns(2)

    with col_p:
        st.markdown(
            "<div style='font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:10px;'>"
            "🎭 Clinical Diagnoses</div>", unsafe_allow_html=True,
        )
        personality_df = pd.DataFrame(
            list(night["personalities"].items()), columns=["User", "Diagnosis"]
        )
        st.dataframe(personality_df, use_container_width=True)

    with col_l:
        st.markdown(
            "<div style='font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:10px;'>"
            "🏆 The Hall of Shame (Most Midnight Texts)</div>", unsafe_allow_html=True,
        )
        st.dataframe(night["leaderboard"], use_container_width=True)