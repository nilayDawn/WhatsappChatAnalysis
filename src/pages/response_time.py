import streamlit as st
import reply_speed
import styles


def render(df):
    """Renders the Response Time Analysis page (Group-only)."""

    st.markdown(
        '<div class="section-title">⚡ Response Time Analysis</div>',
        unsafe_allow_html=True,
    )

    reply_stats = reply_speed.response_time_analysis(df)

    if not reply_stats:
        st.info("Not enough data to compute response times.")
        return

    # ── Award cards ───────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        styles.render_metric_card(
            "🏆 Fastest Replier",
            reply_stats["fastest"],
            "Fastest average response",
            icon="⚡",
        )

    with col2:
        styles.render_metric_card(
            "💀 Longest Ignore",
            reply_stats["longest_ignore_sender"],
            reply_speed.format_seconds(reply_stats["longest_ignore"]),
            icon="💀",
        )

    with col3:
        styles.render_metric_card(
            "⏱️ Message Ignored To",
            reply_stats["longest_ignore_to"],
            f"At {reply_stats['longest_ignore_time'].strftime('%Y-%m-%d %H:%M')}",
            icon="⏱️",
        )

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

    # ── Per-user average reply times ──────────────────────────────────────────
    st.markdown(
        "<div style='font-weight:600; color:#a5b4fc; font-size:1.1rem; margin-bottom:16px;'>📋 Average Reply Time per User</div>",
        unsafe_allow_html=True,
    )

    avg_items = reply_stats["avg_reply"].items()
    cols = st.columns(min(len(reply_stats["avg_reply"]), 4))

    for idx, (user, sec) in enumerate(avg_items):
        with cols[idx % len(cols)]:
            styles.render_metric_card(
                user,
                reply_speed.format_seconds(sec),
                "avg reply time",
                icon="💬",
            )
