from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr, conint

class UserOut(SQLModel):
    id: int
    email: str


# --- Post Schemas ---
class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut #nests the user info inside the response

# --- User Schemas ---
class UserBase(SQLModel):
    email: str 

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: Optional[str] = None

class Vote(SQLModel):
    post_id: int
    dir: int 
#combines the post object and vote count
class PostOut(SQLModel):
    Post: PostResponse
    votes: int  