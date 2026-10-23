from fastapi import FastAPI

#import models
from database import Base, engine
from routes import auth
from models import User, Appointment, Prescription
from database import get_session
from datetime import date
from fastcrud import crud_router

from schemas import SignupRequest, UpdateUser, ReadUser, CreateAppt, UpdateAppt, ReadAppt, CreatePrescription, UpdatePrescription, ReadPrescription

#Base.metadata.create_all(bind=engine)

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}

# Users table CRUD endpoints

user_router = crud_router(
    session = get_session,
    model = User,
    create_schema = SignupRequest,
    update_schema = UpdateUser,
    select_schema = ReadUser,
    path="/users",
    tags=["Users"]
)

appt_router = crud_router(
    session = get_session,
    model = Appointment,
    create_schema = CreateAppt,
    update_schema = UpdateAppt,
    select_schema = ReadAppt,
    path="/appointments",
    tags=["Appointments"]
)

prescription_router = crud_router(
    session = get_session,
    model = Prescription,
    create_schema = CreatePrescription,
    update_schema = UpdatePrescription,
    select_schema = ReadPrescription,
    path="/prescriptions",
    tags=["Prescriptions"]
)

app.include_router(user_router)
app.include_router(appt_router)
app.include_router(prescription_router)


"""
@app.post("/users")
async def create_user(full_name: str, email: str,
                      password: str, ssn: str, date_of_birth: date,
                      address: str, phone: str, medical_history: str,
                      credit_card_number: str):
    db = SessionLocal()
    db_user = User(full_name=full_name, email=email,
                   password=password, ssn=ssn, date_of_birth=date_of_birth,
                   address=address, phone=phone, medical_history=medical_history,
                   credit_card_number=credit_card_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Read
@app.get("/users/{id}")
async def read_user(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    return user

# Update
@app.put("/users/{id}")
async def update_user(id: int, full_name: str, email: str,
                      password: str, ssn: str, date_of_birth: date,
                      address: str, phone: str, medical_history: str,
                      credit_card_number: str):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == id).first()
    db_user.full_name = full_name
    db_user.email = email
    db_user.password = password
    db_user.ssn = ssn
    db_user.date_of_birth = date_of_birth
    db_user.address = address
    db_user.phone = phone
    db_user.medical_history = medical_history
    db_user.credit_card_number = credit_card_number
    db.commit()

    return db_user

# Delete
@app.delete("/users/{id}")
async def delete_user(id: int):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User removed successfully"}
    """
    
