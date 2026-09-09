import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.core.config import settings
from backend.features.reminders.controller import router as ReminderRouter
from backend.jobs.reminders import reminder_worker
from backend.features.auth.controller import router as AuthRouter
from backend.features.tasks.controller import router as TaskRouter
from backend.features.categories.controller import router as CategoryRouter
from backend.features.tags.controller import router as TagRouter
from backend.features.ai.controller import router as AIRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()
    worker = asyncio.create_task(
        reminder_worker(stop_event, settings.REMINDER_POLL_INTERVAL_SECONDS)
    )
    yield
    stop_event.set()
    await worker


app = FastAPI(
    title = "Complete.AI",
    version = "1.0.0",
    lifespan=lifespan,
    )

app.include_router(AuthRouter)
app.include_router(TaskRouter)
app.include_router(CategoryRouter)
app.include_router(TagRouter)
app.include_router(ReminderRouter)
app.include_router(AIRouter)

@app.get('/', tags=['Health'])
def health():
    return JSONResponse(
        content={
            "message" : "Congratulations, Your Application is up and running!!"
        }
    )