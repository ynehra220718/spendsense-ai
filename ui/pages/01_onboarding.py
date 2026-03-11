import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from tools.user_tools import load_user_profile, list_user_profiles

st.set_page_config(page_title="Select Profile · SpendSense AI", page_icon="👤", layout="wide")

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── Persona cards ──────────────────────────────────────────────────────────
PERSONA_META = {
    "priya": {
        "emoji": "👩‍💻",
        "tagline": "Software Engineer · Austin, TX · 28",
        "blurb": "Earns well but carries credit card debt and budget guilt. Needs a clear go/no-go with honest rationale.",
        "color": "blue",
    },
    "marcus": {
        "emoji": "📊",
        "tagline": "Operations Manager · Columbus, OH · 34",
        "blurb": "Analytical comparison shopper with hidden BNPL debt. Needs data-driven alternatives when finances are tight.",
        "color": "orange",
    },
    "destiny": {
        "emoji": "🌱",
        "tagline": "Nonprofit Coordinator · Atlanta, GA · 25",
        "blurb": "Rebuilding finances after setbacks. Needs non-judgmental coaching that celebrates small wins.",
        "color": "green",
    },
}

st.title("👤 Choose a Profile")
st.caption("Select a demo persona to begin. Each profile is built from real 2024–2025 financial research data.")
st.divider()

profiles = list_user_profiles()
cols = st.columns(len(profiles))

selected_id = None
for col, pid in zip(cols, profiles):
    meta = PERSONA_META.get(pid, {"emoji": "👤", "tagline": pid, "blurb": "", "color": "gray"})
    profile = load_user_profile(pid)
    with col:
        st.subheader(f"{meta['emoji']} {profile['name']}")
        st.caption(meta["tagline"])
        st.write(meta["blurb"])
        monthly_net = profile.get("monthly_income", 0)
        monthly_exp = profile.get("monthly_expenses", 0)
        surplus = monthly_net - monthly_exp
        st.metric("Monthly Net Income", f"${monthly_net:,.0f}")
        st.metric("Monthly Surplus", f"${surplus:,.0f}", delta=f"${surplus:,.0f} left after expenses")
        st.metric("Total Debt", f"${profile.get('total_debt', 0):,.0f}")
        st.metric("Savings", f"${profile.get('savings', 0):,.0f}")
        if st.button(f"Select {profile['name']}", key=pid, use_container_width=True, type="primary"):
            selected_id = pid

if selected_id:
    profile = load_user_profile(selected_id)
    st.session_state.user_id = selected_id
    st.session_state.user_profile = profile
    st.success(f"Profile set to **{profile['name']}**. Redirecting to purchase check…")
    st.switch_page("pages/02_purchase_check.py")

# ── Full profile expander ──────────────────────────────────────────────────
st.divider()
st.subheader("Full Profile Details")
for pid in profiles:
    profile = load_user_profile(pid)
    meta = PERSONA_META.get(pid, {})
    with st.expander(f"{meta.get('emoji','👤')} {profile['name']} — full breakdown"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Income & Surplus**")
            st.write(f"- Annual gross: ${profile.get('income', {}).get('annual_gross', 0):,.0f}")
            st.write(f"- Monthly net: ${profile.get('monthly_income', 0):,.0f}")
            st.write(f"- Monthly expenses: ${profile.get('monthly_expenses', 0):,.0f}")
            surplus = profile.get('monthly_income', 0) - profile.get('monthly_expenses', 0)
            st.write(f"- Monthly surplus: ${surplus:,.0f}")
            st.markdown("**Savings**")
            savings_breakdown = profile.get("savings_breakdown", {})
            for k, v in savings_breakdown.items():
                if k != "note" and isinstance(v, (int, float)):
                    st.write(f"- {k.replace('_', ' ').title()}: ${v:,.0f}")
        with col2:
            st.markdown("**Debt Breakdown**")
            debt = profile.get("debt_breakdown", {})
            for k, v in debt.items():
                if "note" not in k and isinstance(v, (int, float)) and v > 0:
                    st.write(f"- {k.replace('_', ' ').title()}: ${v:,.0f}")
            st.markdown("**Financial Goals**")
            for goal in profile.get("financial_goals", []):
                st.write(f"- {goal}")
        st.markdown("**Behavioral Profile**")
        bp = profile.get("behavioral_profile", {})
        st.info(f"💬 *\"{bp.get('money_script', '')}\"*")
        st.write(f"**Anxiety level:** {bp.get('financial_anxiety_level', 'unknown').title()}")
        st.markdown("**Spending triggers:**")
        for t in bp.get("spending_triggers", []):
            st.write(f"- {t}")
