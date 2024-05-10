# HASH
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)