# SpendSense AI — Product Roadmap

---

## Roadmap Philosophy

SpendSense is built in three distinct phases with explicit gates between them. Each phase must prove a specific hypothesis before the next begins. This prevents over-building on unvalidated assumptions — a common failure mode in AI product development.

| Phase | Hypothesis to Prove | Gate Condition |
|---|---|---|
| Phase 1 | Multi-agent AI can produce meaningfully better purchase guidance than a single prompt | 3 demo scenarios work, coaching varies by persona, <8s latency |
| Phase 2 | Real users will change purchase behavior based on SpendSense recommendations | >40% recommendation acceptance rate, >35% 30-day retention |
| Phase 3 | SpendSense can scale with a sustainable distribution + monetization model | >1K MAU, >8% free-to-premium conversion, 1 employer partnership |

---

## Phase 1 — Prototype (Months 1–3)
**Theme:** Prove the agent architecture. Ship something demoable.

### What We Build
- All 5 agents operational (Financial Health, Product Intelligence, Behavioral Coach, Deal Hunter, Orchestrator)
- Mock user profiles (Priya, Marcus, Destiny) grounded in real financial research data
- Mock product catalog with realistic price history including anomaly filtering
- Platform auto-detection from URL (Amazon, Flipkart, Myntra, Meesho, Snapdeal)
- Streamlit web app: Onboarding → Purchase Check → History
- CamelCamelCamel free API integration for live Amazon price history (optional, zero-cost)

### What We Explicitly Do Not Build
- Real bank account connections
- User accounts or persistent storage
- Chrome extension (JS required — deferred to Phase 2)
- Payment or monetization

### Deliverables
- Working Streamlit demo (Streamlit Cloud hosted)
- GitHub repo (public, portfolio-ready)
- README with architecture diagram and demo instructions
- All 6 PM artifacts completed
- 3-minute demo video recorded

### Success Criteria (Phase Gate)
- [ ] All 3 demo scenarios produce expected verdicts
- [ ] Coaching messages differ meaningfully between Priya and Destiny for the same product
- [ ] End-to-end latency <8s (P90) across 10 test runs
- [ ] Price anomaly filtering works correctly on all mock products
- [ ] PM artifacts tell a consistent story: personas → user stories → RICE → OKRs

---

## Phase 2 — Closed Beta (Months 4–9)
**Theme:** Validate real behavior change with 20 users over 30 days.

### What We Build
- **Plaid integration:** Connect real bank accounts for actual financial health scoring (replaces mock profiles)
- **User accounts + auth:** Persistent profiles, evaluation history stored securely
- **Chrome extension (V1):** Activates on Amazon and Flipkart product pages — no tab switching
  - Built in JavaScript + Manifest V3
  - Sends product data to Python backend via API
  - Displays recommendation in a sidebar overlay
- **Feedback loops:** 7-day post-evaluation survey, 24h behavior check ("did you buy it?")
- **Real price data:** CamelCamelCamel for Amazon; web scraping layer for Flipkart (legal grey area — document clearly)
- **Model A/B testing:** OpenRouter makes it trivial to compare Claude vs. GPT-4o on coaching quality

### Distribution Strategy (Phase 2)
- Build in public on LinkedIn (weekly posts documenting the build)
- Seed r/personalfinance and r/ynab with genuine value posts
- Personal outreach to 50 target users matching Priya/Marcus/Destiny profiles
- 5 micro-influencer partnerships (50K–500K followers, personal finance niche)

### Success Criteria (Phase Gate)
- [ ] 20 users complete 30-day beta
- [ ] Recommendation acceptance rate >40%
- [ ] 7-day PDQS >55%
- [ ] 30-day retention >35%
- [ ] NPS ≥35

---

## Phase 3 — Scale (Months 10–18)
**Theme:** Distribution + monetization at 1K MAU.

### What We Build
- **WhatsApp / Telegram bot:** Paste a product link, get analysis back — zero install, maximum reach for India market
- **Employer benefits channel:** Partner with HR platforms (Sequoia, Benefitfocus) to offer SpendSense as a financial wellness benefit
- **Premium tier:** SpendSense Premium at $9.99/mo (unlimited evaluations, advanced deal hunting, weekly financial health digest)
- **Family plan:** $14.99/mo (3 users, shared spending insights — privacy-first, no cross-user comparison)
- **Mobile app:** React Native wrapper around the web app — iOS/Android distribution

### Monetization Model
| Tier | Price | Features | Target User |
|---|---|---|---|
| Free | $0 | 10 evaluations/month, mock data | Acquisition / top of funnel |
| Premium | $9.99/mo | Unlimited evals, Plaid integration, deal alerts | Priya / Marcus |
| Family | $14.99/mo | 3 users, shared insights | Households |
| Employer | Custom | Bulk licensing via HR platform | Phase 3 distribution channel |

### Beachhead Market
Millennial women aged 25–35 in the US with annual income $50K–$120K and at least one active financial goal. This cohort has the highest financial anxiety, highest e-commerce activity, and highest openness to financial coaching tools. Destiny and Priya represent the two ends of this spectrum.

### Success Criteria (Phase Gate)
- [ ] 1,000 MAU
- [ ] PDQS >65%
- [ ] NPS ≥45
- [ ] Free-to-Premium conversion ≥8%
- [ ] 1 employer benefits partnership signed

---

## What We Are Not Building (Explicit Deprioritization)

| Feature | Rationale |
|---|---|
| Social comparison / peer spending | Behavioral economics shows this increases spending, not decreases it. Antithetical to mission. |
| Investment advice | Regulatory risk. Out of scope for V1–V3. |
| Tax optimization | Different product category. Requires CPA-level accuracy. |
| Buy Now Pay Later integration | We are solving for financial health. Integrating BNPL would undermine that. |
| Crypto / NFT tracking | Not relevant to impulse purchase decisions. Scope creep. |
