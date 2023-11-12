""" WSGI app as a class """

from flask import Flask
from flask_classful import FlaskView
from flask_dotenv import DotEnv

from dbs import Database

class singleton(type):
    """ A singleton metaclass to avoid creating
        more than one webapp (and more importantly,
        database) (and yes, a bit overkill)"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Webapp(Flask, metaclass = singleton):
    """ The webapp """

    def __init__(self) -> None:

        # Create the Flask object
        super().__init__("eventcalendar")

        # Load environment variables
        DotEnv(self)

        # Load the database using the application
        # Note how app context is required
        with self.app_context():
            self._db = Database(self)

    def routes(self) -> list[FlaskView]:
        """ Load all views (routes) in app """
        print("not placeholder")

        # We're importing pages here to avoid circular imports
        import pages

        views: list[FlaskView] = [
            pages.HomeView,
            pages.authorization.RegisterView
        ]

        for View in views:
            View.register(self, route_base="/")

        return views

    def run(self, **kwargs) -> None:
        """ Wrapper for Flask.run() """

        # Load routes
        self.routes()

        # Run flask
        super().run(**kwargs)

    @property
    def db(self) -> Database:
        return self._db
