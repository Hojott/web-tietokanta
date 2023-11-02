""" Flask routes """

from flask import Flask, render_template, request
from dbs import Database # pylint: disable=import-error

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

    @app.route("/register/<type>", methods=["GET", "POST"])
    def register(type: str) -> str:
        """ Register user / organization """

        if request.method == "POST":

            if type == "user":
                db.register_user(
                    request.form["username"],
                    request.form["shown_name"],
                    request.form["password"]
                )

            elif type == "organization":
                db.register_organization(
                    request.form["username"],
                    request.form["shown_name"],
                    request.form["password"]
                )

            else:
                return "You spelled organazation wrong"

            return login()

        if request.method == "GET":
            return "Email sakari.marttinen@helsinki.fi for account"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """ Login user/org """

        return "Please log in to see this page"
