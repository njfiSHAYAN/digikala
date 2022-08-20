import logging
from application.config import CONFIG_DATA
from application.db import database
import redis


def get_logger(severity="INFO"):
    logging.basicConfig(
        format="%(asctime)s  %(levelname)-6s %(filename)s:%(lineno)s - %(name)s.%(funcName)s()   %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, severity))
    return logger


def get_config():
    return CONFIG_DATA


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    redis_conf = get_config().get("redis", {})
    r = redis.Redis(
        host=redis_conf.get("host", "localhost"),
        port=redis_conf.get("port", 6379),
        db=redis_conf.get("db", 0),
        password=redis_conf.get("password", "redis"),
    )
    return r
