from fastapi import FastAPI
from .routers import login, users, posts, votes
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine) #you do not need this anymore when using alembic

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/")
def read_root():
    return {"Hello": "My World"}

