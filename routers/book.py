from fastapi import APIRouter, HTTPException, Response, Depends
from sqlmodel import Session, select
from db import get_session
from models import Book, User
from utils import verify_access_token
from schemas import Newbook
from schemas import GetUser
from schemas import Location
router = APIRouter(tags=['book'],
                   responses={404: {"description": "Not found"}})

@router.post('/create_book')
def new_book(data: Newbook, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    if not user:
        raise HTTPException(status_code=400, detail='Хрень сделал')

    book = Book(nazv=data.nazv, avtor=data.avtor, vladelec=user.id)
    session.add(book)
    session.commit()
    return 'compleate'

@router.get('/smotri')
def get_book(id: int, session: Session = Depends(get_session)):
    return session.exec(select(Book).where(Book.id == id)).first()

@router.get('/location')
def sm_location(data: Location, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    if not user:
        raise HTTPException(status_code=400, detail='Хрень сделал')

    lok = Location(location=data.location)
    session.add(lok)
    session.commit()
    return 'compleate'