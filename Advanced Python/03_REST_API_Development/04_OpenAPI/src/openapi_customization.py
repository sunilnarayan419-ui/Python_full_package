from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Compound Intelligence API",
    description="Endpoints for compound registry, screening, and analysis jobs.",
    version="2.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/v2/openapi.json",
)


def build_custom_openapi_schema() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=[
            {"name": "compounds", "description": "Chemical compound registry operations."},
            {"name": "screening-runs", "description": "Automated screening execution and results."},
            {"name": "analysis-jobs", "description": "Asynchronous computational analysis jobs."},
        ],
    )

    schema["info"]["contact"] = {"name": "Platform Engineering", "email": "platform-eng@example-research.org"}
    schema["info"]["x-api-lifecycle"] = "stable"

    schema.setdefault("components", {}).setdefault("securitySchemes", {})["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
    }
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    schema["security"] = [{"ApiKeyAuth": []}, {"BearerAuth": []}]

    schema["components"].setdefault("schemas", {})["ErrorResponse"] = {
        "type": "object",
        "properties": {
            "error": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "example": "COMPOUND_NOT_FOUND"},
                    "message": {"type": "string"},
                    "request_id": {"type": "string", "format": "uuid"},
                },
                "required": ["code", "message", "request_id"],
            }
        },
        "required": ["error"],
    }

    schema["components"]["schemas"]["PageMeta"] = {
        "type": "object",
        "properties": {
            "limit": {"type": "integer", "minimum": 1, "maximum": 200},
            "offset": {"type": "integer", "minimum": 0},
            "count": {"type": "integer", "minimum": 0},
        },
        "required": ["limit", "offset", "count"],
    }

    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            operation.setdefault("responses", {})["429"] = {
                "description": "Rate limit exceeded.",
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}},
                "headers": {"Retry-After": {"schema": {"type": "integer"}}},
            }
            operation["responses"]["500"] = {
                "description": "Unexpected internal error.",
                "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}},
            }

    app.openapi_schema = schema
    return schema


app.openapi = build_custom_openapi_schema  # type: ignore[method-assign]
