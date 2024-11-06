from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import trials

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trials.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Clinical Trials API"}