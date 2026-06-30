import streamlit as st
import features.roast_mode as roast_mode
import styles

# Color palette for different roast categories
ROAST_COLORS = [
    "#EC4899", "#EF4444", "#F59E0B", "#8B5CF6",
    "#06B6D4", "#10B981", "#3B82F6", "#EC4899",
]


def render(df):
    """Chapter 6: Roast Report — The funniest section."""

    styles.render_chapter_divider("06", "Roast Report")

    styles.render_section_header("😂", "No Feelings Were Considered",
                                 "AI-generated roasts based on each member's real chat behaviour")

    roasts = roast_mode.roast_mode(df)

    if not roasts:
        st.info("Not enough data to generate roast reports.")
        return

    cols = st.columns(2)
    for i, (title, roast) in enumerate(roasts.items()):
        with cols[i % 2]:
            icon = title.split()[0] if title else "😂"
            clean_title = title.split(" ", 1)[1] if " " in title else title
            color = ROAST_COLORS[i % len(ROAST_COLORS)]

            styles.render_roast_card(
                icon=icon,
                title=clean_title,
                winner=roast["winner"],
                stat=roast["value"],
                roast_text=roast["roast"],
                color=color,
            )
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
