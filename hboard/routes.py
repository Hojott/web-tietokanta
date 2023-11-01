""" Flask routes """

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def load_routes(app: Flask, db: SQLAlchemy) -> None:
    """ Load all routes for the flask app """

    @app.route("/")
    def root():
        return render_template("frontpage.html")
