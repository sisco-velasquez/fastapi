from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship 


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship: A user can have many posts
    posts: List["Post"] = Relationship(back_populates="owner")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Key
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationship: A post belongs to ONE user (owner)
    owner: Optional[User] = Relationship(back_populates="posts")


class Vote(SQLModel, table=True):
    # Composite Primary Key: The pair (user_id, post_id) must be unique
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    post_id: int = Field(foreign_key="post.id", primary_key=True)