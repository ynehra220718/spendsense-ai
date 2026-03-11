import json
from pathlib import Path
from agents.base import client, DEFAULT_MODEL

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def run_financial_health_agent(user_profile: dict, purchase_amount: float) -> dict:
    """Evaluates user's financial health relative to a purchase amount."""
    monthly_income = user_profile.get("monthly_income", 0)
    monthly_expenses = user_profile.get("monthly_expenses", 0)
    savings = user_profile.get("savings", 0)
    total_debt = user_profile.get("total_debt", 0)
    monthly_surplus = monthly_income - monthly_expenses
    purchase_pct = (purchase_amount / monthly_income * 100) if monthly_income > 0 else 100

    user_message = f"""
Evaluate this purchase decision:

User Profile:
- Name: {user_profile.get("name", "User")}
- Monthly Income: ${monthly_income:,.0f}
- Monthly Expenses: ${monthly_expenses:,.0f}
- Monthly Surplus: ${monthly_surplus:,.0f}
- Current Savings: ${savings:,.0f}
- Total Debt: ${total_debt:,.0f}
- Financial Goals: {user_profile.get("financial_goals", [])}

Purchase:
- Amount: ${purchase_amount:,.2f}
- Purchase as % of monthly income: {purchase_pct:.1f}%

Return exactly the JSON schema specified. No markdown, no explanation.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": load_prompt("financial_health_prompt.md")},
            {"role": "user", "content": user_message},
        ],
    )
    return json.loads(response.choices[0].message.content)
