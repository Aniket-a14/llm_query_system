from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import query_routes

app = FastAPI(title="LLM Query System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the LLM Query System API!"}
