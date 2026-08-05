from fastapi import FastAPI
from app.api.github_router import router as github_router
from app.api.query_router import router as query_router

app = FastAPI()

app.include_router(github_router)
app.include_router(query_router)

@app.get("/")
def home():
    return{
        "message":"codebase assistant api is uruku tundi"
    }