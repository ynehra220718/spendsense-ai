"""
Orchestrator — sequences all agents and returns the unified recommendation.

Flow:
  1. Load user profile and product data
  2. Run Financial Health Agent
  3. Run Product Intelligence Agent  (parallel-safe with step 2, kept sequential for clarity)
  4. Run Behavioral Coach Agent      (needs outputs from 2 + 3)
  5. Run Deal Hunter Agent           (needs outputs from 2 + 3; skips if health score >= 60)
  6. Run Orchestrator synthesis      (needs all agent outputs)
  7. Return complete recommendation object
"""

import json
import time
from pathlib import Path

from agents.base import client, DEFAULT_MODEL
from agents.financial_health_agent import run_financial_health_agent
from agents.product_intelligence_agent import run_product_intelligence_agent
from agents.behavioral_coach_agent import run_behavioral_coach_agent
from agents.deal_hunter_agent import run_deal_hunter_agent
from tools.price_source import get_product_from_url, get_product_by_id
from tools.user_tools import load_user_profile

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def run(
    user_id: str,
    product_url: str = None,
    product_id: str = None,
    purchase_amount: float = None,
) -> dict:
    """
    Main entry point for a purchase evaluation.

    Args:
        user_id:         ID of the user profile to load (e.g., "priya")
        product_url:     Full product URL (auto-detects platform, preferred)
        product_id:      Mock catalog ID (fallback if no URL)
        purchase_amount: Override price (optional; uses product current_price if not set)

    Returns:
        Complete recommendation dict with all agent outputs + synthesis.
    """
    start_time = time.time()

    # --- 1. Load user profile ---
    user_profile = load_user_profile(user_id)
    if not user_profile:
        raise ValueError(f"User profile '{user_id}' not found.")

    # --- 2. Load product data (auto-routes by platform) ---
    if product_url:
        product = get_product_from_url(product_url)
    elif product_id:
        product = get_product_by_id(product_id)
    else:
        raise ValueError("Provide either product_url or product_id.")

    if not product:
        raise ValueError("Product not found in catalog or URL could not be resolved.")

    amount = purchase_amount or product.get("current_price", 0)

    # --- 3. Financial Health Agent ---
    financial_result = run_financial_health_agent(user_profile, amount)

    # --- 4. Product Intelligence Agent ---
    product_result = run_product_intelligence_agent(product)

    # --- 5. Behavioral Coach Agent ---
    coach_result = run_behavioral_coach_agent(
        user_profile, product, financial_result, product_result
    )

    # --- 6. Deal Hunter Agent (conditional) ---
    deal_result = run_deal_hunter_agent(
        user_profile, product, financial_result, product_result
    )

    # --- 7. Orchestrator synthesis ---
    synthesis_message = f"""
Synthesize these four agent outputs into a final unified recommendation.

Financial Health Agent:
{json.dumps(financial_result, indent=2)}

Product Intelligence Agent:
{json.dumps(product_result, indent=2)}

Behavioral Coach Agent:
{json.dumps(coach_result, indent=2)}

Deal Hunter Agent:
{json.dumps(deal_result, indent=2)}

Return exactly the JSON schema specified. No markdown, no explanation.
"""

    synthesis_response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=512,
        messages=[
            {"role": "system", "content": load_prompt("orchestrator_prompt.md")},
            {"role": "user", "content": synthesis_message},
        ],
    )
    synthesis = json.loads(synthesis_response.choices[0].message.content)

    elapsed = round(time.time() - start_time, 2)

    return {
        "user": user_profile.get("name"),
        "product": product.get("name"),
        "amount": amount,
        "platform": product.get("_platform", "mock"),
        "data_source": product.get("_source", "mock"),
        "elapsed_seconds": elapsed,
        "financial": financial_result,
        "product": product_result,
        "coach": coach_result,
        "deals": deal_result,
        "synthesis": synthesis,
    }
