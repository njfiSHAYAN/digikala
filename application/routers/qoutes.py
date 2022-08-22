# TODO: add some logging

from datetime import datetime
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from typing import List
import redis
from pydantic import BaseModel

from application.db import schemas, crud
from application.routers.users import get_user
from application.util import get_db, get_logger, get_redis

logger = get_logger()
router = APIRouter()
redis = get_redis()


class Count(BaseModel):
    all_users: int
    you: int


@router.post("/add-qoute/", response_model=schemas.Qoute)
def add_qoute(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user),
    qoute: schemas.QouteCreate = Body(...),
):
    logger.info(f"user {user} is trying to add a qoute")
    crud.create_access_log(db, user)
    logger.info("qoute added successfully")
    return crud.create_qoute(db, qoute=qoute)


@router.get("/qoutes/", response_model=List[schemas.Qoute])
def add_qoute(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user),
):
    logger.info(f"user {user} is trying to read qoutes")
    crud.create_access_log(db, user)
    redis.incr("counter")
    redis.incr(str(user) + ":counter")
    logger.info("counters were updated in redis")
    a = crud.get_some_qoutes(db)
    return a


@router.get("/count/", response_model=Count)
def get_counter(user: schemas.User = Depends(get_user)):
    logger.info(f"user {user} is getting counts")
    user_cnt = redis.get(str(user) + ":counter")
    total_cnt = redis.get("counter")
    return {
        "all_users": total_cnt if total_cnt is not None else 0,
        "you": user_cnt if user_cnt is not None else 0,
    }


@router.get("/log/", response_model=List[datetime])
def get_counter(db: Session = Depends(get_db), user: schemas.User = Depends(get_user)):
    logger.info(f"user {user} is trying to get access logs")
    return crud.get_access_logs(db, user)
