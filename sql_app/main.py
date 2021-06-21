from typing import List, final
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    '''
    Dependency for using Database.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users', tags=['user'],
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered',
        )
    return crud.create_user(db, user)

@app.get('/users', tags=['user'],
    response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@app.get('/users/{user_id}', tags=['user'],
    response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    return db_user

@app.post('/users/{user_id}/items', tags=['item'],
    response_model=schemas.Item,
    status_code=status.HTTP_201_CREATED)
def create_item_for_user(user_id: int, item: schemas.ItemCreate,
                         db: Session = Depends(get_db)):
    return crud.create_user_item(db, item, user_id)

@app.get('/items', tags=['item'],
    response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    items = crud.get_items(db, skip, limit)
    return items
