from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from core.settings import app_settings
import logging
import os

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from domain.exceptions.auth_errors import (
    MissingPermissionError,
    MissingRoleError,
    UnauthorizedUserError,
)
from domain.exceptions.german_verb_errors import (
    GermanVerbNotFoundError,
    GermanVerbAlreadyExistsError,
)
from domain.exceptions.german_noun_errors import (
    GermanNounNotFoundError,
    GermanNounAlreadyExistsError,
)
from domain.exceptions.user_profile_errors import (
    UserProfileNotFoundError,
    UserProfileAlreadyExistsError,
    LanguageNotFoundError,
)
from domain.exceptions.exercise_errors import ExerciseGenerationError, LLMProviderError
from application.routers import (
    language_router,
    german_noun_router,
    german_verb_router,
    user_profile_router,
    exercise_router,
)
from infrastructure.observability.logging.azure_handler import (
    setup_azure_handler,
    get_structured_logger,
)
from infrastructure.observability.tracing.azure_tracing import setup_azure_tracer
from infrastructure.observability.metrics.azure_metrics import init_azure_metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

logging.basicConfig(
    level=app_settings.log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s starting", app_settings.service_name)
    try:
        from sqlalchemy import text
        from infrastructure.databases.database import engine
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection: OK")
    except Exception as e:
        logger.error("Database connection failed: %s", e, exc_info=True)
        raise
    yield
    logger.info("%s shutting down", app_settings.service_name)


app = FastAPI(
    title=app_settings.service_name,
    description="LanguageApp Deutsch API - practice German nouns and verbs",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in app_settings.cors_allow_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(MissingRoleError)
async def role_exception_handler(request, exc: MissingRoleError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc), "role": exc.role_name})


@app.exception_handler(MissingPermissionError)
async def permission_exception_handler(request, exc: MissingPermissionError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc), "resource": exc.resource, "action": exc.action},
    )


@app.exception_handler(UnauthorizedUserError)
async def unauthorized_exception_handler(request, exc: UnauthorizedUserError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})


@app.exception_handler(GermanVerbNotFoundError)
async def verb_not_found_handler(request, exc: GermanVerbNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(GermanVerbAlreadyExistsError)
async def verb_exists_handler(request, exc: GermanVerbAlreadyExistsError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(GermanNounNotFoundError)
async def noun_not_found_handler(request, exc: GermanNounNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(GermanNounAlreadyExistsError)
async def noun_exists_handler(request, exc: GermanNounAlreadyExistsError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(UserProfileNotFoundError)
async def profile_not_found_handler(request, exc: UserProfileNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(UserProfileAlreadyExistsError)
async def profile_exists_handler(request, exc: UserProfileAlreadyExistsError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.exception_handler(LanguageNotFoundError)
async def language_not_found_handler(request, exc: LanguageNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(ExerciseGenerationError)
async def exercise_generation_handler(request, exc: ExerciseGenerationError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": exc.detail})


@app.exception_handler(LLMProviderError)
async def llm_provider_handler(request, exc: LLMProviderError):
    return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={"detail": exc.detail, "provider": exc.provider})


app.include_router(language_router.router)
app.include_router(german_noun_router.router)
app.include_router(german_verb_router.router)
app.include_router(user_profile_router.router)
app.include_router(exercise_router.router)


@app.get("/")
async def root():
    return {"message": f"Welcome to {app_settings.service_name}"}


@app.get("/health")
async def health():
    return {"status": "ok"}
