from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.features.auth.controller import router as AuthRouter
from backend.features.tasks.controller import router as TaskRouter
from backend.features.categories.controller import router as CategoryRouter
from backend.features.tags.controller import router as TagRouter

app = FastAPI(
    title = "Complete.AI",
    version = "1.0.0"    
    )

app.include_router(AuthRouter)
app.include_router(TaskRouter)
app.include_router(CategoryRouter)
app.include_router(TagRouter)

@app.get('/', tags=['Health'])
def health():
    return JSONResponse(
        content={
            "message" : "Congratulations, Your Application is up and running!!"
        }
    )