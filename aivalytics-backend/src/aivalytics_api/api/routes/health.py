from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a minimal liveness response for local and deployment checks."""
    return {"status": "ok"}
