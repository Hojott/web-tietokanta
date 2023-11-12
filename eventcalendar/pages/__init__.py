""" Pages """

from flask import render_template
from flask_classful import FlaskView

from wsgi import Webapp

# modules
from . import authorization

class HomeView(FlaskView):

    def __new__(self):
        self._app = Webapp

    def index(self) -> str:
        return render_template("frontpage.html")