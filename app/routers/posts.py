from typing import List, Optional
from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy import func 
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (%s,%s,%s) returning *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schemas.PostResponse]) 
def get_posts(current_user: int = Depends(oauth2.get_current_user), 
              db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                     ).outerjoin(models.Vote, models.Vote.post_id==models.Post.id
                                 ).group_by(models.Post.id
                                            ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
       
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                     ).outerjoin(models.Vote, models.Vote.post_id==models.Post.id
                                 ).group_by(models.Post.id
                                            ).filter(models.Post.id==id).first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Post with id {id} does not exist.")
    return post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning *""", 
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()   
    post_query = db.query(models.Post).filter(models.Post.id==id) 
    post_retrieved = post_query.first()
    if post_retrieved==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Post with id {id} does not exist.")  
    if post_retrieved.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="Not outorized action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()      
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE from posts WHERE id=%s returning *""", (str(id),))
    # cursor.fetchone()
    # conn.commit()    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_retrieved = post_query.first()
    if post_retrieved==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Post with id {id} does not exist.")
    if post_retrieved.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="Not outorized action")        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 