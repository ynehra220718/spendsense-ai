# SpendSense AI — Product Requirements Document

**Version:** 1.0
**Author:** Portfolio Project — Deloitte USI Analyst transitioning to PM
**Status:** Draft
**Last Updated:** March 2026

---

## 1. Problem Statement

### The Gap No One Has Filled

| Product | What It Does | What It Misses |
|---|---|---|
| Mint / YNAB | Tracks spending after the fact | No real-time purchase intercept |
| Honey / Rakuten | Finds coupons at checkout | Ignores personal financial health |
| Affirm / Klarna | Enables installment payments | Actively encourages overspending |
| ChatGPT (manual) | Answers financial questions | No personal data, no product context |
| **SpendSense AI** | Intercepts the decision moment with personal financial context + AI coaching | This is the gap |

**The moment that matters is the 30 seconds before "Buy Now."**
No existing product owns that moment with both financial context and behavioral intelligence.

### Market Size
- 78M US Millennials and Gen Z with both financial anxiety and high e-commerce activity
- $440B/year in impulse purchases in the US
- 74% of Millennials impulse buy regularly; 9 in 10 impulse buy on social media (GoDaddy, 2024)
- 52.3% of Millennials rate financial stress impact on mood at 7+/10 (PlanAdviser)
- 48% of Gen Z financially insecure in 2025, up 60% from 2024 (Deloitte)

---

## 2. Product Vision

> **"Before you click Buy Now, SpendSense tells you if you should."**

SpendSense AI is a multi-agent AI copilot that evaluates e-commerce purchase decisions in real time using personal financial data, price intelligence, and behavioral coaching grounded in consumer psychology.

---

## 3. Goals and Non-Goals

### Goals (V1)
- Evaluate any purchase in under 8 seconds
- Deliver a verdict (RECOMMENDED / CAUTION / NOT_RECOMMENDED) with clear rationale
- Provide behavioral coaching tailored to user's financial persona
- Surface price history and identify sensible historical lows
- Trigger deal-finding when financial health is under strain
- Demonstrate multi-agent AI architecture as a portfolio differentiator

### Non-Goals (V1 — explicit)
- No real bank account connection (manual profile entry only)
- No purchases made on behalf of users
- No legal or fiduciary financial advice
- No persistent transaction history storage across sessions
- No social comparison features (deliberately excluded — see RICE document)
- No support for cryptocurrency, investments, or tax optimization

---

## 4. User Personas

See `/pm_artifacts/user_personas.md` for full persona sheets.

| Persona | Age | Income | Core Need |
|---|---|---|---|
| Priya | 28 | $95K engineer | Real-time go/no-go with honest rationale |
| Marcus | 34 | $72K ops manager | Agent-curated alternative analysis |
| Destiny | 25 | $48K nonprofit | Non-judgmental coaching that builds literacy |

---

## 5. User Stories

### Epic 1: Profile & Onboarding
1. As a new user, I want to select a financial profile so that SpendSense can personalize its evaluation to my real situation.
2. As a user, I want to see a summary of my financial health snapshot before I evaluate a purchase, so I have context for the recommendation.
3. As a user, I want my profile to persist within a session so I don't have to re-enter it for every evaluation.

### Epic 2: Purchase Evaluation
4. As Priya, I want to paste an Amazon product URL and get an evaluation within 8 seconds so I don't lose my purchase momentum while waiting.
5. As Marcus, I want to see how the current price compares to the product's historical low so I can decide if now is a good time to buy.
6. As Destiny, I want to understand the opportunity cost of my purchase in concrete terms (e.g., "2 months of your BNPL payoff") not abstract percentages.
7. As any user, I want the verdict to be a single clear signal (green/yellow/red) so I can act immediately without reading a paragraph.
8. As a user on Flipkart, I want SpendSense to still work even if live price data isn't available — using demo data is fine as long as I know that's what it's showing.
9. As a user, I want to override the product price manually so I can evaluate prices I see in-store or on a different platform.

### Epic 3: Behavioral Coaching
10. As Destiny, I want the coaching message to feel warm and non-judgmental so I don't feel ashamed for wanting something nice.
11. As Marcus, I want the coach to name the specific bias at play (e.g., "research justification trap") so I can recognize the pattern myself.
12. As Priya, I want to understand why I feel the urge to buy — not just whether I should — so I build financial self-awareness over time.

### Epic 4: Deal Hunter
13. As Marcus evaluating a $1,200 laptop, I want three concrete alternatives (best price, wait, creative) so I have actionable next steps if I decide not to buy now.
14. As Destiny, I want the Deal Hunter to tell me where to find the alternative — not just that a cheaper option exists — so I can actually act on it.
15. As a user, I want to know why Deal Hunter was triggered (my health score was below 60) so the system feels transparent, not paternalistic.

---

## 6. Functional Requirements by Agent

### Orchestrator
- FR-O1: Must sequence Financial Health → Product Intelligence → Behavioral Coach → Deal Hunter in order
- FR-O2: Must pass outputs from earlier agents as context to later agents
- FR-O3: Must produce a unified synthesis object with final_verdict, confidence, one_line_verdict, key_factors
- FR-O4: Must complete full pipeline in ≤8 seconds (P90 target)
- FR-O5: Must expose data_source field indicating mock vs. live data

### Financial Health Agent
- FR-F1: Must output health_score (0-100), verdict, opportunity_cost, timing_recommendation, rationale
- FR-F2: Score bands: 0-40 = NOT_RECOMMENDED, 41-60 = CAUTION, 61-100 = RECOMMENDED
- FR-F3: Opportunity cost must be expressed in concrete terms relative to user's actual financial data
- FR-F4: Must consider monthly surplus, debt load, savings buffer, and purchase as % of monthly income

### Product Intelligence Agent
- FR-P1: Must output price_assessment (GOOD_DEAL / FAIR_PRICE / OVERPRICED), sensible_lowest_price, excluded_anomalies
- FR-P2: Must filter price history anomalies: exclude prices lasting <3 days or >40% below median
- FR-P3: Must explain any filtered anomaly in excluded_anomalies array
- FR-P4: Must output value_score (0-100) and market_context summary

### Behavioral Coach Agent
- FR-B1: Must tailor tone to persona_type (budget_guilt / comparison_shopper / rebuilding_finances)
- FR-B2: Must detect and name at least one behavioral bias when applicable
- FR-B3: Coaching message must be 2-4 sentences, no bullet points, conversational tone
- FR-B4: Must never use the phrase "can't afford" — must use timing/opportunity framing instead

### Deal Hunter Agent
- FR-D1: Must trigger only when financial health score < 60
- FR-D2: Must return exactly 3 alternatives: best_price, wait, creative
- FR-D3: Each alternative must include estimated_price_range, saving_vs_current, where_to_find
- FR-D4: Must not suggest specific URLs — platform/channel names only

---

## 7. Non-Functional Requirements

| Requirement | Target | Notes |
|---|---|---|
| Response time (P90) | ≤8 seconds | Full agent pipeline end-to-end |
| Response time (P50) | ≤5 seconds | Typical case |
| Model swappability | Zero code changes | All model IDs in .env only |
| Platform detection accuracy | 100% for Amazon/Flipkart | Regex-based, deterministic |
| Data privacy | No PII stored | Session-only profile data |
| Uptime (demo) | 99% | Streamlit Cloud free tier |

---

## 8. Success Metrics

| Metric | Target | How Measured |
|---|---|---|
| Purchase Decision Quality Score | >65% satisfied 7 days post-CAUTION eval | Post-decision survey (V2) |
| Recommendation acceptance rate | >40% of CAUTION/NOT_RECOMMENDED → delay/abandon | Session behavior tracking (V2) |
| Time to recommendation | <8s P90 | Instrumented in orchestrator |
| 30-day retention | >35% | Streamlit analytics (V2) |
| NPS | 45+ by end of Phase 2 | In-app survey |

---

## 9. Open Questions

1. **Trust calibration:** How do we handle the case where a CAUTION recommendation is wrong and the user later regrets following it? What's the feedback loop?
2. **Plaid integration (Phase 2):** What's the minimum viable data pull from bank accounts that improves recommendation quality without creating a privacy liability?
3. **Chrome extension (V1):** How do we handle single-page apps (React-based product pages) where the DOM updates without a page reload?
4. **India market:** Should pricing, currency, and platform detection be configurable by region, or hardcoded for US/India dual-market launch?
5. **Fiduciary risk:** At what recommendation specificity does SpendSense begin to approach regulated financial advice? Need legal review before Phase 2.
