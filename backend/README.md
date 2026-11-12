# Backend – Alerte précoce du décrochage universitaire

API FastAPI pour prédire le risque de décrochage d’un étudiant  
(modèle retenu : **Random Forest**).

---

## Structure du projetbackend/
├── README.md
├── pyproject.toml
├── uv.lock
├── tests/
└── app/
├── init.py
├── main.py                 # Point d'entrée FastAPI
├── config.py               # Chemins + liste des features
├── api/
│   ├── init.py
│   └── routes/
│       ├── init.py
│       ├── health.py       # GET /health
│       └── predict.py      # POST /predict
├── schemas/
│   ├── init.py
│   └── student.py          # StudentFeatures + PredictionResponse
├── services/
│   ├── init.py
│   └── prediction.py       # Chargement modèle + logique de prédiction
└── ml/
├── dataset/
│   ├── raw/
│   └── processed/
├── models/             # .joblib (best_model, preprocessor, ...)
└── notebooks/          # Notebooks des Phases 1 à 3text---

## Prérequis

Les fichiers suivants doivent exister :app/ml/models/best_model.joblib
app/ml/models/preprocessor.joblibtextIls sont produits à la fin de la Phase 3 (`04_modeling_and_evaluation.ipynb`).

---

## Installation

Avec **uv** (recommandé si tu utilises déjà `pyproject.toml` / `uv.lock`) :

```bash
cd backend
uv syncOu avec pip :Bashcd backend
pip install fastapi uvicorn[standard] pydantic scikit-learn pandas numpy joblibLancementDepuis le dossier backend/ :Bashuvicorn app.main:app --reload --host 0.0.0.0 --port 8000Puis ouvrir :




















URLDescriptionhttp://127.0.0.1:8000/docsDocumentation interactive Swaggerhttp://127.0.0.1:8000/healthStatut du modèlehttp://127.0.0.1:8000/Info de baseEndpointsGET /healthVérifie que le modèle et le préprocesseur sont bien chargés.Exemple de réponse :JSON{
  "status": "ok",
  "model_loaded": true,
  "model_path": ".../best_model.joblib",
  "preprocessor_path": ".../preprocessor.joblib",
  "error": null
}POST /predictPrédit le risque de décrochage pour un étudiant.Corps de la requête : voir l’exemple dans /docs (schéma StudentFeatures).Exemple de réponse :JSON{
  "prediction": 1,
  "probability": 0.72,
  "risk_level": "high",
  "message": "Risque élevé de décrochage (probabilité estimée : 72.0 %). Une intervention rapide est conseillée."
}
























ChampSignificationprediction0 = non-risque, 1 = risque de décrochageprobabilityProbabilité de décrochage (entre 0 et 1)risk_levellow (< 0.35) / medium (0.35–0.60) / high (≥ 0.60)messageMessage lisible pour l’utilisateurLes features dérivées (success_rate_1st, avg_grade, etc.) sont calculées automatiquement si elles ne sont pas fournies.Test rapide avec curlBashcurl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "marital_status": 1,
    "application_mode": 17,
    "application_order": 1,
    "course": 9254,
    "daytime_evening_attendance": 1,
    "previous_qualification": 1,
    "mother_qualification": 19,
    "father_qualification": 12,
    "mother_occupation": 5,
    "father_occupation": 9,
    "displaced": 0,
    "debtor": 0,
    "tuition_fees_up_to_date": 1,
    "gender": 1,
    "scholarship_holder": 0,
    "age_at_enrollment": 20,
    "admission_grade": 125.0,
    "previous_qualification_grade": 130.0,
    "cu_1st_enrolled": 6,
    "cu_1st_approved": 6,
    "cu_1st_grade": 13.5,
    "cu_2nd_enrolled": 6,
    "cu_2nd_approved": 5,
    "cu_2nd_grade": 12.8
  }'