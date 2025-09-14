# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.db.models import Candidate, Job
from backend.app.api import job_routes  # Import the router modules
from app.db_clients.mongo_client import init_mongo
from backend.app.api import candidate_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    try:
        await init_mongo()
        yield
    except Exception as e:
        raise


app = FastAPI(
    title="Hire Caliber",
    description="An API for screening resumes against job descriptions using AI.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Include Routers ---
# This is the key part. The app object now incorporates all endpoints
# from the router files, automatically handling the prefixes we defined.
app.include_router(candidate_routes.router, prefix="/api")
app.include_router(job_routes.router, prefix="/api")


# --- Root Endpoint ---
# It's good practice to have a simple root endpoint to check if the API is up.
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Intelligent Talent Acquisition API"}
