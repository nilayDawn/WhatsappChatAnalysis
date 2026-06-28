import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import helper
import styles


def render(selected_user, df):
    """Renders the Vocabulary & Phrase Analysis page."""

    st.markdown(
        '<div class="section-title">🔤 Vocabulary &amp; Phrase Analysis</div>',
        unsafe_allow_html=True,
    )

    most_common_df, all_words_df = helper.most_common_words(selected_user, df)
    tab_wc, tab_words = st.tabs(["✨ Word Cloud (Bigrams)", "📊 Most Common Phrases"])

    with tab_wc:
        df_wc = helper.create_wordcloud_bigrams(selected_user, df)
        if df_wc is not None:
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.imshow(df_wc, interpolation="bilinear")
            ax.axis("off")
            fig.patch.set_facecolor("none")
            ax.patch.set_facecolor("none")
            st.pyplot(fig, clear_figure=True)
            plt.close(fig)
        else:
            st.info("No words found. This chat might be empty or entirely media files.")

    with tab_words:
        if not most_common_df.empty:
            if selected_user == "All":
                fig = px.bar(
                    most_common_df,
                    x="Count",
                    y="Word",
                    color="Sender",
                    orientation="h",
                    barmode="stack",
                    title="Top 20 Phrases Breakdown by Sender",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
            else:
                fig = px.bar(
                    most_common_df,
                    x="Count",
                    y="Word",
                    orientation="h",
                    title=f"Top 20 Phrases for {selected_user}",
                    color_discrete_sequence=["#818cf8"],
                )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            styles.style_plotly_fig(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No words found. This chat might be empty or entirely media files.")

    # Always-visible phrases table
    if not all_words_df.empty:
        st.markdown(
            "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-top:24px; margin-bottom:8px;'>📋 Top 50 Most Common Phrases</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(all_words_df, use_container_width=True)
