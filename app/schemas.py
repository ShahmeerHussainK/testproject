from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: constr()

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    text: str

class Post(BaseModel):
    id: int
    text: str
    owner_id: int

    class Config:
        orm_mode = True
