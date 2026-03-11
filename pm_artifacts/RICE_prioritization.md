# SpendSense AI — RICE Prioritization

**Framework:** RICE Score = (Reach × Impact × Confidence) / Effort
**Scale:** Reach (users/month), Impact (0.25–3x), Confidence (%), Effort (person-months)

---

## Scoring Definitions

| Factor | Scale |
|---|---|
| **Reach** | Estimated users impacted per month (10 = 10 users) |
| **Impact** | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **Confidence** | % certainty in estimates (100% = certain, 50% = rough guess) |
| **Effort** | Person-months to build and ship (solo developer) |

---

## Feature Backlog — Scored

| # | Feature | Reach | Impact | Confidence | Effort | RICE Score | Decision |
|---|---|---|---|---|---|---|---|
| 1 | **Core purchase evaluation flow** (all 4 agents + orchestrator) | 100 | 3 | 90% | 2.0 | **135** | ✅ Build — foundational, everything depends on this |
| 2 | **Price history chart with sensible low filtering** | 100 | 2 | 85% | 0.5 | **340** | ✅ Build — high visual impact, low effort, core to trust |
| 3 | **Behavioral coaching with bias detection** | 100 | 3 | 80% | 1.0 | **240** | ✅ Build — primary differentiator from single-prompt AI |
| 4 | **Deal Hunter (3 alternatives when score <60)** | 60 | 2 | 85% | 0.5 | **204** | ✅ Build — highest value for distressed users |
| 5 | **Platform auto-detection from URL** | 100 | 1 | 95% | 0.3 | **317** | ✅ Build — required for demo credibility, easy to build |
| 6 | **Persona-based onboarding (3 profiles)** | 100 | 2 | 90% | 0.5 | **360** | ✅ Build — enables personalization, needed for demo |
| 7 | **Evaluation history page** | 80 | 1 | 80% | 0.3 | **213** | ✅ Build — shows longitudinal value, low effort |
| 8 | **Plaid bank account integration** | 100 | 3 | 60% | 4.0 | **45** | 🔜 Phase 2 — transforms from demo to real product |
| 9 | **Chrome browser extension** | 100 | 3 | 70% | 6.0 | **35** | 🔜 Phase 2 — ideal UX but JS build is a new language |
| 10 | **Social comparison ("friends also bought")** | 80 | 1 | 50% | 2.0 | **20** | ❌ Deprioritized — see rationale below |

---

## Deprioritized: Social Comparison Feature

**Feature:** Show anonymized peer spending data (e.g., "People with similar income spent $X on this category").

**Why explicitly deprioritized — three reasons:**

**1. Behavioral economics risk (primary reason)**
Social comparison in financial contexts is a well-documented driver of *increased* spending, not decreased spending. The "keeping up with the Joneses" effect is one of the strongest predictors of lifestyle creep (Frank, 2007; Leibenstein, 1950). A tool designed to *reduce* impulse spending should not introduce the primary psychological mechanism that *causes* it. Adding social comparison would undermine SpendSense's core behavioral thesis.

**2. Trust and privacy concern**
Financial data is the highest-sensitivity personal data category. Even anonymized peer comparisons require collecting and aggregating real user financial data. Before we have user trust established (Phase 2+), introducing social data creates a perception risk that outweighs the engagement benefit.

**3. Product focus**
SpendSense's differentiation is *individual financial health + behavioral coaching*, not social commerce. Adding social features risks diluting the brand toward "financial Instagram" — a crowded, low-trust space. Staying focused on the individual decision moment is the sharper, more defensible product position.

**Revisit condition:** If retention data in Phase 2 shows users want community accountability features (e.g., accountability partners, not comparison), revisit with a trust-first design. This is not a permanent no — it's a deliberate V1 exclusion.

---

## Phased Build Plan Summary

| Phase | Features | Rationale |
|---|---|---|
| **Phase 1 (now)** | Features 1–7: all core agent + UI features | Proves the concept, enables demo |
| **Phase 2** | Feature 8 (Plaid) + Feature 9 (Chrome extension) | Converts from demo to usable product |
| **Phase 3** | WhatsApp/Telegram bot, employer benefits channel | Distribution at scale |
| **Never (V1)** | Feature 10 (social comparison) | Actively harmful to core mission |
