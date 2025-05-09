from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.schemas import UserCreate, UserOut, Token, UserUpdate
from app.crud import create_user, authenticate_user, get_all_users, update_user
from app.auth import create_access_token, decode_token
from app.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(User).filter_by(username=payload["sub"]).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    return create_user(db, user.username, user.email, user.password)

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_all_users(db)

@app.put("/users/{user_id}", response_model=UserOut)
def update_user_api(user_id: int, data: UserUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = update_user(db, user_id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
