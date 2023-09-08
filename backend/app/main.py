import uvicorn
from app import tasks
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.ingredients import ingredients_router
from app.api.api_v1.routers.meals import meals_router
from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.users_diet_requirements import users_diet_router
from app.core import config
from app.core.auth import get_current_active_user
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from fastapi import Depends, FastAPI
from starlette.requests import Request

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}


# Routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    users_diet_router,
    prefix="/api/v1",
    tags=["users_diet"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    ingredients_router,
    prefix="/api/v1",
    tags=["ingredients"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    meals_router,
    prefix="/api/v1",
    tags=["meals"],
    dependencies=[Depends(get_current_active_user)],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
