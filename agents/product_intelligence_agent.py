import json
from pathlib import Path
from agents.base import client, DEFAULT_MODEL

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def run_product_intelligence_agent(product: dict) -> dict:
    """Analyzes product price fairness and pricing history."""
    user_message = f"""
Analyze this product and its pricing history:

Product: {product.get("name")}
Category: {product.get("category")}
Brand: {product.get("brand")}
Current Price: ${product.get("current_price")}

Price History (chronological):
{json.dumps(product.get("price_history", []), indent=2)}

Apply the sensible lowest price rules from your instructions.
Return exactly the JSON schema specified. No markdown, no explanation.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": load_prompt("product_intelligence_prompt.md")},
            {"role": "user", "content": user_message},
        ],
    )
    return json.loads(response.choices[0].message.content)
