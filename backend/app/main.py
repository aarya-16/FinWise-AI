from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import transactions, insights, goals
import os
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="FinWise AI API",
    description="AI-powered financial coaching for gig workers",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    allow_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
else:
    allow_origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])

@app.get("/api")
async def root():
    return {
        "message": "Welcome to FinWise AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Mount static files (frontend build)
# The frontend dist folder should be at ../frontend/dist relative to backend
static_dir = Path(__file__).parent.parent.parent / "frontend" / "dist"

if static_dir.exists():
    # Serve static assets (js, css, images)
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")
    
    # Catch-all route to serve index.html for client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # If a file exists, serve it
        file_path = static_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        # Otherwise serve index.html (for React Router)
        return FileResponse(static_dir / "index.html")
