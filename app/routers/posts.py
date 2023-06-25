from .. import models,schemas,utils
from fastapi import HTTPException, HTTPException, status, status, Response, Response, FastAPI, Depends,APIRouter
from fastapi.params import Dict, Optional, Body
from sqlalchemy.orm import Session, sessionmaker
from ..database import get_db
from typing import List
from .. import oauth2
from sqlalchemy import func
router = APIRouter(prefix="/posts", tags= ["posts"])

@router.get("/", response_model=List[schemas.PostOut])
def test(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,search: Optional[str] = ""):
    #all_posts = db.query(models.Post_python).filter(models.Post_python.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post_python, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post_python.id, isouter=True).group_by(models.Post_python.id).filter(
        models.Post_python.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_post(nuevo: schemas.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post_python(user_id=user.id, **nuevo.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    filtered_post = db.query(models.Post_python).filter(models.Post_python.id == id).first()

    post = db.query(models.Post_python, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post_python.id, isouter=True).group_by(models.Post_python.id).filter(models.Post_python.id == id).first()

    if not filtered_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    if filtered_post.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform that action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post_python).filter(models.Post_python.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    if post.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform that action")
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}")
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_filtered = db.query(models.Post_python).filter(models.Post_python.id == id)
    post_first = post_filtered.first()
    if not post_first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    if post_first.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform that action")
    post_filtered.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_filtered.first() 