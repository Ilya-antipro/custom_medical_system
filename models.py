from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    age = Column(Integer, nullable=True)
    diagnosis = Column(Text, nullable=True)  # Например, "Альцгеймер, ГБ"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    schedules = relationship("Schedule", back_populates="patient", cascade="all, delete-orphan")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    dosage = Column(String(50), nullable=True)      # Например, "5 мг"
    form = Column(String(30), nullable=True)        # Таблетка, капсула и т.д.
    criticality = Column(Float, default=1.0)        # Вес для алгоритма adherence (1.0 = базовый, 2.0 = критичный)

    # Связи
    schedules = relationship("Schedule", back_populates="medication")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    
    # Временное окно приёма (например, "08:00–10:00")
    time_window_start = Column(String(10), nullable=False)   # Формат: "HH:MM"
    time_window_end = Column(String(10), nullable=False)     # Формат: "HH:MM"
    
    # Дополнительно
    frequency_days = Column(Integer, default=1)              # Повтор каждые N дней (1 = ежедневно)
    active = Column(Boolean, default=True)                   # Активно ли расписание сейчас
    criticality = Column(Float, default=1.0)                 # Уровень важности конкретного назначения

    # Связи
    patient = relationship("Patient", back_populates="schedules")
    medication = relationship("Medication", back_populates="schedules")
    intakes = relationship("IntakeLog", back_populates="schedule", cascade="all, delete-orphan")


class IntakeLog(Base):
    __tablename__ = "intake_logs"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    confirmed_by = Column(String(20), nullable=False)        # "app", "device", "caregiver"
    method = Column(String(20), nullable=True)               # Доп. детализация: "button", "smartpill", "manual"

    # Связь
    schedule = relationship("Schedule", back_populates="intakes")