from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
from database import get_db
import utils
from icecream import ic
import schemas
import oauth

router = APIRouter(tags=["Authentication"])

@router.post("/login/")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db) ):
    print("*****************")
    ic(user_credentials)

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
       
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials")
    
    access_token = oauth.create_access_token(data = {"user_id": user.id})

    return  {"access_token": access_token, "token_type": "bearer",}