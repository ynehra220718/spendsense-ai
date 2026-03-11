import streamlit as st


def render_financial_health_gauge(financial_result: dict):
    """Renders financial health score as a styled gauge with verdict badge."""
    score = financial_result.get("health_score", 0)
    verdict = financial_result.get("verdict", "CAUTION")
    rationale = financial_result.get("rationale", "")
    opportunity_cost = financial_result.get("opportunity_cost", "")
    timing = financial_result.get("timing_recommendation", "")

    # Score band config
    if score >= 61:
        color = "green"
        label = "Healthy"
        icon = "✅"
    elif score >= 41:
        color = "orange"
        label = "Caution Zone"
        icon = "⚠️"
    else:
        color = "red"
        label = "Under Strain"
        icon = "🚫"

    verdict_colors = {
        "RECOMMENDED": "🟢",
        "CAUTION": "🟡",
        "NOT_RECOMMENDED": "🔴",
    }

    st.markdown("#### 💰 Financial Health")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.progress(score / 100, text=f"**{icon} Score: {score}/100 — {label}**")

    with col2:
        st.metric(
            label="Verdict",
            value=f"{verdict_colors.get(verdict, '⚪')} {verdict.replace('_', ' ').title()}",
        )

    with col3:
        st.metric(label="Opportunity Cost", value=opportunity_cost or "—")

    if rationale:
        with st.expander("Why this score?"):
            st.write(rationale)
            if timing:
                st.info(f"**Timing:** {timing}")
