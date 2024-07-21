from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from hashlib import sha256

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    hash_password: str  # хэш пароля
    role: str = Field(default='user')
    email: str  # почта
    user_name: str  # имя
    city: str
    date_reg: datetime = Field(default_factory=datetime.utcnow)

    def verify_password(self, password):
        return self.hash_password == sha256(password.encode()).hexdigest()

    def super_user(self):
        self.role = 'super_user'

    def un_super_user(self):
        self.role = 'user'


class Book(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    nazv: str
    avtor: str
    vladelec: int

    def set_vladel(self, new_vladelec: int):
        self.vladelec = new_vladelec