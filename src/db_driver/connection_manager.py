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

Base = declarative_base()


class Singleton(type):
    """
    Singleton design pattern used to limit possible database instances to one.
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        """
        Returns a new or existing class object depending on whether or not it was created previously.

        :return: The requested objects sole instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class ConnectionManager(metaclass=Singleton):
    """
    Helper class to manage database resources.
    """
    _engine = None
    Session = None
    _Base = None
    db_path = environ["RA_DB_LOCATION"]

    @classmethod
    def init(cls):
        """
        If the database has not been previously setup then initialise the database and create a Session and Base object
        to connect to it with.

        Initialisation only takes place if "ConnectionManager._engine" is None, otherwise nothing happens.
        """
        if cls._engine is None:
            print(f"config (BAD): {ConnectionManager.db_path}")
            if ConnectionManager.db_path is not None:
                pass
            elif environ.get("RA_DB_PATH", None) is None:
                print("Using in-memory database", file=stderr)
                ConnectionManager.db_path =  ":memory:"
                # raise ValueError("Database path was not set")
            elif ConnectionManager.db_path == ":memory:":
                pass

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
        Returns the base-model for the database.

        :return: The declarative Base object.
        """
        cls.init()

        return cls._Base

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
