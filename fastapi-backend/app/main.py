from fastapi import FastAPI
from app.routers import trials

app = FastAPI()

app.include_router(trials.router)

@app.get("/")
async def root():
   return {"message": "Welcome to the Clinical Trials API"}
