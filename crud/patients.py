# crud/patients.py

from sqlalchemy.orm import Session
from typing import List, Optional
from models import Patient
from schemas import PatientCreate


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    """Создать нового пациента."""
    db_patient = Patient(
        name=patient.name,
        age=patient.age,
        diagnosis=patient.diagnosis
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    """Получить пациента по ID."""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    """Получить список пациентов (с пагинацией)."""
    return db.query(Patient).offset(skip).limit(limit).all()