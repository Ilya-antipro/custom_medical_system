from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


# === Patient ===
class PatientBase(BaseModel):
    name: str = Field(..., max_length=100, description="Имя пациента")
    age: Optional[int] = Field(None, ge=0, le=150)
    diagnosis: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# === Medication ===
class MedicationBase(BaseModel):
    name: str = Field(..., max_length=150, description="Название препарата")
    dosage: Optional[str] = Field(None, max_length=50)
    form: Optional[str] = Field(None, max_length=30)
    criticality: float = Field(1.0, ge=0.1, le=10.0)


class MedicationCreate(MedicationBase):
    pass


class Medication(MedicationBase):
    id: int

    class Config:
        orm_mode = True


# === Schedule ===
class ScheduleBase(BaseModel):
    patient_id: int
    medication_id: int
    time_window_start: str = Field(..., regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    time_window_end: str = Field(..., regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    frequency_days: int = Field(1, ge=1)
    active: bool = True
    criticality: float = Field(1.0, ge=0.1, le=10.0)


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True


# === IntakeLog ===
class IntakeLogBase(BaseModel):
    schedule_id: int
    timestamp: datetime
    confirmed_by: str = Field(..., max_length=20)  # "app", "device", "caregiver"
    method: Optional[str] = Field(None, max_length=20)  # "button", "smartpill", "manual"


class IntakeLogCreate(IntakeLogBase):
    pass


class IntakeLog(IntakeLogBase):
    id: int

    class Config:
        orm_mode = True


# === Adherence Report ===
class AdherenceReport(BaseModel):
    date: date
    score: float = Field(..., ge=0.0, le=100.0, description="Оценка приверженности от 0 до 100")