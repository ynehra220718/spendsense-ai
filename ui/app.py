import sys
from pathlib import Path

# Ensure project root is on path when running from ui/
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

st.set_page_config(
    page_title="SpendSense AI",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global session state defaults ──────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar nav ────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/idea.png", width=56)
    st.title("SpendSense AI")
    st.caption("Before you click Buy Now,\nSpendSense tells you if you should.")
    st.divider()

    if st.session_state.user_profile:
        st.success(f"Signed in as **{st.session_state.user_profile['name']}**")
        if st.button("Switch profile", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_profile = None
            st.switch_page("pages/01_onboarding.py")
    else:
        st.warning("No profile selected.")
        if st.button("Select profile →", use_container_width=True):
            st.switch_page("pages/01_onboarding.py")

    st.divider()
    st.caption("v0.1 · Portfolio project · Mock data")

# ── Landing page ───────────────────────────────────────────────────────────
st.title("💡 SpendSense AI")
st.subheader("A multi-agent AI copilot for smarter purchase decisions.")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Financial Health Agent**\nEvaluates affordability against your real financial picture.")
with col2:
    st.info("**Product Intelligence Agent**\nAnalyzes price fairness and surfaces your best historical price.")
with col3:
    st.info("**Behavioral Coach Agent**\nDelivers persona-tailored coaching grounded in behavioral economics.")

st.divider()
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🚀  Start a purchase check", use_container_width=True, type="primary"):
        if st.session_state.user_profile:
            st.switch_page("pages/02_purchase_check.py")
        else:
            st.switch_page("pages/01_onboarding.py")
with col_b:
    if st.button("📋  View evaluation history", use_container_width=True):
        st.switch_page("pages/03_history.py")
