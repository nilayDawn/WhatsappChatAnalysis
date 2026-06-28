import streamlit as st
import chat_award
import styles


def render(df):
    """Renders the Chat Awards page (Group-only)."""

    st.markdown(
        '<div class="section-title">🏆 Chat Awards</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:24px;'>Recognition for the group's most notable chat personalities and behaviours.</p>",
        unsafe_allow_html=True,
    )

    awards = chat_award.chat_awards(df)

    if not awards:
        st.info("Not enough data to generate awards.")
        return

    # Render in a 3-column grid
    cols = st.columns(3)
    for i, award in enumerate(awards.values()):
        with cols[i % 3]:
            icon = award["title"].split()[0]
            st.markdown(
                f"""
<div class="metric-card">
    <div class="metric-icon">{icon}</div>
    <div class="metric-label">{award['title']}</div>
    <div class="metric-value">{award['winner']}</div>
    <div class="metric-user">{award['value']} {award['suffix']}</div>
</div>
""",
                unsafe_allow_html=True,
            )
