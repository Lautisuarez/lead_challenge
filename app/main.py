from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import api
from app.utils.config import settings

app = FastAPI(
    title=f"API Lead registration - Open Dev Challenge",
    version=settings.VERSION
)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FRONTEND ENDPOINTS
@app.get("/", response_class=HTMLResponse, tags=["FRONTEND"])
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{transaction_id}", response_class=HTMLResponse, tags=["FRONTEND"])
def read_root(transaction_id: str, request: Request):
    return templates.TemplateResponse("confirm.html", {"request": request})

# BACKEND ENDPOINTS
app.include_router(api.router_v1)

