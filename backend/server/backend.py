from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.router import user

app = FastAPI(title="QuantumLeap Backend Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(user.router) 


@app.get("/ping")
def health_check():
    """Health check."""

    return {"message": "Hello I am working!"}

@app.get("/")
def intro():
    """
    This Endpoint for intro to this backend
    """
    return {"message": "This backend is for simple chess club website"}