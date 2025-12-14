import pandas as pd
import os
import streamlit as st
from datetime import datetime
from groq import Groq
import json

# --- CONFIGURATION ---
# Attempts to load the API key from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    api_key = "key_missing"

client = Groq(api_key=api_key)
DATA_FILE = "reviews_data.csv"

# --- AI FUNCTIONS ---
def generate_ai_response(user_rating, user_review):
    """
    Generates a professional response for the user based on their review.
    """
    prompt = f"""
    A user just left a {user_rating}-star review: "{user_review}".
    Write a brief, professional response to them on behalf of the company management.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception:
        return "Thank you for your feedback."

def analyze_review_for_admin(user_rating, user_review):
    """
    Generates a summary, action item, and sentiment analysis for the admin dashboard.
    """
    prompt = f"""
    Analyze the following customer review:
    Rating: {user_rating}/5
    Review: "{user_review}"

    Return a JSON object with the following keys:
    1. "summary": A concise 5-word summary of the review content.
    2. "action": A recommended business action based on this feedback.
    3. "sentiment": One word only ("Positive", "Neutral", or "Negative").
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {"summary": "Processing Error", "action": "Manual review required", "sentiment": "Neutral"}

# --- DATA FUNCTIONS ---
def load_data():
    """Loads the CSV data file or creates a new one if it does not exist."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Rating", "Review", "AI_Response", "Summary", "Action", "Sentiment"])

def save_review(rating, review, ai_response, analysis):
    """Appends a new review to the CSV data file."""
    df = load_data()
    new_data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Rating": rating,
        "Review": review,
        "AI_Response": ai_response,
        "Summary": analysis.get("summary", "N/A"),
        "Action": analysis.get("action", "N/A"),
        "Sentiment": analysis.get("sentiment", "Neutral")
    }
    # Using pd.concat to append the new row
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
