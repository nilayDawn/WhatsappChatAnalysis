import streamlit as st
import plotly.express as px
import features.helper as helper
import styles


def render(selected_user, df):
    """Renders the Emoji & Sentiment Analysis page."""

    styles.render_section_header("🎭", "Emoji & Vibe Check",
                                 "Which emojis define your conversations?")

    emoji_df = helper.emoji_helper(selected_user, df)

    if not emoji_df.empty:
        col_emo1, col_emo2 = st.columns([2, 3])
        with col_emo1:
            st.markdown(
                "<div style='font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:8px;'>"
                "📊 Emoji Count Table</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(emoji_df, use_container_width=True)

        with col_emo2:
            top = emoji_df.head(10).copy()
            top["Sender_Label"] = top["Sender"] + " (" + top["Emoji"] + ")"
            if not top.empty:
                fig = px.pie(
                    top,
                    values="Count",
                    names="Sender_Label",
                    title="Top 10 Most Used Emojis",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                styles.style_plotly_fig(fig)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No emojis found. This chat might be empty or entirely media files.")
