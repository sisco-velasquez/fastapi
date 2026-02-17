from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List, Optional

from ..oauth2 import get_current_user
from ..database import get_session
from ..models import Post,User, Vote
from ..schemas import PostCreate, PostUpdate, PostResponse, PostOut

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    
    
    db_post = Post(**post.dict(), user_id=current_user.id)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostOut])
def get_posts(
    session: Session = Depends(get_session), 
    limit: int = 10, 
    skip: int = 0, 
    search: Optional[str] = ""
):

    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))  # Select Post AND Count
        .join(Vote, isouter=True)                              # Left Outer Join (keep posts with 0 votes)
        .group_by(Post.id)                                     # Group results by Post
        .where(Post.title.contains(search))                    # Filter by search term
        .offset(skip)
        .limit(limit)
    )

    results = session.exec(statement).all()
    
    return results


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, session: Session = Depends(get_session)):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post_data = updated_post.dict(exclude_unset=True)
    
    for field, value in post_data.items():
        setattr(post, field, value)

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    session.delete(post)
    session.commit()
    return None 