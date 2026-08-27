from __future__ import annotations

import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "development")
_DOCS_USERNAME = os.environ.get("DOCS_BASIC_AUTH_USER", "")
_DOCS_PASSWORD = os.environ.get("DOCS_BASIC_AUTH_PASS", "")

app = FastAPI(
    title="Bioassay Data Platform API",
    version="1.4.0",
    docs_url=None,
    redoc_url=None,
)


def _verify_docs_access(request: Request) -> None:
    if _ENVIRONMENT == "development":
        return

    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Basic ") or not _DOCS_USERNAME or not _DOCS_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Documentation access requires authentication in this environment.",
            headers={"WWW-Authenticate": "Basic"},
        )

    import base64

    encoded_credentials = auth_header.removeprefix("Basic ").strip()
    try:
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, _, password = decoded.partition(":")
    except (ValueError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed credentials.") from exc

    if username != _DOCS_USERNAME or password != _DOCS_PASSWORD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid documentation credentials.")


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def swagger_ui(_: Annotated[None, Depends(_verify_docs_access)]) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/api/v1/openapi.json",
        title=f"{app.title} — {_ENVIRONMENT.title()} Docs",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "tagsSorter": "alpha",
            "operationsSorter": "method",
            "defaultModelsExpandDepth": 1,
        },
    )


@app.get("/api/v1/openapi.json", include_in_schema=False)
async def openapi_json(_: Annotated[None, Depends(_verify_docs_access)]) -> dict:
    return app.openapi()
