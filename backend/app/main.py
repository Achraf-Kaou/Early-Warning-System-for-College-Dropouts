from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.services import prediction_service

app = FastAPI(
    title="API Alerte Précoce Décrochage Universitaire",
    description="Prédiction du risque de décrochage étudiant (Random Forest).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def startup():
    prediction_service.load()


@app.get("/")
def root():
    return {
        "message": "API Alerte Précoce Décrochage Universitaire",
        "docs": "/docs",
        "health": "/health",
        "predict": "POST /predict",
    }