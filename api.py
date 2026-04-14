from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load CSV
df = pd.read_csv("data/leetcode_data.csv")

# Clean data
df = df.fillna("")

# Convert all values to string (VERY IMPORTANT FIX)
df = df.astype(str)

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/questions")
def get_questions():
    return df.head(10).to_dict(orient="records")
# Filter by difficulty
@app.get("/questions/{difficulty}")
def get_by_difficulty(difficulty: str):
    filtered = df[df["Difficulty"].str.lower() == difficulty.lower()]
    return filtered.head(50).to_dict(orient="records")
# FILTER BY TOPIC
@app.get("/questions/topic/{topic}")
def get_by_topic(topic: str):
    filtered = df[df["Topics"].str.lower().str.contains(topic.lower())]
    return filtered.head(50).to_dict(orient="records")

# SEARCH BY TITLE
@app.get("/questions/search/{keyword}")
def search_questions(keyword: str):
    filtered = df[df["Title"].str.lower().str.contains(keyword.lower())]
    return filtered.head(50).to_dict(orient="records")

from fastapi import Query

@app.get("/recommend")
def recommend_questions(difficulty: str = Query(None), topic: str = Query(None)):
    filtered = df

    if difficulty:
        filtered = filtered[filtered["Difficulty"].str.lower() == difficulty.lower()]

    if topic:
        filtered = filtered[filtered["Topics"].str.lower().str.contains(topic.lower())]

    return filtered.head(20).to_dict(orient="records")