from fastapi import FastAPI

from application.db import models
from application.db.database import engine

from application.routers import users, qoutes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, tags=["users"])
app.include_router(qoutes.router, tags=["qoutes"])
