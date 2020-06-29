"""
Author:     David Walshe
Date:       28 June 2020
"""

import functools

from src.db_driver.connection_manager import ConnectionManager, Singleton


def sqlite_session(func: callable) -> callable:
    """
    Decorator to inject a ORM session into common operations.

    :param func: The function to decorate.
    :return: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        with ConnectionManager.session_scope() as session:
            return_value = func(session, *args, **kwargs)

        return return_value

    return wrapper


class DBManager(metaclass=Singleton):

    def __init__(self, db_path: str = ":memory:"):
        """
        Managers the database resource and allows CRUD operations.
        """
        ConnectionManager.db_path = db_path
        ConnectionManager.base().metadata.create_all(bind=ConnectionManager.engine())

    @staticmethod
    @sqlite_session
    def create(session, table_cls, data: dict = None) -> None:
        """
        Creates the passed table class in the SQLite table.

        :param session: The ORM session object.
        :param table_cls: The class to use for the table creation.
        :param data: The data to fill the table with.
        """
        table = table_cls()
        table.insert_from_dict(data)
        session.add(table)

    @staticmethod
    @sqlite_session
    def query(session, table, **kwargs: dict) -> tuple:
        """
        Requests data from the database following some search criteria provided by kwargs.

        Similar to a "SELECT * FROM $TABLE$ WHERE {**kwargs}" in SQL.

        :param session: The ORM session object.
        :param table: The table object to query.
        :param kwargs: The search criteria for the WHERE clause.
        :return: A list of row items that match the search criteria.
        """
        return session.query(table).filter_by(**kwargs).all()

    @staticmethod
    @sqlite_session
    def update(session, item) -> None:
        """
        Updates a passed item in the database.

        :param session: The ORM session object.
        :param item: The item to update.
        """
        session.add(item)

    @staticmethod
    @sqlite_session
    def all(session, table_cls) -> tuple:
        """
        Helpere to return all items from a specified database.

        :param session: The ORM session object.
        :param table_cls: The class to use for the table creation.
        :return: All of th entries of that table.
        """
        return session.query(table_cls).all()
