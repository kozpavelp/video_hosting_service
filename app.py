import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

import config
from api.handlers.login_handlers import login_router
from api.handlers.user_handlers import user_router
from api.handlers.video_handlers import video_router
from api.service import service_router

sentry_sdk.init(dsn=config.SENTRY_URL, traces_sample_rate=1.0, profiles_sample_rate=1.0)

app = FastAPI(title="lessons")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
main_router.include_router(video_router, prefix='/video', tags=['video'])
main_router.include_router(service_router, tags=["service"])
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=config.PORT, reload=True)
