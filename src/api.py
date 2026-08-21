from fastapi import FastAPI
from pydantic import BaseModel

from src.classifier import classify_log


app = FastAPI(
    title="AI Log Analyzer",
    version="1.0.0"
)


class LogRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze_log(request: LogRequest):

    result = classify_log(request.message)

    return result