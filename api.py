from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Questions JSON
with open("finalquestions_100.json", "r", encoding="utf-8") as file:
    questions = json.load(file)


# HOME API
@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }


# QUESTIONS API
@app.get("/questions")
def get_questions(
    difficulty: str = None,
    topic: str = None
):

    filtered = questions.copy()

    # Difficulty Filter
    if difficulty:

        filtered = [
            q for q in filtered
            if q.get("Difficulty", "").lower().strip()
            == difficulty.lower().strip()
        ]

    # Topic Filter
    if topic:

        filtered = [
            q for q in filtered
            if topic.lower().strip()
            in q.get("Topics", "").lower()
        ]

    return filtered


# GET OPTIMIZED SOLUTION API
@app.get("/get-solution")
def get_solution(
    title: str,
    language: str
):

    # JSON files for each language
    solution_files = {

        "python": "solutions/py_solutions.json",

        "java": "solutions/java_solutions.json",

        "cpp": "solutions/cpp_solutions.json",

        "javascript": "solutions/js_solutions.json",

        "c": "solutions/c_solutions.json"
    }

    language = language.lower()

    # Check language
    if language not in solution_files:

        return {
            "message": "Unsupported language"
        }

    # Load selected language JSON
    with open(
        solution_files[language],
        "r",
        encoding="utf-8"
    ) as file:

        solutions = json.load(file)

    # Search matching question
    for item in solutions:

       # Search matching question
for item in solutions:
    db_title = (
        item["title"]
        .lower()
        .replace("-", "")
        .replace(" ", "")
        .strip()
    )

    search_title = (
        title
        .lower()
        .replace("-", "")
        .replace(" ", "")
        .strip()
    )

    if db_title == search_title:

        return {

            "question": item["title"],

            "language": language,

            "time_complexity": item.get("time_complexity"),

            "space_complexity": item.get("space_complexity"),

            "optimized_code": item.get("solution")
        }

    return {
        "message": "Solution not found"
    }
