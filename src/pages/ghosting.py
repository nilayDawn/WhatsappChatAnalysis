import streamlit as st
import ghost_mode
import styles


def render(df):
    """Renders the Ghosting Analysis page (Group-only)."""

    st.markdown(
        '<div class="section-title">👻 Ghosting Analysis</div>',
        unsafe_allow_html=True,
    )

    ghost = ghost_mode.ghosting_analysis(df)

    if ghost is None:
        st.info("Not enough conversation transitions found for ghost analysis.")
        return

    # ── Row 1: Biggest Ghoster | Fastest Responder | Ultra Ghost ─────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        styles.render_metric_card(
            "Biggest Ghoster",
            ghost["biggest_ghoster"],
            ghost_mode.format_ghost_time(ghost["biggest_ghoster_time"]),
            icon="👻",
        )
        ex = ghost["biggest_example"]
        st.caption(
            f'💬 {ex["prev_sender"]} ({ex["prev_time"]}): "{str(ex["prev_message"])[:60]}"\n\n'
            f'↩️ {ex["reply_sender"]} ({ex["reply_time"]}): "{str(ex["reply_message"])[:60]}"'
        )

    with col2:
        styles.render_metric_card(
            "Fastest Responder",
            ghost["fastest"],
            ghost_mode.format_ghost_time(ghost["fastest_time"]),
            icon="⚡",
        )
        ex = ghost["fastest_example"]
        st.caption(
            f'💬 {ex["prev_sender"]} ({ex["prev_time"]}): "{str(ex["prev_message"])[:60]}"\n\n'
            f'↩️ {ex["reply_sender"]} ({ex["reply_time"]}): "{str(ex["reply_message"])[:60]}"'
        )

    with col3:
        styles.render_metric_card(
            "Ultra Ghost (24h+)",
            ghost["ultra_person"],
            f"{ghost['ultra_count']} times",
            icon="💀",
        )
        if ghost["ultra_example"] is not None:
            ex = ghost["ultra_example"]
            st.caption(
                f'💬 {ex["prev_sender"]} ({ex["prev_time"]}): "{str(ex["prev_message"])[:60]}"\n\n'
                f'↩️ {ex["reply_sender"]} ({ex["reply_time"]}): "{str(ex["reply_message"])[:60]}"'
            )
        else:
            st.caption("Nobody disappeared for more than 24 hours.")

    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)

    # ── Row 2: Most Ignored | Longest Ghost ───────────────────────────────────
    col4, col5 = st.columns(2)

    with col4:
        styles.render_metric_card(
            "Most Ignored",
            ghost["ignored_person"],
            f"{ghost['ignored_count']} times",
            icon="🥲",
        )
        st.caption("The universe chose silence.")

    with col5:
        longest = ghost["longest"]
        styles.render_metric_card(
            "Longest Ghost",
            f"{longest['prev_sender']} → {longest['reply_sender']}",
            ghost_mode.format_ghost_time(longest["ghost_seconds"]),
            icon="🏆",
        )
        st.caption(
            f'💬 {longest["prev_time"]}: "{str(longest["prev_message"])[:60]}"\n\n'
            f'↩️ {longest["reply_time"]}: "{str(longest["reply_message"])[:60]}"'
        )

    st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)

    # ── Worst Ghosting Pairs table ────────────────────────────────────────────
    st.markdown(
        "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:10px;'>🤝 Worst Ghosting Pairs</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(ghost["pair_stats"], use_container_width=True)

    with st.expander("📋 View Complete Ghosting Evidence", expanded=False):
        st.dataframe(ghost["verification"], use_container_width=True, height=450)
