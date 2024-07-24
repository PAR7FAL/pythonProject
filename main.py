import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from db import engine
from routers import user, book
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(book.router)


# uvicorn.run(app, port=8001)