from fastapi import APIRouter, HTTPException
from app.schemas import StudentFeatures, PredictionResponse
from app.services import prediction_service

router = APIRouter(tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(student: StudentFeatures):
    if not prediction_service.loaded:
        raise HTTPException(
            status_code=503,
            detail=f"Modèle non chargé : {prediction_service.error}"
        )
    try:
        return prediction_service.predict(student)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))