# SpendSense AI — OKRs and KPIs

---

## North Star Metric

**Purchase Decision Quality Score (PDQS)**
*"% of users who report satisfaction with their purchase decision 7 days after receiving a CAUTION or NOT_RECOMMENDED evaluation"*

### Why This Is the Right North Star
- It measures actual outcome quality, not engagement (engagement can be gamed by making the app addictive)
- It aligns product incentives with user wellbeing — we win when users make better decisions, not just more evaluations
- It's measurable with a simple 7-day follow-up prompt: "Looking back, are you happy with what you decided?"
- It directly addresses the trust risk: one bad recommendation that causes regret is more damaging than 10 missed evaluations

**Target by end of Phase 2:** >65% of users report satisfaction with their decision 7 days post-evaluation

---

## OKRs by Phase

### Phase 1 — Prototype (Months 1–3)

**Objective:** Ship a working multi-agent prototype that demonstrates the core value proposition and withstands portfolio interview scrutiny.

| Key Result | Target | Measurement |
|---|---|---|
| KR1 | All 5 agents (Financial Health, Product Intelligence, Behavioral Coach, Deal Hunter, Orchestrator) operational | Binary — works / doesn't work |
| KR2 | 3 demo scenarios (Priya/Marcus/Destiny) produce meaningfully different coaching messages | Qualitative review — coach output varies by persona |
| KR3 | End-to-end evaluation completes in <8 seconds (P90) across 10 test runs | Instrumented timer in orchestrator |
| KR4 | Price history anomaly filtering correctly excludes 1-day errors in all 3 mock products | Unit test pass/fail |
| KR5 | Platform auto-detection correctly identifies Amazon, Flipkart, and unknown URLs | 10 URL test cases, 100% accuracy |

---

### Phase 2 — Closed Beta (Months 4–9)

**Objective:** Validate that SpendSense changes real purchase behavior with 20 actual users over 30 days.

| Key Result | Target | Measurement |
|---|---|---|
| KR1 | 20 beta users complete onboarding and run ≥3 evaluations in first week | Beta cohort tracking |
| KR2 | Recommendation acceptance rate >40% (CAUTION/NOT_RECOMMENDED → user delays or abandons purchase) | Post-evaluation follow-up survey at 24h |
| KR3 | Purchase Decision Quality Score >55% (7-day follow-up survey) | 7-day email/in-app prompt |
| KR4 | 30-day retention >35% (users who return after first evaluation) | Session analytics |
| KR5 | NPS ≥35 from beta cohort | End-of-beta NPS survey |
| KR6 | Plaid integration live for at least 10 users with real bank data | Feature flag rollout |

---

### Phase 3 — Scale (Months 10–18)

**Objective:** Reach 1,000 monthly active users and establish a distribution channel for sustained growth.

| Key Result | Target | Measurement |
|---|---|---|
| KR1 | 1,000 monthly active users (≥1 evaluation/month) | Product analytics |
| KR2 | Purchase Decision Quality Score >65% | 7-day follow-up (automated) |
| KR3 | NPS ≥45 | Quarterly in-app survey |
| KR4 | Chrome extension published with >500 installs | Chrome Web Store analytics |
| KR5 | 1 employer benefits partnership signed (HR/wellness program) | Partnership agreement |
| KR6 | Free-to-Premium conversion rate ≥8% | Revenue analytics |

---

## Supporting KPIs Dashboard

| KPI | Definition | Target (Phase 2) | Target (Phase 3) |
|---|---|---|---|
| **Evaluation completion rate** | % of evaluations started that reach final recommendation | >85% | >90% |
| **Time to recommendation (P50)** | Median seconds from submit to result | <5s | <4s |
| **Time to recommendation (P90)** | 90th percentile seconds | <8s | <6s |
| **Deal Hunter trigger rate** | % of evaluations where Deal Hunter fires (score <60) | ~40% (expected for beta cohort) | Track for calibration |
| **Recommendation acceptance rate** | CAUTION/NOT_RECOMMENDED → user reports delay/abandon at 24h | >40% | >50% |
| **7-day PDQS** | % satisfied with decision 7 days later | >55% | >65% |
| **30-day retention** | % users returning after first evaluation | >35% | >45% |
| **Session depth** | Avg evaluations per session | >1.5 | >2.0 |
| **NPS** | Net Promoter Score | ≥35 | ≥45 |
| **Free-to-Premium conversion** | % converting within 30 days | N/A (Phase 2) | ≥8% |

---

## Anti-Metrics (What We Will Not Optimize For)

These metrics could go up while the product gets worse — we explicitly track them as health checks, not growth targets:

| Anti-Metric | Why We Don't Optimize For It |
|---|---|
| Total evaluations per user | High evaluation frequency could mean the app is being used as a dopamine loop, not a decision tool |
| Time in app | Longer sessions don't mean better decisions — we want fast, confident recommendations |
| Social sharing rate | Financial data sharing creates privacy risk; social proof drives the spending we're trying to reduce |
| CAUTION/NOT_RECOMMENDED rate | Artificially high discouragement rate would reflect poor calibration, not product health |

---

## Measurement Infrastructure (Phase 2 Plan)

1. **7-day follow-up:** Automated prompt (email or in-app) with single question: *"Looking back, are you happy with the decision you made about [product]?"* — binary yes/no with optional free text
2. **24-hour behavior check:** *"Did you end up buying [product]?"* — tracks recommendation acceptance for CAUTION/NOT_RECOMMENDED cases
3. **Session analytics:** Track evaluation starts, completions, agent errors, and elapsed time
4. **NPS cadence:** End of onboarding month + quarterly thereafter
