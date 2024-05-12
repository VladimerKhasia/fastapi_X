from calendar import timegm
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models, config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = config.settings.SECRET_KEY
ALGORITHM = config.settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    #expire = timegm(datetime.now(timezone.utc).utctimetuple()) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print("-----------------------------------------------------------------", expire, to_encode)
    #encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm="HS256")

    return encoded_jwt    



def validate_access_token(token: str, creadential_error):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]) 
        id: str = payload.get("id")
        if id is None:
            raise creadential_error
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise creadential_error
    return token_data
    
def get_current_user(token: str =  Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):
    credential_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                     detail="Invalid Credentials",
                                     headers={"WWW-Authenticate": "bearer"})
    token_data = validate_access_token(token, credential_error)
    current_user = db.query(models.User).filter(models.User.id==token_data.id).first()
    return current_user 
