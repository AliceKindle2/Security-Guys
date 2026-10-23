from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from models import User
from schemas import SignupRequest

router = APIRouter()

# POST /signup
# Check incoming request against SignupRequest in schemas.py
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_session)):
    # Intentionally log the user's whole request
    print("New signup:", data)

    # check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # convert request data into user row
    # intentionally save everything in plaintext, including pws, ssn, etc
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "email": user.email}