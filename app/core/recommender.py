# ============================================================
# TradeIQ — Re-engagement Recommender
# Uses Groq LLM to generate personalised customer messages
# ============================================================

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_reengagement_message(persona: dict) -> str:
    """
    Takes a customer persona and generates a personalised
    re-engagement message the business owner should send.
    """

    prompt = f"""
You are a smart sales assistant for a small African business owner.
Your job is to write a short, warm, and personalised WhatsApp message 
to re-engage a customer based on their profile.

Customer Profile:
- Name: {persona['customer_name']}
- Days since last purchase: {persona['days_since_purchase']} days
- Favourite product: {persona['favourite_product']}
- Products they buy: {', '.join(persona['products_bought'])}
- Total spent with us: ₦{persona['total_spend']:,.2f}
- Number of orders: {persona['purchase_count']}
- Churn risk: {persona['churn_risk']}
- Customer segment: {persona['value_segment']}

Instructions:
- Write ONLY the WhatsApp message, nothing else
- Keep it under 50 words
- Sound warm, human, and personal — not like a robot
- Mention their favourite product naturally
- If they are VIP, make them feel special
- If they are At Risk or Lost, create a gentle sense of urgency
- Write in a Nigerian friendly tone
- Do not use hashtags or emojis overload — maximum 2 emojis
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def generate_all_recommendations(personas: list) -> list:
    """
    Generate re-engagement messages for all at-risk customers.
    Skips active customers — they don't need re-engagement yet.
    """
    results = []

    for persona in personas:
        if persona["churn_risk"] in ["At Risk", "High Risk", "Lost"]:
            message = generate_reengagement_message(persona)
            results.append({
                "customer_name" : persona["customer_name"],
                "churn_risk"    : persona["churn_risk"],
                "value_segment" : persona["value_segment"],
                "message"       : message,
            })

    return results