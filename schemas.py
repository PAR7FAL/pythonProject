from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    user_name: str = Field(default='Имя')  # имя
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')
    city: str = Field(default='Город')

class GetUser(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    user_name: str = Field(default='Имя')  # имя
    city: str = Field(default='Город')

class Newbook(BaseModel):
    nazv: str = Field(default='Название книги')
    avtor: str = Field(default='автор книги')
    published_date: datetime = Field(None, description="Дата публикации книги")
    isbn: str = Field(None, description="ISBN книги")


class Location(BaseModel):
    location: str = Field(default='место встречи')

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Новое название книги")
    author: Optional[str] = Field(None, description="Новый автор книги")
    published_date: Optional[datetime] = Field(None, description="Новая дата публикации книги")
    isbn: Optional[str] = Field(None, description="Новый ISBN книги")

