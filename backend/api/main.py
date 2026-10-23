
"""FastAPI application entry point for Meridian AI."""

from fastapi import FastAPI

from api.endpoints import (
    health_router,
    status_router,
    agent_router,
    rag_router,
)

app = FastAPI(
    title="Meridian AI",
    description="Multi-agent Procurement Audit and RAG Document Intelligence API",
    version="1.0.0",
)

# Register API routers
app.include_router(health_router)
app.include_router(status_router)
app.include_router(agent_router)
app.include_router(rag_router)


@app.get("/")
def root():
    """Basic API welcome endpoint."""
    return {
        "message": "Welcome to Meridian AI API",
        "docs": "/docs",
        "health": "/api/health",
    }

from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    for component in schema.get("components", {}).get("schemas", {}).values():
        for prop in component.get("properties", {}).values():
            if prop.get("contentMediaType") == "application/octet-stream":
                prop.pop("contentMediaType", None)
                prop["format"] = "binary"

            items = prop.get("items", {})
            if items.get("contentMediaType") == "application/octet-stream":
                items.pop("contentMediaType", None)
                items["format"] = "binary"

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
