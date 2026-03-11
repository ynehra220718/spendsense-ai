import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from tools.price_source import get_product_from_url, get_all_mock_products, get_platform_label, detect_platform
from agents import orchestrator
from ui.components.financial_health_gauge import render_financial_health_gauge
from ui.components.recommendation_card import render_recommendation_card

st.set_page_config(page_title="Purchase Check · SpendSense AI", page_icon="🛒", layout="wide")

# ── Guard: must have a profile ──────────────────────────────────────────────
if "user_profile" not in st.session_state or not st.session_state.user_profile:
    st.warning("Please select a profile first.")
    if st.button("Go to profile selection"):
        st.switch_page("pages/01_onboarding.py")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

profile = st.session_state.user_profile
user_id = st.session_state.user_id

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🛒 Purchase Check")
st.caption(f"Evaluating as **{profile['name']}** · {profile.get('occupation', '')} · {profile.get('location', '')}")
st.divider()

# ── Demo scenario shortcuts ─────────────────────────────────────────────────
with st.expander("⚡ Quick demo scenarios", expanded=False):
    st.caption("Pre-built scenarios that match the three research personas.")
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.markdown("**Scenario A — Priya**")
        st.write("Instant Pot · $280 · Expected: CAUTION")
        if st.button("Load Scenario A", key="demo_a"):
            st.session_state.demo_product_id = "instant-pot-duo-7in1"
            st.session_state.demo_price = 279.99
    with dc2:
        st.markdown("**Scenario B — Marcus**")
        st.write("Dell XPS 15 Laptop · $1,200 · Expected: NOT_RECOMMENDED")
        if st.button("Load Scenario B", key="demo_b"):
            st.session_state.demo_product_id = "dell-xps-15-laptop"
            st.session_state.demo_price = 1199.99
    with dc3:
        st.markdown("**Scenario C — Destiny**")
        st.write("Nike Air Max 270 · $95 · Expected: CAUTION / NOT_RECOMMENDED")
        if st.button("Load Scenario C", key="demo_c"):
            st.session_state.demo_product_id = "nike-air-max-270"
            st.session_state.demo_price = 94.99

st.divider()

# ── Input form ──────────────────────────────────────────────────────────────
st.subheader("What are you thinking of buying?")

input_mode = st.radio(
    "Input method",
    ["Paste a product URL", "Select from demo catalog"],
    horizontal=True,
)

product_url = None
product_id = None
purchase_amount = None
product_data = None

if input_mode == "Paste a product URL":
    url_input = st.text_input(
        "Product URL",
        placeholder="https://www.amazon.in/dp/B00FLYWNYQ  or  https://www.flipkart.com/...",
        help="Supports Amazon (all regions) and Flipkart. Other platforms use demo data.",
    )
    if url_input:
        platform = detect_platform(url_input)
        platform_label = get_platform_label(url_input)
        platform_icons = {
            "amazon": "🟠", "flipkart": "🔵", "myntra": "🩷",
            "meesho": "🟣", "snapdeal": "🔴", "unknown": "⚪"
        }
        st.caption(f"Detected platform: {platform_icons.get(platform, '⚪')} **{platform_label}**")
        if platform in ("flipkart", "myntra", "meesho", "snapdeal", "unknown"):
            st.info("ℹ️ No free price history API exists for this platform — using demo data to show how SpendSense would work.")
        product_url = url_input

    price_override = st.number_input(
        "Purchase price (₹ or $)", min_value=0.0, step=0.01,
        help="Enter the price you see on the page."
    )
    purchase_amount = price_override if price_override > 0 else None

else:
    # Demo catalog selector
    all_products = get_all_mock_products()
    product_names = {p["id"]: f"{p['name']} (${p['current_price']})" for p in all_products}

    default_id = st.session_state.get("demo_product_id", all_products[0]["id"])
    selected_id = st.selectbox(
        "Choose a product",
        options=list(product_names.keys()),
        format_func=lambda x: product_names[x],
        index=list(product_names.keys()).index(default_id) if default_id in product_names else 0,
    )
    product_id = selected_id

    default_price = st.session_state.get("demo_price", None)
    price_override = st.number_input(
        "Override price (optional)",
        min_value=0.0,
        value=float(default_price) if default_price else 0.0,
        step=0.01,
    )
    purchase_amount = price_override if price_override > 0 else None

    # Clear demo state after consuming it
    st.session_state.pop("demo_product_id", None)
    st.session_state.pop("demo_price", None)

# ── Evaluate button ─────────────────────────────────────────────────────────
st.divider()
run_eval = st.button("🔍  Evaluate this purchase", type="primary", use_container_width=True)

if run_eval:
    if not product_url and not product_id:
        st.error("Please enter a product URL or select a product.")
        st.stop()

    with st.spinner("Agents are analysing your purchase… this takes 5–10 seconds."):
        try:
            result = orchestrator.run(
                user_id=user_id,
                product_url=product_url,
                product_id=product_id,
                purchase_amount=purchase_amount,
            )

            # Attach raw product data for price chart rendering
            if product_url:
                result["_product_data"] = get_product_from_url(product_url)
            elif product_id:
                from tools.price_source import get_product_by_id
                result["_product_data"] = get_product_by_id(product_id) or {}

            # Save to session history
            st.session_state.history.append(result)

        except Exception as e:
            st.error(f"Evaluation failed: {e}")
            st.stop()

    st.success("Analysis complete!")
    st.divider()

    # ── Results ──────────────────────────────────────────────────────────────
    render_financial_health_gauge(result.get("financial", {}))
    st.divider()
    render_recommendation_card(result)
