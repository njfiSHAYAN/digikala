from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from application import config, util

logger = util.get_logger()


try:
    db_conf = config.CONFIG_DATA['db']
except KeyError as ex:
    logger.error('ex')
    logger.error('db dictionary expected in config.json file')
    exit(-1)
    

SQLALCHEMY_DATABASE_URL = db_conf.get('sql_alchemy_url', 'sqlite:///./sql_app.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, **db_conf.get('create_engine_args', {})
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()