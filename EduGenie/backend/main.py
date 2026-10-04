from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="EduGenie API",
    description="AI-powered learning assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

# Allows frontend running with VS Code Live Server
# Example:
# http://127.0.0.1:5500/frontend/index.html

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class TextRequest(BaseModel):
    text: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {
        "success": True,
        "message": "EduGenie backend is running",
        "status": "online"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "success": True,
        "status": "healthy"
    }


# ============================================================
# ASK A QUESTION
# ============================================================

@app.post("/qa")
async def qa(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:

        answer = answer_question(text)

        return {
            "success": True,
            "result": answer
        }

    except Exception as error:

        print("QA ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(error)}"
        )


# ============================================================
# EXPLAIN A TOPIC
# ============================================================

@app.post("/explain")
async def explain(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic."
        )

    try:

        explanation = explain_topic(text)

        return {
            "success": True,
            "result": explanation
        }

    except Exception as error:

        print("EXPLANATION ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Topic explanation failed: {str(error)}"
        )


# ============================================================
# GENERATE QUIZ
# ============================================================

@app.post("/quiz")
async def quiz(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic or passage."
        )

    try:

        quiz_data = generate_quiz(text)

        return {
            "success": True,
            "quiz": quiz_data
        }

    except Exception as error:

        print("QUIZ ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {str(error)}"
        )


# ============================================================
# SUMMARIZE
# ============================================================

@app.post("/summarize")
async def summarize(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter text to summarize."
        )

    try:

        summary = summarize_text(text)

        return {
            "success": True,
            "result": summary
        }

    except Exception as error:

        print("SUMMARY ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(error)}"
        )


# ============================================================
# LEARNING PATH
# ============================================================

@app.post("/learn/recommendations")
async def learning_path(request: TextRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic."
        )

    try:

        recommendations = get_learning_recommendations(text)

        return {
            "success": True,
            "result": recommendations
        }

    except Exception as error:

        print("LEARNING PATH ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Learning path generation failed: {str(error)}"
        )


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():

    print("=" * 60)
    print("EduGenie Backend Started")
    print("API: http://127.0.0.1:8000")
    print("Docs: http://127.0.0.1:8000/docs")
    print("Frontend: http://127.0.0.1:5500")
    print("=" * 60)