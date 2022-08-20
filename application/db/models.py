from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)

    access = relationship("Access_Logs", back_populates="user")


class Qoutes(Base):
    __tablename__ = "qoute"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(Text)
    author = Column(String)
    number = Column(Integer)
    blockqoute = Column(Text)


class Access_Logs(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="access")
