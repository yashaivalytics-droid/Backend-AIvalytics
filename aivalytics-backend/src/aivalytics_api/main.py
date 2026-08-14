from fastapi import FastAPI

from aivalytics_api.api.routes.health import router as health_router
from aivalytics_api.api.routes.dashboard import router as dashboard_router

app = FastAPI(title="AiValytics API", version="0.1.0")
app.include_router(health_router)
app.include_router(dashboard_router)