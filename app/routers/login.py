from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(
    tags=['Login']
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="Invalid credentials.")
    if not utils.verify(user_credentials.password, user.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="Invalid credentials.")    
    token = oauth2.create_access_token(data={"id": user.id})            
    return {"access_token": token, "token_type": "bearer"}
