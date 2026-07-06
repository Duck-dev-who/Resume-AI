from fastapi import FastAPI
from app.api.resumes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    return {"message": "The Beginning"}