from datetime import date
from models import User

from pydantic import BaseModel, ConfigDict

class SignupRequest(BaseModel):
    full_name: str
    email: str
    password: str
    ssn: str
    date_of_birth: date
    address: str
    phone: str
    medical_history: str
    credit_card_number: str

class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    password: str
    ssn: str
    date_of_birth: date
    address: str
    phone: str
    medical_history: str
    credit_card_number: str

class UpdateUser(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    ssn: str | None = None
    date_of_birth: date | None = None
    address: str | None = None
    phone: str | None = None
    medical_history: str | None = None
    credit_card_number: str | None = None

class CreateAppt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    patient_ssn: str
    patient_full_name: str
    patient_email: str
    doctor_name: str
    scheduled_at: date
    reason: str
    #user: User

class ReadAppt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    patient_ssn: str
    patient_full_name: str
    patient_email: str
    doctor_name: str
    scheduled_at: date
    reason: str
    #user: User

class UpdateAppt(BaseModel):
    patient_full_name: str | None = None
    patient_email: str | None = None
    doctor_name: str | None = None
    scheduled_at: date | None = None
    reason: str | None = None

class CreatePrescription(BaseModel):
    user_id: int

    patient_ssn: str
    patient_full_name: str
    patient_email: str

    medication_name: str
    dosage: str
    prescribing_doctor: str
    prescribed_at: date

    #user: User

class ReadPrescription(BaseModel):
    id: int
    user_id: int

    patient_ssn: str
    patient_full_name: str
    patient_email: str

    medication_name: str
    dosage: str
    prescribing_doctor: str
    prescribed_at: date

    #user: User

class UpdatePrescription(BaseModel):
    patient_full_name: str | None = None
    patient_email: str | None = None

    medication_name: str | None = None
    dosage: str | None = None
    prescribing_doctor: str | None = None
    prescribed_at: date | None = None
    