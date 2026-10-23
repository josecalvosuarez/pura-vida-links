"""HTTP layer (T009, T012, T014, T016, T020). Contract: specs/001-short-links/contracts/openapi.yaml"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, field_validator

from .codes import generate_code
from .logging import get_logger
from .storage import DuplicateCode, LinkStore
from .validation import MAX_URL_LENGTH, ValidationError, normalize_alias, validate_url

log = get_logger()
MAX_CODE_RETRIES = 5  # research.md Decision 3


class CreateLink(BaseModel):
    url: str = Field(max_length=MAX_URL_LENGTH, examples=["https://gdg.community.dev/gdg-pura-vida/"])
    alias: str | None = Field(default=None, examples=["gdg-oct"])

    @field_validator("url")
    @classmethod
    def _url(cls, v: str) -> str:  # FR-002, FR-011
        try:
            return validate_url(v)
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("alias")
    @classmethod
    def _alias(cls, v: str | None) -> str | None:  # FR-008
        if v is None:
            return None
        try:
            return normalize_alias(v)
        except ValidationError as exc:
            raise ValueError(str(exc)) from exc


class LinkOut(BaseModel):
    code: str
    url: str
    short_url: str
    created_at: str


def create_app(db_path: str | Path | None = None, base_url: str | None = None) -> FastAPI:
    db_path = db_path or os.getenv("LINKS_DB", "links.db")
    base_url = (base_url or os.getenv("LINKS_BASE_URL", "http://localhost:8000")).rstrip("/")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.store = LinkStore(db_path)
        yield
        app.state.store.close()

    app = FastAPI(title="Pura Vida Links", version="1.0.0", lifespan=lifespan)

    @app.get("/health")
    def health() -> dict:  # FR-009
        return {"status": "ok"}

    @app.post("/links", status_code=201, response_model=LinkOut,
              responses={409: {"description": "Alias already in use"}})
    def create_link(body: CreateLink, request: Request) -> LinkOut:  # FR-001, FR-003, FR-006, FR-007
        store: LinkStore = request.app.state.store
        if body.alias:
            try:
                link = store.insert(body.alias, body.url)
            except DuplicateCode:
                raise HTTPException(409, f"Alias '{body.alias}' is already in use")
        else:
            for _ in range(MAX_CODE_RETRIES):
                try:
                    link = store.insert(generate_code(), body.url)
                    break
                except DuplicateCode:
                    continue
            else:  # pragma: no cover — astronomically unlikely
                raise HTTPException(503, "Could not allocate a unique code, try again")
        log.info("link_created", extra={"extra_fields": {"code": link.code}})
        return LinkOut(code=link.code, url=link.url, short_url=f"{base_url}/{link.code}",
                       created_at=link.created_at)

    @app.get("/{code}", status_code=307, responses={404: {"description": "Unknown code"}})
    def follow(code: str, request: Request) -> RedirectResponse:  # FR-004, FR-005, FR-013
        store: LinkStore = request.app.state.store
        link = store.get(code) or store.get(code.lower())
        if link is None:
            raise HTTPException(404, "Short link not found")
        return RedirectResponse(link.url, status_code=307)

    return app


app = create_app()
