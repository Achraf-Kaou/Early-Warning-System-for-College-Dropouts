from pydantic import BaseModel, Field
from typing import Optional


class StudentFeatures(BaseModel):
    marital_status: int
    application_mode: int
    application_order: int = Field(..., ge=0, le=9)
    course: int
    daytime_evening_attendance: int
    previous_qualification: int
    mother_qualification: int
    father_qualification: int
    mother_occupation: int
    father_occupation: int
    displaced: int
    debtor: int
    tuition_fees_up_to_date: int
    gender: int
    scholarship_holder: int

    age_at_enrollment: int = Field(..., ge=15, le=80)
    admission_grade: float
    previous_qualification_grade: float

    cu_1st_credited: int = 0
    cu_1st_enrolled: int = 0
    cu_1st_evaluations: int = 0
    cu_1st_approved: int = 0
    cu_1st_grade: float = 0.0
    cu_1st_without_evaluations: int = 0

    cu_2nd_credited: int = 0
    cu_2nd_enrolled: int = 0
    cu_2nd_evaluations: int = 0
    cu_2nd_approved: int = 0
    cu_2nd_grade: float = 0.0
    cu_2nd_without_evaluations: int = 0

    # Optionnelles : calculées automatiquement si absentes
    success_rate_1st: Optional[float] = None
    success_rate_2nd: Optional[float] = None
    avg_grade: Optional[float] = None
    total_approved: Optional[int] = None
    grade_diff: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str
    message: str