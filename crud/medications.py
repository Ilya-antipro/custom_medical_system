# crud/medications.py

from sqlalchemy.orm import Session
from typing import Optional
from models import Medication
from schemas import MedicationCreate


def create_medication(db: Session, medication: MedicationCreate) -> Medication:
    """Создать новый препарат."""
    db_med = Medication(
        name=medication.name,
        dosage=medication.dosage,
        form=medication.form,
        criticality=medication.criticality
    )
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med


def get_medication(db: Session, medication_id: int) -> Optional[Medication]:
    """Получить препарат по ID."""
    return db.query(Medication).filter(Medication.id == medication_id).first()