from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from seetree.config import Config


def _get_engine(url, echo):
    return create_engine(url, echo=echo)


def get_engine_session(url=Config.SQLALCHEMY_DATABASE_URI, echo=False):
    """
    Given a database URL, returns an SQLAlchemy engine/session
    """
    engine = _get_engine(url, echo=echo)
    session = scoped_session(sessionmaker(bind=engine, autoflush=True))
    return engine, session


db = SQLAlchemy()
