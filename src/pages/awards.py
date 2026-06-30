import streamlit as st
import features.chat_award as chat_award
import styles


def render(df):
    """Chapter 2: Chat Awards — Steam-style achievement unlocks."""

    styles.render_chapter_divider("02", "Chat Awards")

    styles.render_section_header("🏆", "Achievement Unlocked",
                                 "Recognition for the group's most notable chat personalities")

    awards = chat_award.chat_awards(df)

    if not awards:
        st.info("Not enough data to generate awards.")
        return

    # Render awards in a 3-column grid
    cols = st.columns(3)
    for i, award in enumerate(awards.values()):
        with cols[i % 3]:
            icon = award["title"].split()[0]
            desc = award.get("description", "")
            styles.render_award_card(
                icon=icon,
                title=award["title"].split(" ", 1)[1] if " " in award["title"] else award["title"],
                winner=award["winner"],
                stat=f'{award["value"]} {award["suffix"]}',
                description=award["description"] if "description" in award else "",
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
