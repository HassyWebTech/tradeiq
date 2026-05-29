# ============================================================
# TradeIQ — Persona Engine
# Builds a behavioral profile for each customer
# ============================================================

import pandas as pd
import numpy as np
from datetime import datetime, date

def load_customers(filepath: str) -> pd.DataFrame:
    """
    Load customer CSV and clean it up.
    """
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"])
    df["total_spend"] = pd.to_numeric(df["total_spend"], errors="coerce").fillna(0)
    df["purchase_count"] = pd.to_numeric(df["purchase_count"], errors="coerce").fillna(0)
    df["purchase_frequency_days"] = pd.to_numeric(df["purchase_frequency_days"], errors="coerce").fillna(30)
    return df


def calculate_days_since_purchase(last_purchase_date) -> int:
    """
    How many days since this customer last bought something.
    """
    today = pd.Timestamp(datetime.today().date())
    return (today - last_purchase_date).days


def calculate_churn_risk(days_since_purchase: int, frequency: int) -> str:
    """
    Determine churn risk based on how overdue the customer is.
    
    Logic:
    - If days since purchase < frequency → Active
    - If days since purchase is 1x-2x their frequency → At Risk  
    - If days since purchase is 2x+ their frequency → High Risk
    - If days since purchase is 3x+ their frequency → Lost
    """
    ratio = days_since_purchase / max(frequency, 1)
    
    if ratio < 1.0:
        return "Active"
    elif ratio < 2.0:
        return "At Risk"
    elif ratio < 3.0:
        return "High Risk"
    else:
        return "Lost"


def calculate_customer_value(total_spend: float, purchase_count: int) -> str:
    """
    Segment customer by value.
    """
    if total_spend >= 100000 or purchase_count >= 20:
        return "VIP"
    elif total_spend >= 30000 or purchase_count >= 10:
        return "Regular"
    else:
        return "Occasional"


def build_persona(row: pd.Series) -> dict:
    """
    Build a complete persona for a single customer.
    """
    days_since = calculate_days_since_purchase(row["last_purchase_date"])
    churn_risk = calculate_churn_risk(days_since, row["purchase_frequency_days"])
    value_segment = calculate_customer_value(row["total_spend"], row["purchase_count"])
    
    # Parse products into a list
    products = [p.strip() for p in str(row.get("products_bought", "")).split(",")]
    
    persona = {
        "customer_name"        : row["customer_name"],
        "phone"                : row.get("phone", ""),
        "days_since_purchase"  : days_since,
        "purchase_count"       : int(row["purchase_count"]),
        "total_spend"          : float(row["total_spend"]),
        "avg_spend_per_order"  : round(float(row["total_spend"]) / max(int(row["purchase_count"]), 1), 2),
        "purchase_frequency"   : int(row["purchase_frequency_days"]),
        "products_bought"      : products,
        "favourite_product"    : products[0] if products else "Unknown",
        "churn_risk"           : churn_risk,
        "value_segment"        : value_segment,
        "last_purchase_date"   : str(row["last_purchase_date"].date()),
    }
    
    return persona


def build_all_personas(filepath: str) -> list:
    """
    Load CSV and build personas for all customers.
    """
    df = load_customers(filepath)
    personas = [build_persona(row) for _, row in df.iterrows()]
    return personas


def get_dashboard_summary(personas: list) -> dict:
    """
    Generate summary stats for the dashboard.
    """
    total = len(personas)
    active = sum(1 for p in personas if p["churn_risk"] == "Active")
    at_risk = sum(1 for p in personas if p["churn_risk"] == "At Risk")
    high_risk = sum(1 for p in personas if p["churn_risk"] == "High Risk")
    lost = sum(1 for p in personas if p["churn_risk"] == "Lost")
    
    total_revenue = sum(p["total_spend"] for p in personas)
    top_customer = max(personas, key=lambda x: x["total_spend"])
    
    return {
        "total_customers"  : total,
        "active"           : active,
        "at_risk"          : at_risk,
        "high_risk"        : high_risk,
        "lost"             : lost,
        "total_revenue"    : round(total_revenue, 2),
        "top_customer"     : top_customer["customer_name"],
        "top_customer_spend": top_customer["total_spend"],
    }