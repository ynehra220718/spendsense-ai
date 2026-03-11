import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(page_title="History · SpendSense AI", page_icon="📋", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("📋 Evaluation History")
st.caption("All purchase evaluations from this session.")

history = st.session_state.history

if not history:
    st.info("No evaluations yet. Run a purchase check to see results here.")
    if st.button("Start a purchase check →"):
        st.switch_page("pages/02_purchase_check.py")
    st.stop()

VERDICT_ICONS = {
    "RECOMMENDED": "✅",
    "CAUTION": "⚠️",
    "NOT_RECOMMENDED": "🚫",
}

# ── Summary table ────────────────────────────────────────────────────────────
st.subheader(f"{len(history)} evaluation{'s' if len(history) != 1 else ''} this session")

rows = []
for i, r in enumerate(history):
    synth = r.get("synthesis", {})
    fin = r.get("financial", {})
    prod = r.get("product", {})
    verdict = synth.get("final_verdict", "—")
    rows.append({
        "#": i + 1,
        "Product": r.get("product", "—"),
        "Amount": f"${r.get('amount', 0):,.2f}",
        "Verdict": f"{VERDICT_ICONS.get(verdict, '⚪')} {verdict.replace('_', ' ').title()}",
        "Health Score": f"{fin.get('health_score', '—')}/100",
        "Price Assessment": prod.get("price_assessment", "—").replace("_", " ").title(),
        "Confidence": synth.get("confidence", "—").title(),
        "Time (s)": r.get("elapsed_seconds", "—"),
        "Platform": r.get("platform", "mock").title(),
    })

import pandas as pd
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()

# ── Individual evaluation drilldowns ────────────────────────────────────────
st.subheader("Evaluation Details")
for i, r in enumerate(reversed(history)):
    synth = r.get("synthesis", {})
    verdict = synth.get("final_verdict", "CAUTION")
    icon = VERDICT_ICONS.get(verdict, "⚪")

    with st.expander(f"{icon} #{len(history) - i} · {r.get('product', '—')} · ${r.get('amount', 0):,.2f}"):
        st.markdown(f"**One-line verdict:** {synth.get('one_line_verdict', '—')}")
        st.markdown(f"**Confidence:** {synth.get('confidence', '—').title()}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Financial Health**")
            fin = r.get("financial", {})
            st.write(f"- Score: {fin.get('health_score')}/100")
            st.write(f"- Verdict: {fin.get('verdict')}")
            st.write(f"- Opportunity cost: {fin.get('opportunity_cost')}")

        with col2:
            st.markdown("**Product Intelligence**")
            prod = r.get("product", {})
            st.write(f"- Price assessment: {prod.get('price_assessment', '—')}")
            st.write(f"- Sensible low: ${prod.get('sensible_lowest_price', '—')}")
            st.write(f"- Value score: {prod.get('value_score', '—')}/100")

        st.markdown("**Coaching Message**")
        st.info(r.get("coach", {}).get("coaching_message", "—"))

        if r.get("deals", {}).get("triggered"):
            st.markdown("**Deal Hunter triggered** — alternatives were suggested.")

if st.button("Clear history", type="secondary"):
    st.session_state.history = []
    st.rerun()
