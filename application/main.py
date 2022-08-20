from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from application.db import crud, models, schemas
from application.db.database import engine
from application.util import get_db

from application.routers import users, qoutes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, tags=["users"])
app.include_router(qoutes.router, tags=["qoutes"])
