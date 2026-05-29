# ============================================================
# TradeIQ — Test Recommender
# ============================================================

from app.core.persona_engine import build_all_personas, get_dashboard_summary
from app.core.recommender import generate_all_recommendations

# --- Build personas
filepath = "data/sample_customers.csv"
personas = build_all_personas(filepath)

# --- Dashboard summary
summary = get_dashboard_summary(personas)
print("=" * 50)
print("TRADEIQ DASHBOARD SUMMARY")
print("=" * 50)
print(f"Total Customers : {summary['total_customers']}")
print(f"Active          : {summary['active']}")
print(f"At Risk         : {summary['at_risk']}")
print(f"High Risk       : {summary['high_risk']}")
print(f"Lost            : {summary['lost']}")
print(f"Total Revenue   : ₦{summary['total_revenue']:,.2f}")
print(f"Top Customer    : {summary['top_customer']}")

# --- Generate re-engagement messages
print("\n" + "=" * 50)
print("RE-ENGAGEMENT RECOMMENDATIONS")
print("=" * 50)

recommendations = generate_all_recommendations(personas)

for rec in recommendations:
    print(f"\n⚠️  {rec['customer_name']} — {rec['churn_risk']} ({rec['value_segment']})")
    print(f"📱 Message: {rec['message']}")