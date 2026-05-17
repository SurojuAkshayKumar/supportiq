import os
import shutil
from typing import Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai_support_pipeline import (
    add_support_ticket_fields,
    clean_text,
    categorize_ticket,
    detect_sentiment,
    detect_frustration,
    generate_suggested_response,
    extract_top_issues
)

app = FastAPI(
    title="SupportIQ Backend API",
    description="Backend API for AI-Powered Customer Support Insight Platform",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RAW_FILE = "uploaded_tickets.csv"
PROCESSED_FILE = "processed_tickets.csv"


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function processes either:
    1. The original spam/ham dataset with label, text, label_num columns
    2. A support-ticket style dataset with a message column
    """

    if {"label", "text", "label_num"}.issubset(set(df.columns)):
        tickets_df = add_support_ticket_fields(df)
    elif "message" in df.columns:
        tickets_df = df.copy()

        if "ticket_id" not in tickets_df.columns:
            tickets_df["ticket_id"] = [f"TKT{i+1:05d}" for i in range(len(tickets_df))]

        if "order_value" not in tickets_df.columns:
            tickets_df["order_value"] = 0

        if "original_email_label" not in tickets_df.columns:
            tickets_df["original_email_label"] = "ham"

    else:
        raise ValueError(
            "CSV must contain either label/text/label_num columns or a message column."
        )

    clean_messages = []
    predicted_categories = []
    sentiments = []
    sentiment_scores = []
    frustration_levels = []
    suggested_responses = []

    for _, row in tickets_df.iterrows():
        message = row.get("message", "")

        original_label = row.get("original_email_label", "ham")

        clean_msg = clean_text(message)
        category = categorize_ticket(message, original_label)
        sentiment, score = detect_sentiment(message)
        frustration = detect_frustration(message, score)
        response = generate_suggested_response(category)

        clean_messages.append(clean_msg)
        predicted_categories.append(category)
        sentiments.append(sentiment)
        sentiment_scores.append(score)
        frustration_levels.append(frustration)
        suggested_responses.append(response)

    tickets_df["clean_message"] = clean_messages
    tickets_df["predicted_category"] = predicted_categories
    tickets_df["sentiment"] = sentiments
    tickets_df["sentiment_score"] = sentiment_scores
    tickets_df["frustration_level"] = frustration_levels
    tickets_df["suggested_response"] = suggested_responses

    return tickets_df


@app.get("/")
def home():
    return {
        "message": "SupportIQ Backend API is running",
        "available_endpoints": [
            "/health",
            "/upload",
            "/process",
            "/insights",
            "/tickets",
            "/suggest-response"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
def upload_tickets(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    with open(RAW_FILE, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "saved_as": RAW_FILE
    }


@app.post("/process")
def process_tickets():
    if not os.path.exists(RAW_FILE):
        if os.path.exists("spam_ham_dataset.csv"):
            input_file = "spam_ham_dataset.csv"
        else:
            raise HTTPException(
                status_code=404,
                detail="No uploaded file found. Upload a CSV first."
            )
    else:
        input_file = RAW_FILE

    try:
        df = pd.read_csv(input_file)
        processed_df = process_dataframe(df)
        processed_df.to_csv(PROCESSED_FILE, index=False)

        return {
            "message": "Tickets processed successfully",
            "rows_processed": len(processed_df),
            "output_file": PROCESSED_FILE
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/insights")
def get_insights():
    if not os.path.exists(PROCESSED_FILE):
        raise HTTPException(
            status_code=404,
            detail="processed_tickets.csv not found. Run /process first."
        )

    df = pd.read_csv(PROCESSED_FILE)

    total_tickets = len(df)

    total_revenue = float(df["order_value"].sum()) if "order_value" in df.columns else 0

    top_issues = (
        df["predicted_category"]
        .value_counts()
        .reset_index()
    )
    top_issues.columns = ["category", "count"]

    sentiment_summary = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )
    sentiment_summary.columns = ["sentiment", "count"]

    frustration_summary = (
        df["frustration_level"]
        .value_counts()
        .reset_index()
    )
    frustration_summary.columns = ["frustration_level", "count"]

    revenue_impact = (
        df.groupby("predicted_category")["order_value"]
        .sum()
        .reset_index()
        .sort_values("order_value", ascending=False)
    )
    revenue_impact.columns = ["category", "revenue_impact"]

    top_keywords = extract_top_issues(df["message"], top_n=15)

    return {
        "total_tickets": total_tickets,
        "total_revenue_impact": total_revenue,
        "top_issues": top_issues.to_dict(orient="records"),
        "sentiment_summary": sentiment_summary.to_dict(orient="records"),
        "frustration_summary": frustration_summary.to_dict(orient="records"),
        "revenue_impact": revenue_impact.to_dict(orient="records"),
        "top_recurring_keywords": [
            {"keyword": word, "count": count} for word, count in top_keywords
        ]
    }


@app.get("/tickets")
def get_tickets(
    limit: int = 100,
    category: Optional[str] = None
):
    if not os.path.exists(PROCESSED_FILE):
        raise HTTPException(
            status_code=404,
            detail="processed_tickets.csv not found. Run /process first."
        )

    df = pd.read_csv(PROCESSED_FILE)

    if category and category != "All":
        df = df[df["predicted_category"] == category]

    output_columns = [
        "ticket_id",
        "timestamp",
        "channel",
        "product",
        "customer_country",
        "message",
        "predicted_category",
        "sentiment",
        "frustration_level",
        "resolution_status",
        "order_value",
        "suggested_response"
    ]

    available_columns = [col for col in output_columns if col in df.columns]

    return {
        "tickets": df[available_columns].head(limit).to_dict(orient="records")
    }


@app.post("/suggest-response")
def suggest_response(payload: dict):
    message = payload.get("message", "")

    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    category = categorize_ticket(message, "ham")
    sentiment, score = detect_sentiment(message)
    frustration = detect_frustration(message, score)
    response = generate_suggested_response(category)

    return {
        "message": message,
        "predicted_category": category,
        "sentiment": sentiment,
        "sentiment_score": score,
        "frustration_level": frustration,
        "suggested_response": response
    }