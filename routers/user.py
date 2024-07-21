from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select

from db import get_session
from models import User
from schemas import UserCreate, GetUser
from utils import create_access_token, verify_access_token, hash_password

router = APIRouter(tags=['user'],
                   responses={404: {"description": "Not found"}})


@router.post('/login/')
async def login_user(response: Response,
                     session: Session = Depends(get_session),
                     data: OAuth2PasswordRequestForm = Depends()
                     ):
    user = session.exec(select(User).where(
        User.email == data.username)).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401,
                            detail='Incorrect email or password',
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token = create_access_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register/')
def reg_user(user: UserCreate,
             session: Session = Depends(get_session)
             ):
    temp_user = session.exec(select(User).where(User.email == user.email)).first()
    if temp_user:
        raise HTTPException(status_code=400,
                            detail='Email is busy')
    if user.password != user.complete_password:
        raise HTTPException(status_code=401, detail='Incorrect password')
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email,
                   hash_password=hashed_password,
                   user_name=user.user_name,
                   city=user.city
                   )
    session.add(db_user)
    session.commit()
    raise HTTPException(status_code=200)


@router.post('/token')
def login_user_for_token(response: Response,
                         session: Session = Depends(get_session),
                         data: OAuth2PasswordRequestForm = Depends()
                         ):
    user = session.exec(select(User).where(
        User.email == data.username)).first()  # так как у нас нет username как такогого, мы будем использовать email
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401,
                            detail='Incorrect email or password',
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token = create_access_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me/')
def user_me(temp_user: User = Depends(verify_access_token)):
    user = GetUser(email=temp_user.email, user_name=temp_user.user_name, city=temp_user.city)
    return user