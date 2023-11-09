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
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
        #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Create a SQLAlchemy object from the app
        self._conn = SQLAlchemy(app)

        # Check if all tables exist and create them
        self.__check_tables()


    def register_user(self, username: str, shown_name: str, password: str) -> None:
        """ Register a user, validating it and adding it to database """

        # self.__validate(username=username)
        # self.__validate(shown_name=shown_name)
        # self.__validate(password=password)

        password_hashed = self.__hash(password)

        self.__add_user(username, shown_name, password_hashed)


    def modify_user(self, username: str, **kwargs: str) -> None:
        """ Modify an existing user """

        # self.__validate(username=username)
        # self.__validate(kwargs)

        for key, kwarg in kwargs.items():
            self.__update_user(username, commit=False, **{key: kwarg})

        self._conn.session.commit()


    def modify_password(self, username: str, password: str) -> None:
        """ Modify password of a user """

        # self.__validate(username=username)
        # self.__validate(password=password)

        password_hashed = self.__hash(password)

        self.__update_user(username, password=password_hashed)

    def test_credentials(self, username: str, password: str) -> bool:
        """ Try logging in """

        password_hashed = self.__hash(password)

        real_password = self.__get_user(username, data="password")

        print(password_hashed, real_password)

        if real_password == password_hashed:
            print("yeaahh")
            return True
        
        return False

#======= Private functions =====#

    def __check_tables(self) -> None:
        """ Check if all tables exist and create any that don't """

        # Check through all the tables if they exist
        tables = {}
        for table in [
            "users",
            "organizations",
            "favourite_organizations",
            "organization_admins",
            "types",
            "favourite_types",
            "events"
        ]:

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
                        id SERIAL PRIMARY KEY,
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
                        id SERIAL PRIMARY KEY,
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
                        id SERIAL PRIMARY KEY,
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
                        id SERIAL PRIMARY KEY,
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
                        id SERIAL PRIMARY KEY,
                        name TEXT
                    )
                ;
            """)
            self._conn.session.execute(sql)

        if not tables["favourite_types"]:
            sql = text("""--sql
                CREATE TABLE
                    favourite_types (
                        id SERIAL PRIMARY KEY,
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
                        id SERIAL PRIMARY KEY,
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

        # Commit if any tables were added
        if False in tables:
            self._conn.session.commit()


    def __add_user(self, username: str, shown_name: str, hashed_password: str) -> None:
        """ Register a new user. ALWAYS hash password firsthand """

        args = {
            "username":username,
            "shown_name":shown_name,
            "password":hashed_password
        }

        sql = text("""--sql
            INSERT INTO
                users (username, shown_name, password)
            VALUES
                (:username, :shown_name, :password)
            ;   
        """)

        self._conn.session.execute(sql, args)
        self._conn.session.commit()


    def __update_user(self, username: str, commit: bool = True, **kwarg: str) -> None:
        """ Modify an existing user """

        args = {
            "username": username,
            "name": kwarg.keys()[0],
            "value": kwarg[0]
        }

        sql = text("""--sql
            UPDATE TABLE
                users (:name)
            VALUES
                :value
            WHERE
                username = :username
            ;
        """)

        self._conn.session.execute(sql, args)

        # For cases when we want to commit at the end only
        if commit:
            self._conn.session.commit()

    def __get_user(self, username: str, data: str|list[str]) -> str|dict[str:str]:
        """ Get different data by username """

        args = {
            "username": username
        }

        sql = text("""--sql
            SELECT
                *
            FROM
                users
            WHERE
                username = :username
            ;
        """)

        result = self._conn.session.execute(sql, args)

        # Get neccessary data from result
        if isinstance(data, str):
            for column, value in zip(result.keys(), result.fetchone()):
                if column == data:

                    return value

        if isinstance(data, list):
            wanted_result = {}
            for column in zip(result.keys(), result.fetchone()):
                if column in data:
                    wanted_result[column] = value

            return wanted_result
    
    def __list_users(self) -> list[str]:
        """ List all users """

    def __hash(self, password: str) -> str:
        """ Hash and salt given password """

        hashed = password + "hash"

        return hashed
    
    def __validate(self, **kwargs) -> bool:
        """ Validate stuff """