# crud/schedules.py

from sqlalchemy.orm import Session
from typing import List, Optional
from models import Schedule
from schemas import ScheduleCreate


def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
    """Создать новое расписание приёма препарата."""
    db_schedule = Schedule(
        patient_id=schedule.patient_id,
        medication_id=schedule.medication_id,
        time_window_start=schedule.time_window_start,
        time_window_end=schedule.time_window_end,
        frequency_days=schedule.frequency_days,
        active=schedule.active,
        criticality=schedule.criticality
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """Получить расписание по ID."""
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def get_schedules_by_patient(db: Session, patient_id: int) -> List[Schedule]:
    """Получить все активные расписания пациента."""
    return db.query(Schedule).filter(Schedule.patient_id == patient_id, Schedule.active.is_(True)).all()