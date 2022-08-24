from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.annotation import (
    users as annotation_users,
    moments as annotation_moments,
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

# Add routers
routers = [
    annotation_users.router,
    annotation_moments.router,
]
for router in routers:
    app.include_router(router)

