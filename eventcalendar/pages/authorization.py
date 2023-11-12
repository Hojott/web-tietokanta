""" Different authorization pages """

from flask import render_template, redirect, request, session, Response
from flask_classful import FlaskView

from wsgi import Webapp

class RegisterView(FlaskView):
    """ View for registeration """

    def __new__(self):
        self._app = Webapp

    def index(self):
        return render_template("register_user.html")

    def post(self):
        if request.form["password"] == request.form["password_again"]:
            self._app.db.register_user(
                request.form["username"],
                request.form["shown_name"],
                request.form["password"]
            )

            return redirect("/login")
        
        else:
            return "Passwords do not match!"
    