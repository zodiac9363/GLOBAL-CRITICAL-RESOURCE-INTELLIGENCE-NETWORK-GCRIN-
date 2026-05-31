import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import api
from .scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GCRIN API", description="Global Critical Resource Intelligence Network")

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    logger.info("Starting up GCRIN Backend...")
    start_scheduler()

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down GCRIN Backend...")
    stop_scheduler()

@app.get("/")
def read_root():
    return {"status": "GCRIN API is running"}
