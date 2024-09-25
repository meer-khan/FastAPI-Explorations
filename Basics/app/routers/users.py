from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from schemas import UserCreate, UserOut
import uuid
from icecream import ic
# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from decouple import config
import models
from database import get_db
import utils
import oauth

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    response_model_exclude=["password", "id"],
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
async def get_user(id:int, db: Session = Depends(get_db), user_id = Depends(oauth.get_current_user)): 
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with {id} does not found")
    
    return user