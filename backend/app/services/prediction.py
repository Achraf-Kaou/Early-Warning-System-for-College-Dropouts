from typing import Any
import joblib
import numpy as np
import pandas as pd

from app.config import (
    PREPROCESSOR_PATH,
    BEST_MODEL_PATH,
    FEATURE_ORDER,
)
from app.schemas import StudentFeatures, PredictionResponse


class PredictionService:
    def __init__(self):
        self.preprocessor: Any = None
        self.model: Any = None
        self.loaded: bool = False
        self.error: str | None = None

    def load(self) -> None:
        try:
            if not PREPROCESSOR_PATH.exists():
                raise FileNotFoundError(f"Préprocesseur introuvable : {PREPROCESSOR_PATH}")
            if not BEST_MODEL_PATH.exists():
                raise FileNotFoundError(f"Modèle introuvable : {BEST_MODEL_PATH}")

            self.preprocessor = joblib.load(PREPROCESSOR_PATH)
            self.model = joblib.load(BEST_MODEL_PATH)
            self.loaded = True
            self.error = None
            print(f"✓ Modèle chargé : {BEST_MODEL_PATH}")
        except Exception as exc:
            self.loaded = False
            self.error = str(exc)
            print(f"✗ Erreur chargement modèle : {exc}")

    def _compute_derived(self, data: dict) -> dict:
        e1 = data.get("cu_1st_enrolled") or 0
        a1 = data.get("cu_1st_approved") or 0
        e2 = data.get("cu_2nd_enrolled") or 0
        a2 = data.get("cu_2nd_approved") or 0
        g1 = data.get("cu_1st_grade") or 0.0
        g2 = data.get("cu_2nd_grade") or 0.0

        if data.get("success_rate_1st") is None:
            data["success_rate_1st"] = (a1 / e1) if e1 > 0 else 0.0
        if data.get("success_rate_2nd") is None:
            data["success_rate_2nd"] = (a2 / e2) if e2 > 0 else 0.0
        if data.get("avg_grade") is None:
            data["avg_grade"] = float(np.mean([g1, g2]))
        if data.get("total_approved") is None:
            data["total_approved"] = int(a1 + a2)
        if data.get("grade_diff") is None:
            data["grade_diff"] = float(g2 - g1)
        return data

    def _risk_level(self, proba: float) -> str:
        if proba < 0.35:
            return "low"
        if proba < 0.60:
            return "medium"
        return "high"

    def _message(self, level: str, proba: float) -> str:
        pct = proba * 100
        if level == "low":
            return f"Risque faible de décrochage (probabilité estimée : {pct:.1f} %)."
        if level == "medium":
            return f"Risque modéré de décrochage (probabilité estimée : {pct:.1f} %). Un suivi pédagogique est recommandé."
        return f"Risque élevé de décrochage (probabilité estimée : {pct:.1f} %). Une intervention rapide est conseillée."

    def predict(self, student: StudentFeatures) -> PredictionResponse:
        if not self.loaded:
            raise RuntimeError(f"Modèle non chargé : {self.error}")

        data = self._compute_derived(student.model_dump())
        row = {col: data[col] for col in FEATURE_ORDER}
        X = pd.DataFrame([row], columns=FEATURE_ORDER)

        X_processed = self.preprocessor.transform(X)
        proba = float(self.model.predict_proba(X_processed)[0, 1])
        pred = int(self.model.predict(X_processed)[0])
        level = self._risk_level(proba)

        return PredictionResponse(
            prediction=pred,
            probability=round(proba, 4),
            risk_level=level,
            message=self._message(level, proba),
        )


# Instance unique (chargée au démarrage)
prediction_service = PredictionService()