"""
MemVra Brain - Bicameral Predictive Architecture
Version: 3.0
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the new API router
from api.routes import router as api_router

# Initialize FastAPI
app = FastAPI(
    title="MemVra Brain",
    version="3.0",
    description="Bicameral Predictive Memory Architecture"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    print("🧠 Starting MemVra Brain (Bicameral Architecture)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
