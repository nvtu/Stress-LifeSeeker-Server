from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_info'

    username = Column(String(250), ForeignKey('user.username'), primary_key = True)
    name = Column(String(250), nullable = True, default = '')


class UserInDB(Base):
    __tablename__ = 'user'

    username = Column(String(250), primary_key = True, index = True)
    hashed_password = Column(String, nullable = False)


class ExpirationTime(Base):
    __tablename__ = 'expiration_time'

    username = Column(String(250), ForeignKey('user.username'), primary_key = True)
    exp = Column(Integer, nullable = False)
    iat = Column(Integer, nullable = False)
