"""
Author:     David Walshe
Date:       28 June 2020
"""

from sys import stderr
from os import environ

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.utils.singleton import Singleton

Base = declarative_base()


class ConnectionManager(metaclass=Singleton):
    """
    Helper class to manage database resources.
    """
    _engine = None
    Session = None
    _Base = None
    db_path = None

    @classmethod
    def init(cls):
        """
        If the database has not been previously setup then initialise the database and create a Session and Base object
        to connect to it with.

        Initialisation only takes place if "ConnectionManager._engine" is None, otherwise nothing happens.
        """
        if cls._engine is None:
            cls.db_path = environ["RA_DB_PATH"]
            cls._engine = create_engine(f"sqlite:///{cls.db_path}")
            cls.Session = sessionmaker(bind=cls._engine, expire_on_commit=False)
            cls._Base = declarative_base()

    @classmethod
    def engine(cls):
        """
        Return the engine for the database.

        :return: The database engine object.
        """
        cls.init()

        return cls._engine

    @classmethod
    def base(cls):
        """
        Returns the view-model for the database.

        :return: The declarative Base object.
        """
        cls.init()

        return cls._Base

    @classmethod
    def meta_data(cls):
        """
        Returns the database metadata.

        :return: The metadata for the DB.
        """
        cls.init()

        return cls.base().metadata

    @classmethod
    @contextmanager
    def session_scope(cls):
        """
        Provide a transactional scope around a series of operations
        """
        cls.init()

        session = cls.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.flush()
            session.close()
