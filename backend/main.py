from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.features.auth.controller import router as AuthRouter

app = FastAPI(
    title = "Complete.AI",
    version = "1.0.0"    
    )

app.include_router(AuthRouter)

@app.get('/', tags=['Health'])
def health():
    return JSONResponse(
        content={
            "message" : "Congratulations, Your Application is up and running!!"
        }
    )