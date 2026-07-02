from fastapi import FastAPI

from app.config import get_settings

app = FastAPI(title="AI Trading Multi-Agents API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": get_settings().environment}
