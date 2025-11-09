import os
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from core.settings import settings
from routers import chatbot_agent

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    try:
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(settings.GOOGLE_GENAI_USE_VERTEXAI)
        logger.info("API startup complete!!!")
        yield
        logger.info("Shutting down Application...")
    except Exception as e:
        logger.error(f"Failed to start application : {e}")
        raise

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_agent.router, prefix="/api")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")