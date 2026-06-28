import streamlit as st
import plotly.express as px
import helper
import styles


def render(selected_user, df):
    """Renders the Overview page: key metrics + user contribution chart."""

    # ── Key Metrics ───────────────────────────────────────────────────────────
    num_messages, num_words, num_urls, num_media_messages = helper.fetch_stats(
        selected_user, df
    )

    st.markdown(
        '<div class="section-title">📊 Key Metrics Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        styles.render_metric_card(
            "Total Messages", f"{num_messages:,}", selected_user, icon="✉️"
        )
    with col2:
        styles.render_metric_card(
            "Total Words", f"{num_words:,}", selected_user, icon="📝"
        )
    with col3:
        styles.render_metric_card(
            "Media Omitted", f"{num_media_messages:,}", selected_user, icon="🖼️"
        )
    with col4:
        styles.render_metric_card(
            "Links Shared", f"{num_urls:,}", selected_user, icon="🔗"
        )

    # ── User Contribution (All-only) ──────────────────────────────────────────
    if selected_user == "All":
        st.markdown(
            '<div class="section-title">👥 User Contribution &amp; Activity</div>',
            unsafe_allow_html=True,
        )
        x, new_df = helper.most_busy_user(df)

        col_busy1, col_busy2 = st.columns([3, 2])
        with col_busy1:
            fig = px.bar(
                x=x.index,
                y=x.values,
                labels={"x": "User", "y": "Number of Messages"},
                title="Top 5 Most Active Users",
                color=x.values,
                color_continuous_scale="Purples",
            )
            fig.update_layout(coloraxis_showscale=False)
            styles.style_plotly_fig(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col_busy2:
            st.markdown(
                "<div style='padding-top: 10px; font-weight:600; color:#a5b4fc; font-size:1.1rem; margin-bottom:8px;'>Percentage Contribution</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(new_df, use_container_width=True)
