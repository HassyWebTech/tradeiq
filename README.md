# TradeIQ — AI-Powered Customer Intelligence for African SMBs

> *Know your customer. Before they know what they want.*

TradeIQ is a full-stack AI application that transforms raw customer transaction data into actionable behavioral intelligence. It builds deep customer personas, detects churn risk, and generates personalised re-engagement messages — purpose-built for small and medium businesses across Africa.

---

## Problem

Small businesses across Africa — fashion vendors, food sellers, salon owners, online shops — process hundreds of customer transactions but have zero intelligence about who their customers are, why they return, or why they leave silently. Enterprise CRM tools like Salesforce and HubSpot are too expensive and too complex. The gap between "nothing" and "enterprise software" is wide open.

TradeIQ fills that gap.

---

## Features

- **Persona Engine** — builds a structured behavioral profile per customer from raw CSV data
- **Churn Risk Detection** — classifies each customer as Active, At Risk, High Risk, or Lost based on their individual purchase frequency pattern
- **LLM Re-engagement Recommender** — generates personalised WhatsApp messages for at-risk customers using Groq (Llama 3.3 70B)
- **REST API** — clean FastAPI backend with 5 endpoints and auto-generated OpenAPI docs
- **React Dashboard** — professional frontend with customer health chart, revenue summary, customer table, and recommendations view

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| LLM | Groq API — Llama 3.3 70B |
| Data Processing | Pandas |
| ML | Scikit-learn |
| Auth | JWT + bcrypt |
| Database | SQLite (local) / PostgreSQL (production) |
| Frontend | React |
| Charts | Recharts |
| Backend Deploy | Render |
| Frontend Deploy | Vercel |

---

## Architecture

```
Customer CSV Upload
        ↓
FastAPI Backend (Render)
        ↓
Persona Engine → builds behavioral profile per customer
        ↓
Churn Detector → classifies risk based on purchase frequency ratio
        ↓
Groq LLM → generates personalised re-engagement message
        ↓
React Frontend (Vercel) → renders dashboard, table, recommendations
```

---

## Project Structure

```
tradeiq/
├── app/
│   ├── core/
│   │   ├── persona_engine.py     # Persona builder + churn logic
│   │   └── recommender.py        # Groq LLM re-engagement generator
│   ├── api/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── main.py                   # FastAPI app + all endpoints
├── data/
│   └── sample_customers.csv      # Sample Nigerian SMB customer data
├── .env.example
├── Procfile
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/upload` | Upload customer CSV |
| GET | `/dashboard` | Returns summary stats |
| GET | `/personas` | Returns all customer personas |
| GET | `/recommendations` | Returns LLM-generated re-engagement messages |

Full interactive docs available at `/docs` (Swagger UI).

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API key — free at [console.groq.com](https://console.groq.com)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/HassyWebTech/tradeiq.git
cd tradeiq

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Start the server
uvicorn app.main:app --reload
```

API will be running at `http://127.0.0.1:8000`
Interactive docs at `http://127.0.0.1:8000/docs`

### Frontend Setup

```bash
# Clone frontend repo
git clone https://github.com/HassyWebTech/tradeiq-frontend.git
cd tradeiq-frontend

# Install dependencies
npm install

# Start dev server
npm start
```

Frontend will be running at `http://localhost:3000`

---

## CSV Format

TradeIQ accepts a CSV file with the following columns:

```
customer_name, phone, last_purchase_date, purchase_count,
total_spend, products_bought, purchase_frequency_days
```

Example row:
```
Amaka Obi,08012345678,2026-05-10,12,45000,"Ankara fabric, Lace material",7
```

A sample file is included at `data/sample_customers.csv`.

---

## Churn Risk Logic

Churn risk is calculated as a ratio of days since last purchase to the customer's individual purchase frequency — not a fixed threshold.

```
ratio = days_since_purchase / purchase_frequency_days

ratio < 1.0   → Active
ratio < 2.0   → At Risk
ratio < 3.0   → High Risk
ratio >= 3.0  → Lost
```

This means a customer who buys every 5 days is flagged sooner than one who buys every 30 days — personalised to their own behaviour pattern.

---

## Live Demo

- **Frontend:** [https://tradeiq-frontend-tau.vercel.app](https://tradeiq-frontend-tau.vercel.app)
- **API:** [https://tradeiq-xlam.onrender.com](https://tradeiq-xlam.onrender.com)
- **API Docs:** [https://tradeiq-xlam.onrender.com/docs](https://tradeiq-xlam.onrender.com/docs)

> Note: The backend is on Render's free tier and may take 30-50 seconds to wake up on first request.

---

## Environment Variables

```
APP_NAME=TradeIQ
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./tradeiq.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
GROQ_API_KEY=your-groq-api-key
```

---

## Roadmap

- [ ] WhatsApp Business API integration — send messages directly from the dashboard
- [ ] Paystack and Flutterwave transaction sync — no CSV upload needed
- [ ] Multi-business support — one account, multiple shop profiles
- [ ] Fine-tuned LLM on Nigerian business communication patterns
- [ ] Mobile app — iOS and Android

---

## Author

**Hassan Yakubu** — AI Engineer
[GitHub](https://github.com/HassyWebTech) · [LinkedIn](https://linkedin.com/in/hassan-yakubu)

---

## License

MIT License — free to use, modify, and distribute.