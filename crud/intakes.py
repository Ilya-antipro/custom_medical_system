# crud/intakes.py

from sqlalchemy.orm import Session
from typing import List
from datetime import date
from models import IntakeLog
from schemas import IntakeLogCreate


def create_intake_log(db: Session, intake: IntakeLogCreate) -> IntakeLog:
    """Зарегистрировать факт приёма препарата."""
    db_intake = IntakeLog(
        schedule_id=intake.schedule_id,
        timestamp=intake.timestamp,
        confirmed_by=intake.confirmed_by,
        method=intake.method
    )
    db.add(db_intake)
    db.commit()
    db.refresh(db_intake)
    return db_intake


def get_intakes_by_patient_and_date(db: Session, patient_id: int, target_date: date) -> List[IntakeLog]:
    """Получить все подтверждённые приёмы пациента за указанную дату."""
    from models import Schedule  # локальный импорт во избежание циклической зависимости
    
    return (
        db.query(IntakeLog)
        .join(Schedule)
        .filter(
            Schedule.patient_id == patient_id,
            IntakeLog.timestamp >= target_date,
            IntakeLog.timestamp < target_date.replace(day=target_date.day + 1)
        )
        .all()
    )