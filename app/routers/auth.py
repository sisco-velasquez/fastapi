from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..database import get_session
from ..models import User
from ..utils import verify_password
from ..oauth2 import create_access_token
from ..schemas import Token

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    
    #Find the user by email (OAuth2 form stores email in 'username')
    user = session.exec(select(User).where(User.email == user_credentials.username)).first()

    #If user doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials"
        )

    #Verify the password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials"
        )

    # Create the JWT Token
    # We embed the user ID into the token so we know who is logged in later
    access_token = create_access_token(data={"user_id": user.id})

    #Return the token
    return {"access_token": access_token, "token_type": "bearer"}