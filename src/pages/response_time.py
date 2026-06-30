import streamlit as st
import features.reply_speed as reply_speed
import styles


def render(df):
    """Chapter 3: Response Time — Ranking cards with medals."""

    styles.render_chapter_divider("03", "Response Time Analysis")

    styles.render_section_header("⚡", "Who Replies Fastest?",
                                 "Average response times ranked and exposed")
    
    # ── Disclaimer Section ──
    disclaimer_text = (
        "A response duration simply measures the raw time gap between two different speakers. "
        "If a conversation naturally ended (e.g., <i>'Okay, goodnight!'</i>), a message sent days later "
        "to start a <b>new</b> topic will technically register as a long ignore. "
        "Don't start a real-world argument without checking the <b>Ghosting Analysis</b> page "
        "to see if they actually ignored you or if the conversation was just over!"
    )
    styles.render_disclaimer(
        title="Disclaimer & Technical Context",
        text_html=disclaimer_text,
        icon="⚡",
        color="#F59E0B"
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)



    reply_stats = reply_speed.response_time_analysis(df)

    if not reply_stats:
        st.info("Not enough data to compute response times.")
        return
    
    

    # ── Hero Awards ──
    col1, col2, col3 = st.columns(3)

    with col1:
        styles.render_metric_card(
            "Fastest Replier", reply_stats["fastest"],
            "Lightning-fast responses", "⚡", "#10B981",
        )

    with col2:
        
        styles.render_metric_card(
            "Longest Ignore", reply_stats["longest_ignore_sender"],
            reply_speed.format_seconds(reply_stats["longest_ignore"]),
            "💀", "#EF4444",
        )

    with col3:
        styles.render_metric_card(
            "Message Ignored To", reply_stats["longest_ignore_to"],
            f"At {reply_stats['longest_ignore_time'].strftime('%Y-%m-%d %H:%M')}",
            "⏱️", "#F59E0B",
        )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Per-user ranking ──
    styles.render_section_header("📋", "Response Time Leaderboard", "")

    avg_items = list(reply_stats["avg_reply"].items())
    for rank, (user, sec) in enumerate(avg_items, 1):
        styles.render_rank_card(
            rank=rank,
            name=user,
            value=reply_speed.format_seconds(sec),
            icon="⚡",
            color="#8B5CF6" if rank <= 3 else "#3B82F6",
        )
