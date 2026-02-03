"""Main FastAPI application entry point"""
from fastapi import FastAPI

app = FastAPI(
    title="Terminal-V Core API",
    description="Core API service for Terminal-V financial platform",
    version="0.1.0"
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "core-api"}
