from typing import List, Optional
from fastapi import status, Response, HTTPException, Depends, APIRouter, Body
from sqlalchemy import func 
from sqlalchemy.orm import Session
from app.ai_model.chat_service import chat_model
from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(
    prefix="/gemma",
    tags=['Gemma']
)


@router.post("/", response_model=List[schemas.ChatMessage]) 
async def chat(user_input: str = Body(...),
               current_user: int = Depends(oauth2.get_current_user)):
    if not chat_model:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Access to the model failed.")
    response = chat_model.generate(user_input)
    # chat_model.get_full_history_generator()
    return response