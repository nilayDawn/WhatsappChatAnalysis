import streamlit as st
import plotly.express as px
import helper
import styles


def render(selected_user, df):
    """Chapter 1: The Overview — premium metric cards + contribution chart."""

    styles.render_chapter_divider("01", "The Overview")

    styles.render_section_header("📊", "Your Chat at a Glance",
                                 "The big picture of your conversations")

    # ── Key Metrics ──
    num_messages, num_words, num_urls, num_media_messages = helper.fetch_stats(
        selected_user, df
    )

    # Calculate extra stats
    active_days = df["only_date"].nunique() if selected_user == "All" else \
        df[df["Sender"] == selected_user]["only_date"].nunique()
    participants = df["Sender"].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        styles.render_metric_card("Total Messages", f"{num_messages:,}", "conversations captured", "✉️", "#8B5CF6")
    with col2:
        styles.render_metric_card("Total Words", f"{num_words:,}", "words exchanged", "📝", "#3B82F6")
    with col3:
        styles.render_metric_card("Media Shared", f"{num_media_messages:,}", "photos, videos & stickers", "🖼️", "#EC4899")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        styles.render_metric_card("Links Shared", f"{num_urls:,}", "URLs discovered", "🔗", "#06B6D4")
    with col5:
        styles.render_metric_card("Active Days", f"{active_days:,}", "days of conversation", "📅", "#10B981")
    with col6:
        styles.render_metric_card("Participants", f"{participants}", "unique voices", "👥", "#F59E0B")

    # ── User Contribution (All-only) ──
    if selected_user == "All":
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        styles.render_section_header("👥", "Who Dominates the Chat?",
                                     "Message distribution across all participants")

        x, new_df = helper.most_busy_user(df)

        col_busy1, col_busy2 = st.columns([3, 2])
        with col_busy1:
            fig = px.bar(
                x=x.index, y=x.values,
                labels={"x": "User", "y": "Messages"},
                title="Top Active Users",
                color=x.values,
                color_continuous_scale=["#1e1b4b", "#8B5CF6", "#EC4899"],
            )
            fig.update_layout(coloraxis_showscale=False)
            styles.style_plotly_fig(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col_busy2:
            st.markdown(
                "<div style='font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:10px;padding-top:10px;'>"
                "📋 Contribution Breakdown</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(new_df, use_container_width=True)
