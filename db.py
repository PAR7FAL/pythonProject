from fastapi.security import HTTPBasic
from sqlmodel import Session
from sqlmodel import create_engine

engine = create_engine("sqlite:///./durka.db")
security = HTTPBasic()


def get_session():
    with Session(engine) as session:
        yield session