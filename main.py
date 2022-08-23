from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.annotation import (
    users as annotation_users,
)


app = FastAPI(
    name = "LifeSeeker -- Stress Version", 
    docs_url = "/docs", 
    redoc_url = "/redoc"
)

# Setup CORS policy for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(annotation_users.router)

@app.get("/")
async def root():
    return {"message": "Hello World!!!!"}