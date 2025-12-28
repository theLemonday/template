import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Base FastAPI Template", version="1.0.0")

# CORS Setup
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """
    K8s Liveness/Readiness Probe Endpoint
    """
    return {"status": "ok", "version": "1.0.0"}


@app.get("/")
def root():
    return {"message": "FastAPI Base Template Running"}
