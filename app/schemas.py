from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    username: constr(min_length=3) | None = None
    email: EmailStr | None = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
