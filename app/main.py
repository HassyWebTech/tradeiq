# ============================================================
# TradeIQ — FastAPI Backend
# ============================================================

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from app.core.persona_engine import build_all_personas, get_dashboard_summary
from app.core.recommender import generate_all_recommendations

app = FastAPI(
    title="TradeIQ API",
    description="AI-powered customer intelligence for African SMBs",
    version="1.0.0"
)

# --- Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Temporary storage for uploaded file
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Welcome to TradeIQ — Know Your Customer"}


@app.post("/upload")
async def upload_customers(file: UploadFile = File(...)):
    """
    Accept a CSV file upload from the business owner.
    Saves it temporarily and returns a session file path.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    filepath = f"{UPLOAD_DIR}/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully", "filepath": filepath}


@app.get("/dashboard")
def get_dashboard(filepath: str):
    """
    Returns dashboard summary — total customers,
    active, at risk, high risk, lost, top customer.
    """
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found. Please upload first.")

    personas = build_all_personas(filepath)
    summary = get_dashboard_summary(personas)
    return summary


@app.get("/personas")
def get_personas(filepath: str):
    """
    Returns full persona list for all customers.
    """
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found. Please upload first.")

    personas = build_all_personas(filepath)
    return {"customers": personas}


@app.get("/recommendations")
def get_recommendations(filepath: str):
    """
    Returns AI-generated re-engagement messages
    for all at-risk customers.
    """
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found. Please upload first.")

    personas = build_all_personas(filepath)
    recommendations = generate_all_recommendations(personas)
    return {"recommendations": recommendations}