""" Flask routes """

from flask import Flask, render_template, redirect, request, Response
from flask.cli import with_appcontext
from dbs import Database

#@with_appcontext
def load_routes(app: Flask, db: Database) -> None:
    """ Load all routes for the flask app """

    @app.route("/home", methods=["GET"])
    def home():
        """ Frontpage """
        return render_template("frontpage.html")

    @app.route("/calendar", methods=["GET"])
    def calendar():
        """ Calendar page """

    @app.route("/user/<name>", methods=["GET"])
    def user_profile(username: str):
        """ User profile page """

    @app.route("/org/<name>", methods=["GET"])
    def org_profile(orgname: str):
        """ Organization profile page """

    @app.route("/event/<int:post_id>", methods=["GET", "POST"])
    def event(post_id: int):
        """ Event page """

    @app.route("/register")
    def register_empty() -> Response:
        return redirect("/register/user")

    @app.route("/register/<rtype>", methods=["GET", "POST"])
    def register(rtype: str) -> str:
        """ Register user / organization """


        if rtype == "user" or rtype == "":

            if request.method == "GET":
                return render_template("register_user.html")

            if request.method == "POST":
                db.register_user(
                    request.form["username"],
                    request.form["shown_name"],
                    request.form["password"]
                )

                return login()

        elif rtype == "organization":

            if request.method == "GET":
                return render_template("register_organization.html")

            if request.method == "POST":
                db.register_organization(
                    request.form["username"],
                    request.form["shown_name"],
                    request.form["password"]
                )

                return login()

        else:
            return "You spelled organzation wrong"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """ Login user/org """

        if request.method == "GET":
            return render_template("login.html")
        
        if request.method == "POST":
            login = db.test_credentials(
                request.form["username"],
                request.form["password"]
            )

            if login:
                # some cookie stuff
                return "Willkommen!"
            else:
                return "Invalid username or password"
