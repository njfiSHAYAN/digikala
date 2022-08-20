from fastapi import APIRouter, Body, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from application.db import schemas, crud
from application.routers.users import get_user
from application.util import get_config, get_db, get_logger

logger = get_logger()
router = APIRouter()


@router.post("/add-qoute/", response_model=schemas.Qoute)
def add_qoute(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user),
    qoute: schemas.QouteCreate = Body(...),
):
    return crud.create_qoute(db, qoute=qoute)


@router.post("/qoutes/", response_model=List[schemas.Qoute])
def add_qoute(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_user),
):
    a = crud.get_some_qoutes(db)
    return a
