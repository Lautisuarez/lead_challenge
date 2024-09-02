from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api
from app.utils.config import settings

app = FastAPI(
    title=f"API Lead registration - Open Dev Challenge",
    version=settings.VERSION
)

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router_v1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
