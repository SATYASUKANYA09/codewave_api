from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load dataset (IMPORTANT: use relative path)
df = pd.read_csv("data/leetcode_data.csv")

# Clean data
df = df.fillna("")
df = df.astype(str)

# Home API
@app.get("/")
def home():
    return {"message": "API is running successfully"}

# SINGLE SMART API
@app.get("/questions")
def get_questions(difficulty: str = None, topic: str = None):
    
    filtered = df

    # Filter by difficulty
    if difficulty:
        filtered = filtered[filtered["Difficulty"].str.lower() == difficulty.lower()]

    # Filter by topic
    if topic:
        filtered = filtered[filtered["Topics"].str.lower().str.contains(topic.lower())]

    # Return only 100 records
    return filtered.head(100).to_dict(orient="records")