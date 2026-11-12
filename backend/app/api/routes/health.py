from fastapi import APIRouter
from app.services import prediction_service
from app.config import BEST_MODEL_PATH, PREPROCESSOR_PATH

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "ok" if prediction_service.loaded else "error",
        "model_loaded": prediction_service.loaded,
        "model_path": str(BEST_MODEL_PATH),
        "preprocessor_path": str(PREPROCESSOR_PATH),
        "error": prediction_service.error,
    }