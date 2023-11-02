""" Database functions """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def load_db(app: Flask) -> SQLAlchemy:
    """ Load database info """

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hboard"
    db = SQLAlchemy(app)

    check_tables(db)

    return db

def check_tables(db: SQLAlchemy) -> None:
    """ Check if all tables exist and create any that don't """

    try:
        db.session.execute("SELECT * FROM users")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    shown_name TEXT.
                    password PASSWORD
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM organizations")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                organizations (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    shown_name TEXT,
                    password PASSWORD
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM favourite_organizations")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                favourite_organizations (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES users,
                    organization_id INTEGER REFERENCES organizations
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM organization_admins")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                organization_admins (
                    id INTEGER PRIMARY KEY,
                    organization_id INTEGER REFERENCES organizations,
                    user_id INTEGER REFERENCES users
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM types")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                types (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM favourite_types")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                favourite_types (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES users,
                    type_id INTEGER REFERENCES types
                )
            ;
        """)

    try:
        db.session.execute("SELECT * FROM events")
    except RuntimeError:
        db.session.execute("""--sql
            CREATE TABLE
                events (
                    id INTEGER PRIMARY KEY,
                    organization_id INTEGER REFERENCES oraganizations,
                    start_date DATETIME,
                    end_date DATETIME,
                    place TEXT,
                    type TEXT,
                    price INTEGER,
                    in_charge INTEGER REFERENCES users
                )
            ;
        """)
