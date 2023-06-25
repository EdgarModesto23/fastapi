from pydantic import conint, config, class_validators, BaseModel, EmailStr
from datetime import date, date, datetime
from typing import Optional

class contrato(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Out(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class Response(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: Out
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post_python: Response
    votes: int
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserOut(Out):
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
