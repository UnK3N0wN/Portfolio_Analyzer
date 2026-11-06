"""
ai/llm.py
Optimized LLM integration using Groq API with Llama models.
Token-efficient + production-ready version.
"""

import os
import re
from django.conf import settings

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# ── Models ────────────────────────────────────────────────────────────────
FAST_MODEL = "openai/gpt-oss-20b"
SMART_MODEL = "openai/gpt-oss-120b"


# ── Optimized System Prompt (SHORT = LESS TOKENS) ─────────────────────────
SYSTEM_PROMPT = """You are PortfolioAI. Give concise financial insights.
Instructions:
- Use plain text only (NO Markdown like **, ##, or #).
- Use simple dashes (-) for lists.
- Use ALL CAPS for headers and stock tickers.
- Max 3 bullet points per section.
Required Footer: Invest at your own risk. Past performance != future results."""


# ── Groq Client ───────────────────────────────────────────────────────────
def get_groq_client():
    api_key = getattr(settings, 'GROQ_API_KEY', '') or os.getenv('GROQ_API_KEY', '')
    if not api_key or not GROQ_AVAILABLE:
        return None
    return Groq(api_key=api_key)


# ── Optional: Compress Portfolio Context ──────────────────────────────────
def compress_portfolio(portfolio_context: str, max_chars: int = 800) -> str:
    """
    Reduce token usage by trimming large portfolio inputs.
    We can later replace this with smarter summarization.
    """
    if not portfolio_context:
        return ""

    if len(portfolio_context) <= max_chars:
        return portfolio_context

    return portfolio_context[:max_chars] + "\n... (truncated)"


def fallback_portfolio_analysis(portfolio_context=""):
    """Provide a useful analysis without requiring an LLM response."""
    if not portfolio_context:
        return "AI analysis is temporarily unavailable. Add a few holdings to see a portfolio summary."

    lines = [line.strip() for line in portfolio_context.splitlines() if line.strip()]
    total_value = None
    total_invested = None
    total_pl = None
    holdings = []

    for line in lines:
        if line.startswith('Total Value:'):
            match = re.search(r'\$([\d,]+\.\d+)', line)
            if match:
                total_value = float(match.group(1).replace(',', ''))
        elif line.startswith('Total Invested:'):
            match = re.search(r'\$([\d,]+\.\d+)', line)
            if match:
                total_invested = float(match.group(1).replace(',', ''))
        elif line.startswith('Total P/L:'):
            match = re.search(r'\$([\d,]+\.\d+)', line)
            if match:
                total_pl = float(match.group(1).replace(',', ''))
        elif line.startswith('- '):
            match = re.match(r'-\s*([A-Z0-9-]+)\s*\(([^)]+)\):\s*(.*)', line)
            if match:
                symbol, name, details = match.groups()
                holdings.append({'symbol': symbol, 'name': name, 'details': details})

    if total_value is None:
        return "AI analysis is temporarily unavailable, but your portfolio data is loaded and ready to re-check."

    leader = ""
    if holdings:
        strongest = max(holdings, key=lambda h: h['symbol'])
        leader = f"Leading position: {strongest['symbol']}."

    if total_pl is not None:
        direction = 'up' if total_pl >= 0 else 'down'
        pl_line = f"Overall performance is {direction} by ${abs(total_pl):,.2f}."
    else:
        pl_line = "Performance is being re-evaluated."

    value_line = f"Portfolio value is ${total_value:,.2f}."
    invested_line = f"Capital deployed is ${total_invested:,.2f} if known."
    if total_invested is not None:
        invested_line = f"Capital deployed is ${total_invested:,.2f}."

    return (
        "AI analysis is temporarily unavailable, so here is the live portfolio summary:\n"
        f"- {value_line}\n"
        f"- {pl_line}\n"
        f"- {invested_line}\n"
        f"- {leader or 'Portfolio diversification is being assessed.'}\n"
        "- Review your top holdings and rebalance toward your strongest positions."
    )


# ── Core LLM Call ─────────────────────────────────────────────────────────
def ask_llm(user_message, portfolio_context="", model=FAST_MODEL):
    """
    Send message to Groq LLM with optimized token usage.
    """

    client = get_groq_client()

    if not client:
        return fallback_portfolio_analysis(portfolio_context)

    # Compress portfolio to save tokens
    portfolio_context = compress_portfolio(portfolio_context)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add portfolio context ONLY if exists
    if portfolio_context:
        messages.append({
            "role": "user",
            "content": f"Portfolio summary:\n{portfolio_context}"
        })

    # Add actual user query
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=400,
            temperature=0.7,
        )

        content = response.choices[0].message.content
        if content is None or not str(content).strip():
            return fallback_portfolio_analysis(portfolio_context)
        return str(content)

    except Exception:
        return fallback_portfolio_analysis(portfolio_context)


# ── Preset Analysis Functions (SMART MODEL) ───────────────────────────────
def analyze_portfolio(portfolio_context):
    return ask_llm(
        "Analyze my portfolio: performance, diversification, top & worst assets, and give 3 actions.",
        portfolio_context,
        model=SMART_MODEL
    )


def get_risk_assessment(portfolio_context):
    return ask_llm(
        "Assess portfolio risk: concentration, diversification, volatility, and mitigation steps.",
        portfolio_context,
        model=SMART_MODEL
    )


def get_buy_sell_suggestions(portfolio_context):
    return ask_llm(
        "Give buy/sell suggestions based on performance, diversification gaps, and trends.",
        portfolio_context,
        model=SMART_MODEL
    )


# ── Optional: Token Estimator (Rough) ─────────────────────────────────────
def estimate_tokens(text: str) -> int:
    """
    Rough token estimator: 1 token ≈ 4 characters
    """
    if not text:
        return 0
    return len(text) // 4