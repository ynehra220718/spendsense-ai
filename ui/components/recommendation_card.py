import streamlit as st
import pandas as pd


def render_recommendation_card(result: dict):
    """Renders the full unified recommendation card from orchestrator output."""
    synthesis = result.get("synthesis", {})
    coach = result.get("coach", {})
    product_r = result.get("product", {})
    deals = result.get("deals", {})
    product_data = result.get("_product_data", {})

    verdict = synthesis.get("final_verdict", "CAUTION")
    confidence = synthesis.get("confidence", "medium")
    one_liner = synthesis.get("one_line_verdict", "")
    key_factors = synthesis.get("key_factors", [])
    elapsed = result.get("elapsed_seconds", 0)

    # ── Verdict banner ──────────────────────────────────────────────────────
    VERDICT_CONFIG = {
        "RECOMMENDED": {"color": "#1a7f37", "bg": "#d4edda", "icon": "✅", "label": "Recommended"},
        "CAUTION":     {"color": "#856404", "bg": "#fff3cd", "icon": "⚠️", "label": "Caution"},
        "NOT_RECOMMENDED": {"color": "#842029", "bg": "#f8d7da", "icon": "🚫", "label": "Not Recommended"},
    }
    cfg = VERDICT_CONFIG.get(verdict, VERDICT_CONFIG["CAUTION"])

    st.markdown(
        f"""
        <div style="background:{cfg['bg']};border-left:6px solid {cfg['color']};
                    padding:20px 24px;border-radius:8px;margin-bottom:16px;">
            <h2 style="color:{cfg['color']};margin:0 0 6px 0;">{cfg['icon']} {cfg['label']}</h2>
            <p style="font-size:1.1rem;margin:0;color:#333;">{one_liner}</p>
            <p style="font-size:0.8rem;color:#666;margin:8px 0 0 0;">
                Confidence: <strong>{confidence.title()}</strong> &nbsp;·&nbsp;
                Analysis time: <strong>{elapsed}s</strong> &nbsp;·&nbsp;
                Data: <strong>{result.get('data_source','mock').title()}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Key factors ─────────────────────────────────────────────────────────
    if key_factors:
        st.markdown("**Key factors:**")
        for f in key_factors:
            st.write(f"- {f}")

    st.divider()

    # ── Price intelligence + history ────────────────────────────────────────
    col_price, col_coach = st.columns([1, 1])

    with col_price:
        st.markdown("#### 📈 Price Intelligence")
        price_assess = product_r.get("price_assessment", "—")
        assess_icons = {"GOOD_DEAL": "🟢", "FAIR_PRICE": "🟡", "OVERPRICED": "🔴"}
        st.markdown(f"**Price Assessment:** {assess_icons.get(price_assess, '⚪')} {price_assess.replace('_', ' ').title()}")

        current = product_r.get("current_price") or result.get("amount", 0)
        sensible_low = product_r.get("sensible_lowest_price")
        sensible_date = product_r.get("sensible_lowest_date", "")

        m1, m2 = st.columns(2)
        m1.metric("Current Price", f"${current:,.2f}" if current else "—")
        if sensible_low:
            delta_pct = ((current - sensible_low) / sensible_low * 100) if current else 0
            m2.metric(
                "Sensible Historical Low",
                f"${sensible_low:,.2f}",
                delta=f"{delta_pct:+.0f}% vs current" if delta_pct else None,
                delta_color="inverse",
            )

        if sensible_date:
            st.caption(f"Lowest sustained price recorded: {sensible_date}")

        excluded = product_r.get("excluded_anomalies", [])
        if excluded:
            with st.expander("⚠️ Price anomalies filtered out"):
                for e in excluded:
                    st.write(f"- {e}")

        market_ctx = product_r.get("market_context", "")
        if market_ctx:
            st.info(market_ctx)

        # Price history chart
        if product_data.get("price_history"):
            st.markdown("**Price history:**")
            df = pd.DataFrame(product_data["price_history"])
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            st.area_chart(df["price"], height=180)

    # ── Behavioral coach ────────────────────────────────────────────────────
    with col_coach:
        st.markdown("#### 🧠 Behavioral Coach")
        coaching_msg = coach.get("coaching_message", "")
        bias = coach.get("bias_detected")
        tone = coach.get("tone", "")
        insight = coach.get("behavioral_insight", "")

        tone_icons = {"affirming": "😊", "cautionary": "🤔", "redirecting": "🔄"}
        st.markdown(
            f"""
            <div style="background:#f0f4ff;border-radius:8px;padding:16px 20px;margin-bottom:12px;">
                <p style="font-size:1.05rem;margin:0;color:#1a1a2e;line-height:1.6;">{coaching_msg}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"{tone_icons.get(tone, '💬')} Tone: {tone.title()}")

        if bias:
            st.warning(f"**Bias detected:** {bias}")
        if insight:
            with st.expander("Behavioral insight"):
                st.write(insight)

    # ── Deal Hunter ─────────────────────────────────────────────────────────
    if deals.get("triggered"):
        st.divider()
        st.markdown("#### 🔍 Deal Hunter — Smarter Alternatives")
        st.caption(deals.get("deal_hunter_summary", ""))

        TYPE_ICONS = {"best_price": "💰", "wait": "⏳", "creative": "💡"}
        alt_cols = st.columns(len(deals.get("alternatives", [])))

        for col, alt in zip(alt_cols, deals.get("alternatives", [])):
            with col:
                atype = alt.get("type", "")
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd;border-radius:8px;padding:14px 16px;height:100%;">
                        <h5 style="margin:0 0 6px 0;">{TYPE_ICONS.get(atype, '🔹')} {alt.get('title','')}</h5>
                        <p style="font-size:0.9rem;color:#444;margin:0 0 8px 0;">{alt.get('description','')}</p>
                        <p style="margin:4px 0;"><strong>Price:</strong> {alt.get('estimated_price_range','')}</p>
                        <p style="margin:4px 0;color:green;"><strong>{alt.get('saving_vs_current','')}</strong></p>
                        <p style="font-size:0.82rem;color:#666;margin:6px 0 0 0;">📍 {alt.get('where_to_find','')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
