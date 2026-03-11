# SpendSense AI

> **"Before you click Buy Now, SpendSense tells you if you should."**

A multi-agent AI copilot that evaluates e-commerce purchase decisions in real time using personal financial data, price history intelligence, and behavioral coaching grounded in consumer psychology.

---

## Why This Exists

| Existing Tool | What It Does | What It Misses |
|---|---|---|
| Mint / YNAB | Tracks spending *after* the fact | No real-time purchase intercept |
| Honey / Rakuten | Finds coupons at checkout | Ignores personal financial health |
| Affirm / Klarna | Enables installment payments | Actively encourages overspending |
| **SpendSense AI** | Intercepts the decision moment with financial context + AI coaching | **This is the gap** |

---

## Agent Architecture

```
User Input (product URL or catalog item + price)
                    │
            [Orchestrator]
           loads profile, sequences agents
                    │
        ┌───────────┴───────────┐
        │                       │
[Financial Health      [Product Intelligence
     Agent]                  Agent]
  health score 0-100      price history analysis
  verdict + rationale      sensible lowest price
        │                       │
        └───────────┬───────────┘
                    │
         [Behavioral Coach Agent]
         persona-tailored coaching
         bias detection + framing
                    │
            (if health score < 60)
                    │
          [Deal Hunter Agent]
          3 alternatives: best price
          / wait / creative
                    │
            [Orchestrator]
         synthesizes final verdict
                    │
            Streamlit UI
```

| Agent | Role | Output |
|---|---|---|
| **Orchestrator** | Sequences all agents, synthesizes result | Unified recommendation object |
| **Financial Health** | Evaluates affordability against real financial profile | Health score (0–100), verdict, opportunity cost |
| **Product Intelligence** | Analyses price history, filters anomalies, finds sensible low | Price assessment, sensible lowest price, value score |
| **Behavioral Coach** | Delivers persona-tailored coaching using behavioral economics | 2–4 sentence coaching message, bias detected |
| **Deal Hunter** | Finds 3 alternatives when health score < 60 | Best price / wait / creative alternatives |

---

## Platform Auto-Detection

Paste any product URL — SpendSense auto-detects the platform and routes to the right data source:

| Platform | Data Source | Status |
|---|---|---|
| Amazon (all regions) | CamelCamelCamel free API (if key set) → mock fallback | ✅ Live or mock |
| Flipkart | Mock data (no free API exists) | ✅ Mock |
| Myntra, Meesho, Snapdeal | Mock data | ✅ Mock |
| Unknown URL | Mock data | ✅ Mock |

No configuration needed — detection is automatic from the URL domain.

---

## Price History Intelligence

SpendSense filters price history to find the **sensible lowest price** — not a 1-day pricing error:

- Excludes prices lasting fewer than 3 consecutive days
- Excludes prices more than 40% below the median (glitches, errors)
- Explains any excluded anomaly transparently
- Shows the date of the sensible lowest price so you know when to expect it again

---

## Demo Personas (Research-Backed)

All three personas are built from real 2024–2025 financial research data (Experian, Empower, Bankrate, Deloitte, LifeStance, Federal Reserve SHED):

| Persona | Profile | Core Need |
|---|---|---|
| **Priya**, 28 | $95K engineer, $36K debt, budget guilt | Clear go/no-go with honest rationale |
| **Marcus**, 34 | $72K ops manager, $4K hidden BNPL debt | Data-driven alternative analysis |
| **Destiny**, 25 | $48K nonprofit, rebuilding finances | Non-judgmental coaching that builds literacy |

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/your-username/spendsense-ai
cd spendsense-ai
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

Get a free OpenRouter API key at [openrouter.ai](https://openrouter.ai).
Optional: Get a free CamelCamelCamel API key at [camelcamelcamel.com/api](https://camelcamelcamel.com/api) for live Amazon price history.

### 3. Run the app

```bash
streamlit run ui/app.py
```

### 4. Quick agent test (no UI)

```python
from agents.orchestrator import run
result = run(user_id="priya", product_id="instant-pot-duo-7in1", purchase_amount=279.99)
print(result["synthesis"]["one_line_verdict"])
print(result["coach"]["coaching_message"])
```

### 5. Run tests

```bash
python -m pytest tests/ -v
```

---

## File Structure

```
spendsense-ai/
├── agents/
│   ├── base.py                        # Shared OpenRouter client
│   ├── orchestrator.py                # Sequences all agents
│   ├── financial_health_agent.py
│   ├── product_intelligence_agent.py
│   ├── behavioral_coach_agent.py
│   └── deal_hunter_agent.py
├── prompts/                           # System prompts as .md files
│   ├── financial_health_prompt.md
│   ├── product_intelligence_prompt.md
│   ├── behavioral_coach_prompt.md
│   ├── deal_hunter_prompt.md
│   └── orchestrator_prompt.md
├── tools/
│   ├── price_source.py                # Platform auto-detection + data routing
│   └── user_tools.py                  # Profile loader
├── data/
│   ├── mock_user_profiles/            # priya.json, marcus.json, destiny.json
│   └── mock_product_catalog.json      # 3 products with price history
├── ui/
│   ├── app.py                         # Streamlit entry point
│   ├── pages/
│   │   ├── 01_onboarding.py
│   │   ├── 02_purchase_check.py
│   │   └── 03_history.py
│   └── components/
│       ├── recommendation_card.py
│       └── financial_health_gauge.py
├── pm_artifacts/                      # Full PM documentation
│   ├── PRD.md
│   ├── roadmap.md
│   ├── user_personas.md
│   ├── RICE_prioritization.md
│   ├── OKRs_and_KPIs.md
│   └── GTM_strategy.md
├── tests/
│   ├── test_financial_health_agent.py
│   ├── test_product_intelligence_agent.py
│   └── test_price_source.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Switching AI Models

Change the model in `.env` — zero code changes required:

```bash
DEFAULT_MODEL=anthropic/claude-sonnet-4-6   # Default — best reasoning
DEFAULT_MODEL=openai/gpt-4o                 # Compare outputs
DEFAULT_MODEL=google/gemini-flash-1.5       # Fast + cheap for testing
DEFAULT_MODEL=mistralai/mistral-7b-instruct # Free tier testing
```

---

## PM Artifacts

Full product management documentation is in `/pm_artifacts/`:

- **PRD** — Problem statement, 15 user stories, functional requirements per agent, non-functional requirements, success metrics
- **Roadmap** — 3-phase roadmap with explicit gate conditions between phases
- **User Personas** — Research-backed persona sheets for Priya, Marcus, Destiny with real financial data
- **RICE Prioritization** — 10 features scored; social comparison explicitly deprioritized with behavioral economics rationale
- **OKRs & KPIs** — North Star metric (Purchase Decision Quality Score), OKRs by phase, anti-metrics
- **GTM Strategy** — Beachhead market, channel strategy, pricing tiers, risk register

---

## Design Decisions

**Why multi-agent vs. single prompt?**
Each agent has a separate system prompt, separate context, and a specific job. The Financial Health Agent doesn't know about behavioral economics — it just scores affordability. The Behavioral Coach Agent doesn't see the raw financial numbers — it sees the verdicts and reasons. This separation produces more coherent, less hallucinated output than asking one model to do everything.

**Why mock data for the demo?**
Neither Amazon nor Flipkart have free public price history APIs. CamelCamelCamel provides free Amazon price history (API key required). All other platforms use mock data. For a portfolio demo, mock data is the right choice: zero cost, full control over demo scenarios, no legal risk.

**Why Streamlit and not a Chrome extension?**
Extensions require JavaScript (a new language on top of Python). A Streamlit web app is 100% sufficient to demonstrate the agent logic in a portfolio interview. The agent architecture is UI-agnostic — switching to an extension changes only the UI layer.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| AI | OpenRouter API (model-agnostic — swap Claude/GPT-4o/Gemini in `.env`) |
| Frontend | Streamlit |
| Data | Local JSON (mock), CamelCamelCamel API (optional, free) |
| Config | python-dotenv |
| Hosting | Streamlit Cloud (free) |

---

*Portfolio project — Deloitte USI analyst (data migration, Oracle → Snowflake, Corebridge Financial) transitioning to PM.*
*Built to demonstrate PM rigor (artifacts), technical depth (multi-agent AI), and product thinking (behavioral economics foundation).*
