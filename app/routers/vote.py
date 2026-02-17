from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Vote, Post, User
from ..schemas import Vote as VoteSchema
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteSchema, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    
    # Check if the post actually exists
    post = session.get(Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {vote.post_id} does not exist")

    # Check if the user has ALREADY voted on this post
    vote_query = select(Vote).where(
        Vote.post_id == vote.post_id, 
        Vote.user_id == current_user.id
    )
    found_vote = session.exec(vote_query).first()

    #  Add vote (dir=1)
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=409, 
                detail=f"User {current_user.id} has already voted on post {vote.post_id}"
            )
        
        # Create the new vote
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "successfully added vote"}

    #  Remove vote (dir=0)
    else:
        if not found_vote:
            raise HTTPException(
                status_code=404, 
                detail="Vote does not exist"
            )

        # Delete the vote
        session.delete(found_vote)
        session.commit()
        return {"message": "successfully deleted vote"}