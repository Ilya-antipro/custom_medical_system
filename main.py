from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from database import get_db, engine
import models
import schemas
import crud

# Создаём таблицы (в продакшене используйте миграции, например, Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartPill API", description="REST API для управления персонализированными планами приёма лекарств")

# --- Patients ---
@app.post("/patients/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

# --- Medications ---
@app.post("/medications/", response_model=schemas.Medication, status_code=status.HTTP_201_CREATED)
def create_medication(med: schemas.MedicationCreate, db: Session = Depends(get_db)):
    return crud.create_medication(db=db, medication=med)

# --- Schedules ---
@app.post("/schedules/", response_model=schemas.Schedule, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    # Простая проверка: пациент и препарат должны существовать
    if not crud.get_patient(db, schedule.patient_id):
        raise HTTPException(status_code=400, detail="Patient not found")
    if not crud.get_medication(db, schedule.medication_id):
        raise HTTPException(status_code=400, detail="Medication not found")
    return crud.create_schedule(db=db, schedule=schedule)

@app.get("/patients/{patient_id}/schedules/", response_model=List[schemas.Schedule])
def read_patient_schedules(patient_id: int, db: Session = Depends(get_db)):
    if not crud.get_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.get_schedules_by_patient(db, patient_id=patient_id)

# --- Intake Logs ---
@app.post("/intakes/", response_model=schemas.IntakeLog, status_code=status.HTTP_201_CREATED)
def log_intake(intake: schemas.IntakeLogCreate, db: Session = Depends(get_db)):
    if not crud.get_schedule(db, intake.schedule_id):
        raise HTTPException(status_code=400, detail="Schedule not found")
    return crud.create_intake_log(db=db, intake=intake)

# --- Adherence Score (ваша бизнес-логика) ---
@app.get("/adherence/{patient_id}/daily", response_model=schemas.AdherenceReport)
def get_daily_adherence(patient_id: int, date: datetime.date = None, db: Session = Depends(get_db)):
    if not crud.get_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if date is None:
        date = datetime.date.today()

    schedules = crud.get_schedules_by_patient(db, patient_id)
    intakes = crud.get_intakes_by_patient_and_date(db, patient_id, date)

    # Простейшая реализация штрафной системы
    total_weight = 0.0
    penalty = 0.0

    intake_dict = {i.schedule_id: i for i in intakes}

    for sched in schedules:
        # Вес: критичные препараты имеют больший вес
        weight = sched.criticality or 1.0
        total_weight += weight

        intake = intake_dict.get(sched.id)
        if intake is None:
            # Пропущен приём — полный штраф
            penalty += weight
        else:
            # Можно добавить логику проверки временного окна
            pass

    score = max(0.0, 100.0 * (1 - penalty / (total_weight if total_weight > 0 else 1)))

    return schemas.AdherenceReport(date=date, score=round(score, 2))