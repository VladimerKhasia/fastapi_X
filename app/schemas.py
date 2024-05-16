from datetime import datetime
from typing import Literal   #, Union
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostBase(BaseModel):
    title : str
    content: str
    published: bool = True
    #rating: Optional[int] = None  

class PostCreate(PostBase):    
    pass

class Post(PostBase):    
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

class PostResponse(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: str | None = None        #Union[str, None] = None

class Vote(BaseModel):
    post_id: int
    direction: Literal[0,1]

class ChatMessage(BaseModel):
    role: str = Literal['user', 'model']
    content: str