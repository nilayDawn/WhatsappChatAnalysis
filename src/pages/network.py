import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import reply_network
import styles


def render(df):
    """Renders the Reply Network Analysis page (Group-only)."""

    st.markdown(
        '<div class="section-title">🕸️ Reply Network Analysis</div>',
        unsafe_allow_html=True,
    )

    reply_data = reply_network.reply_network_analysis(df)
    edges = reply_data["edges"]

    if edges.empty:
        st.info("Not enough replies found to build a network.")
        return

    # ── Award cards ───────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        styles.render_metric_card(
            "🏆 Most Popular",
            reply_data["most_popular"],
            "Most replied to",
            icon="🏆",
        )
    with col2:
        styles.render_metric_card(
            "⚡ Most Responsive",
            reply_data["most_responsive"],
            "Most replies sent",
            icon="⚡",
        )
    with col3:
        styles.render_metric_card(
            "🦋 Social Butterfly",
            reply_data["social_butterfly"],
            "Most connections",
            icon="🦋",
        )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:28px 0;'>", unsafe_allow_html=True)

    # ── Network graph ─────────────────────────────────────────────────────────
    G = nx.DiGraph()
    for _, row in edges.iterrows():
        G.add_edge(row["From"], row["To"], weight=row["Replies"])

    fig, ax = plt.subplots(figsize=(10, 7.5))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Use circular layout to arrange nodes cleanly in a circle
    pos = nx.circular_layout(G)
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    # Normalize widths for better visualization
    widths = [max(1.5, min(8.0, w / 3)) for w in weights]

    # Draw nodes with a soft light-blue background and indigo border
    nx.draw_networkx_nodes(
        G, pos, node_size=3200, node_color="#e0e7ff", edgecolors="#4f46e5", linewidths=2.5, ax=ax
    )

    # Draw edges with curved arcs so bidirectional replies don't overlap
    nx.draw_networkx_edges(
        G, pos, width=widths, arrows=True, arrowsize=18,
        edge_color="#818cf8", alpha=0.8, connectionstyle="arc3,rad=0.15", ax=ax
    )

    # Draw node labels with high readability (dark indigo text)
    nx.draw_networkx_labels(
        G, pos, font_size=10, font_weight="bold", font_color="#1e1b4b", ax=ax
    )

    # Draw edge labels in clear bubble tags
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=9, font_color="#4f46e5",
        bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'),
        ax=ax
    )
    ax.axis("off")

    col_graph, col_table = st.columns([3, 2])
    with col_graph:
        st.pyplot(fig)
        plt.close(fig)

    with col_table:
        st.markdown(
            "<div style='font-weight:600; color:#a5b4fc; font-size:1.05rem; margin-bottom:10px;'>📋 Reply Matrix</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            edges.sort_values("Replies", ascending=False),
            use_container_width=True,
        )
