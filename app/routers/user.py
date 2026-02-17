from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserResponse, UserUpdate
from ..utils import hash_password

# Use APIRouter instead of FastAPI
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    # Hash the password
    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd
    
    # Create the user model
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user

@router.get("/", response_model=List[UserResponse])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.put("/{id}", response_model=UserResponse) 
def update_user(id: int, updated_user: UserUpdate, session: Session = Depends(get_session)):
    
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    # Get the data from the request
    user_data = updated_user.dict(exclude_unset=True)

    # Hash password if it is being updated
    if "password" in user_data:
        hashed_pwd = hash_password(user_data["password"])
        user_data["password"] = hashed_pwd

    # Update the database fields
    for field, value in user_data.items():
        setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user