from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    
    post_retrieved = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_retrieved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist")    

    vote_query = db.query(models.Vote).filter(models.Vote.user_id==current_user.id, models.Vote.post_id==vote.post_id)
    vote_retrieved = vote_query.first()

    if (vote.direction == 1):
        if vote_retrieved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"User {current_user.id} already has liked the post {vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit() 
        return {"message": "Successfully addded a vote"}
    else:
        if not vote_retrieved:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"User {current_user.id} has not liked the post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        return {"message": "Successfully removed a vote"}
    
