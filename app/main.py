from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import Base, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events.

    Handles startup database connection/table initialization and shutdown cleanup.
    """
    # Startup: Create tables (useful for development/quickstarts)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown: Dispose engine connection pool
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# Set CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Welcome / root endpoint."""
    return {
        "message": "Welcome to the FastAPI Template Application",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "project": settings.PROJECT_NAME, "version": settings.VERSION}
