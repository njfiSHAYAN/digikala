from hashlib import sha256
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from application.util import get_db, get_logger, get_config
from application.db import schemas, crud

import datetime

import jwt

logger = get_logger()
router = APIRouter()

config = get_config().get("users", {})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def get_user(token: str = Depends(oauth2_scheme)):
    """
    decodes token header which is a jwt token.
    Its decoded fromat containes user_id and expires_at keys.
    expires_at is second fomrat(since 1970) and represents when tokent gets expired
    """
    try:
        user = jwt.decode(
            token,
            config.get("jwt_secret", "STRONG_SECRET"),
            algorithms=["HS256"],
        )
    except jwt.exceptions.DecodeError:
        logger.error("wrong jwt token was given")
        raise HTTPException(
            status_code=401, detail="your token is either invalid or expured"
        )

    if user["expires_at"] < int(datetime.datetime.now().strftime("%s")):
        # if expires_at has been passed
        logger.error("expired jwt token was given")
        raise HTTPException(
            status_code=401, detail="your token is either invalid or expured"
        )

    return int(user["user_id"])


@router.post("/register/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    logger.info("user is trying to register")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@router.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    logger.info("a user is trying to login")
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        logger.info("user did not exist")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = sha256(
        (user.hashed_password[:4] + form_data.password).encode()
    ).hexdigest()
    if hashed_password != user.hashed_password[4:]:
        logger("user had entered a wrong password")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = jwt.encode(
        {
            "user_id": user.id,
            "expires_at": int(datetime.datetime.now().strftime("%s"))
            + config.get("token_duration_seconds", 86400),
        },
        config.get("jwt_secret", "STRONG_SECRET"),
        algorithm="HS256",
    )
    logger.info("user successfully logged in")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(get_user)):
    return current_user
