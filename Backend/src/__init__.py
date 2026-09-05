from fastapi import FastAPI
from contextlib  import asynccontextmanager

from .lesson.routes import router as lesson_router
from .exercise.routes import router as exercise_router
from .solution.routes import router as solution_router
from .database.main import init_db
from .AI.routes import router as ai_hint_router
from .auth.route import router as auth_router
from .progress.route import router as progress_router

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def life_span(app):
    print(f"server is starting................")
    await init_db()
    yield
    print(f"server has been stopped")

version='v1'


app=FastAPI(
    lifespan=life_span
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lesson_router, prefix=f"/api/{version}")
app.include_router(exercise_router, prefix=f"/api/{version}")
app.include_router(solution_router, prefix=f"/api/{version}")
app.include_router(ai_hint_router, prefix=f"/api/{version}")
app.include_router(auth_router, prefix=f"/api/{version}")
app.include_router(progress_router, prefix=f"/api/{version}")