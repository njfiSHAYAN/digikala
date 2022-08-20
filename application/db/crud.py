from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas
import random
from hashlib import sha256
import string
from application.util import get_config


config = get_config()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def hash_pass_decorator(func):
    def myfunc(db: Session, user: schemas.UserCreate):
        salt_length = config.get("password_salt_length", 4)
        salt = get_random_string(salt_length)
        hashed_password = salt + sha256((salt + user.password).encode()).hexdigest()
        user.password = hashed_password
        res = func(db, user, hashed_password)
        return res

    return myfunc


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


@hash_pass_decorator
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.Users(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_some_qoutes(db: Session, skip: int = 0, limit: int = 5):
    q = db.query(models.Qoutes).order_by(func.random()).offset(skip).limit(limit).all()
    return q


def create_qoute(db: Session, qoute: schemas.QouteCreate):
    db_qoute = models.Qoutes(**qoute.dict())
    db.add(db_qoute)
    db.commit()
    db.refresh(db_qoute)
    return db_qoute


def create_access_log(db: Session, user_id: int):
    db_log = models.Access_Logs(user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_access_logs(db: Session, user_id: int):
    return [
        l.time_created
        for l in db.query(models.Access_Logs).filter(
            models.Access_Logs.user_id == user_id
        )
    ]
