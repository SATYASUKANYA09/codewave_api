from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import os
import glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_csv("data/leetcode_data.csv")

# Clean data
df = df.fillna("")
df = df.astype(str)

# Home API
@app.get("/")
def home():
    return {"message": "API is running successfully"}

# Questions API
@app.get("/questions")
def get_questions(difficulty: str = None, topic: str = None):

    filtered = df

    # Filter by difficulty
    if difficulty:
        filtered = filtered[
            filtered["Difficulty"].str.lower() == difficulty.lower()
        ]

    # Filter by topic
    if topic:
        filtered = filtered[
            filtered["Topics"].str.lower().str.contains(topic.lower())
        ]

    # Return only 100 records
    return filtered.head(100).to_dict(orient="records")


# Dynamic Solution API
@app.get("/get-solution")
def get_solution(title: str, language: str):

    # Language folder mapping
    language_folders = {
        "python": "Python",
        "java": "java",
        "c++": "C++",
        "javascript": "JavaScript",
        "c": "c"
    }

    # File extensions
    extensions = {
        "python": "*.py",
        "java": "*.java",
        "c++": "*.cpp",
        "javascript": "*.js",
        "c": "*.c"
    }

    language = language.lower()

    # Check supported language
    if language not in language_folders:
        return {"message": "Unsupported language"}

    folder = language_folders[language]

    extension = extensions[language]

    # Convert title
    search_title = (
    title.lower()
    .replace(" ", "-")
    .replace("(", "")
    .replace(")", "")
    .replace(",", "")
    .replace("'", "")
   )

    # Get all files
    files = glob.glob(f"{folder}/{extension}")

    # Search matching file
    for filepath in files:

        filename = os.path.basename(filepath).lower()

        if search_title in filename:

            with open(filepath, "r", encoding="utf-8") as file:
                code = file.read()

            return {
                "question": title,
                "language": language,
                "file": filename,
                "optimized_code": code
            }

    return {"message": "Solution not found"}


# Python Solutions API
@app.get("/python-solutions")
def python_solutions():

    files = glob.glob("Python/*.py")[:50]

    all_solutions = []

    for filepath in files:

        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        all_solutions.append({
            "file": filename,
            "code": code
        })

    return all_solutions


# Java Solutions API
@app.get("/java-solutions")
def java_solutions():

    files = glob.glob("java/*.java")[:50]

    all_solutions = []

    for filepath in files:

        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        all_solutions.append({
            "file": filename,
            "code": code
        })

    return all_solutions


# C++ Solutions API
@app.get("/cpp-solutions")
def cpp_solutions():

    files = glob.glob("C++/*.cpp")[:50]

    all_solutions = []

    for filepath in files:

        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        all_solutions.append({
            "file": filename,
            "code": code
        })

    return all_solutions


# JavaScript Solutions API
@app.get("/javascript-solutions")
def javascript_solutions():

    files = glob.glob("JavaScript/*.js")[:50]

    all_solutions = []

    for filepath in files:

        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        all_solutions.append({
            "file": filename,
            "code": code
        })

    return all_solutions


# C Solutions API
@app.get("/c-solutions")
def c_solutions():

    files = glob.glob("c/*.c")[:50]

    all_solutions = []

    for filepath in files:

        filename = os.path.basename(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

        all_solutions.append({
            "file": filename,
            "code": code
        })

    return all_solutions