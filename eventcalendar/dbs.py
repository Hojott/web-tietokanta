""" Database functions """

from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import text
from sqlalchemy import inspect

class Database():
    """ API for the database """

    def __init__(self, app: Flask):
        """ ... """

        # Configure the app
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
        #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Create a SQLAlchemy object from the app
        self._conn = SQLAlchemy(app)

        # Check if all tables exist and create them
        self.__check_tables()

    def register_user(self, username: str, shown_name: str, password: str) -> None:
        """ Register a user, validating it and adding it to database """

        # self.__validate("username", username)
        # self.__validate("shown_name", shown_name)
        # self.__validate("password", password)

        password_hashed = password + "hash"

        self.__add_user(username, shown_name, password_hashed)


#======= Private functions =====#

    def __check_tables(self) -> None:
        """ Check if all tables exist and create any that don't """

        # Check through all the tables if they exist
        tables = {}
        for table in "users organizations favourite_organizations organization_admins types favourite_types events".split(" "):
            inspector = inspect(self._conn.engine)
            if inspector.has_table(table):
                tables[table] = True
                continue

            tables[table] = False

        # Create any tables that don't exist
        if not tables["users"]:
            sql = text("""--sql
                CREATE TABLE
                    users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        shown_name TEXT,
                        password TEXT
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["organizations"]:
            sql = text("""--sql
                CREATE TABLE
                    organizations (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        shown_name TEXT,
                        password TEXT
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["favourite_organizations"]:
            sql = text("""--sql
                CREATE TABLE
                    favourite_organizations (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER REFERENCES users,
                        organization_id INTEGER REFERENCES organizations
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["organization_admins"]:
            sql = text("""--sql
                CREATE TABLE
                    organization_admins (
                        id INTEGER PRIMARY KEY,
                        organization_id INTEGER REFERENCES organizations,
                        user_id INTEGER REFERENCES users
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["types"]:
            sql = text("""--sql
                CREATE TABLE
                    types (
                        id INTEGER PRIMARY KEY,
                        name TEXT
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["favourite_types"]:
            sql = text("""--sql
                CREATE TABLE
                    favourite_types (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER REFERENCES users,
                        type_id INTEGER REFERENCES types
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["events"]:
            sql = text("""--sql
                CREATE TABLE
                    events (
                        id INTEGER PRIMARY KEY,
                        organization_id INTEGER REFERENCES organizations,
                        start_date DATE,
                        end_date DATE,
                        place TEXT,
                        type TEXT,
                        price INTEGER,
                        in_charge INTEGER REFERENCES users
                    )
                ;
            """)
            self._conn.session.execute(sql)

    def __add_user(self, username: str, shown_name: str, hashed_password: str) -> None:
        """ Register a new user. ALWAYS hash password firsthand """

        sql = text("""--sql
            INSERT INTO
                users (username, shown_name, password)
            VALUES
                (:username, :shown_name, :password)
            ;   
        """)
        self._conn.execute(sql,
            {"username":username,
             "shown_name":shown_name,
             "password":hashed_password
            }
        )
