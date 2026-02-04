"""Main FastAPI application entry point"""
from core_api.api import app

# Import app from api.py which contains all endpoints
__all__ = ["app"]
