import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.handlers.login_handlers import login_router
from api.handlers.user_handlers import user_router


app = FastAPI(title="lessons")

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
