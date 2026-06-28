import streamlit as st
import roast_mode
import styles


def render(df):
    """Renders the Group Roast Report page (Group-only)."""

    st.markdown(
        '<div class="section-title">😂 Group Roast Report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:24px;'>AI-generated roasts based on each member's real chat behaviour. No feelings were considered.</p>",
        unsafe_allow_html=True,
    )

    roasts = roast_mode.roast_mode(df)

    if not roasts:
        st.info("Not enough data to generate roast reports.")
        return

    cols = st.columns(2)
    for i, (title, roast) in enumerate(roasts.items()):
        with cols[i % 2]:
            icon = title.split()[0] if title else "😂"
            styles.render_metric_card(
                title,
                roast["winner"],
                roast["value"],
                icon=icon,
            )
            st.markdown(
                f"""
<div style="
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 0.9rem;
    color: #cbd5e1;
    font-style: italic;
    background: rgba(30,41,59,0.3);
    border-left: 3px solid #6366f1;
    border-radius: 0 10px 10px 0;
">
    "{roast['roast']}"
</div>
""",
                unsafe_allow_html=True,
            )
