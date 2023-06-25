from fastapi import HTTPException, HTTPException, status, status, Response, Response, FastAPI, Depends
from fastapi.params import Optional, Body
from pydantic import PostgresDsn, BaseModel
from random import random, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

class contrato(BaseModel):
    titulo: str
    contenido: str
    publicado: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='jukolo10', cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        print('conexion exitosa a base de datos')
        break
    except Exception as error:
        print("Conexión fallida a base de datos")
        print("El error fue ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message":"tamos en la base"}

@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
    return {"status": "salio bien"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(nuevo: contrato):
    cursor.execute ("""INSERT INTO posts (titulo, contenido, publicado) VALUES (%s, %s, %s) RETURNING * """, (nuevo.titulo, nuevo.contenido, nuevo.publicado))
    post_creado = cursor.fetchone()
    conn.commit()
    return {"posts": post_creado} 
    

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""Select * FROM posts WHERE id = %s RETURNING * """, (str(id)))
    post_recuperado = cursor.fetchone()
    if not post_recuperado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    return {"post": post_recuperado}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    post_eliminado = cursor.fetchone()
    if not post_eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    conn.commit()

@app.put("/posts/{id}")
def update_posts(id: int, post: contrato):
    cursor.execute("""UPDATE posts SET titulo = %s, contenido = %s, publicado = %s WHERE id = %s RETURNING *""", (post.titulo, post.contenido, post.publicado, str(id)))
    post_actualizado = cursor.fetchone()
    if not post_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post con id: {id} no encontrado")
    conn.commit()
    return {'message': "updated post", "post": post_actualizado}
