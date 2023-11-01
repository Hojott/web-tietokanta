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
    """ Checks if tables exist and creates them if they don't """

    try:
        db.session.execute("SELECT * FROM users")

    except RuntimeError:
        create_tables(db)

def create_tables(db: SQLAlchemy) -> None:
    """ Create necessary tables """

    
