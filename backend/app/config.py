from pathlib import Path

# Racine de l'app (dossier app/)
APP_DIR = Path(__file__).resolve().parent

# Dossier des modèles entraînés (Phase 3)
MODELS_DIR = APP_DIR / "ml" / "models"

PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
BEST_MODEL_PATH = MODELS_DIR / "best_model.joblib"

# Ordre exact des features (doit correspondre à la Phase 3)
NUMERIC_FEATURES = [
    "age_at_enrollment",
    "admission_grade",
    "previous_qualification_grade",
    "cu_1st_credited", "cu_1st_enrolled", "cu_1st_evaluations",
    "cu_1st_approved", "cu_1st_grade", "cu_1st_without_evaluations",
    "cu_2nd_credited", "cu_2nd_enrolled", "cu_2nd_evaluations",
    "cu_2nd_approved", "cu_2nd_grade", "cu_2nd_without_evaluations",
    "success_rate_1st", "success_rate_2nd",
    "avg_grade", "total_approved", "grade_diff",
]

CATEGORICAL_FEATURES = [
    "marital_status",
    "application_mode",
    "application_order",
    "course",
    "daytime_evening_attendance",
    "previous_qualification",
    "mother_qualification", "father_qualification",
    "mother_occupation", "father_occupation",
    "displaced",
    "debtor",
    "tuition_fees_up_to_date",
    "gender",
    "scholarship_holder",
]

FEATURE_ORDER = NUMERIC_FEATURES + CATEGORICAL_FEATURES