""" Flask app """

from flask import Flask

from routes import load_routes # pylint: disable=import-error
from dbs import load_db

def run() -> None:
    """ Run the webserver """

    # Create the Flask object
    app = Flask("hboard")

    # Load the database using the application
    db = load_db(app)

    # Load Flask routes, using the db and app
    load_routes(app, db)

    # Run server
    app.run(host="0.0.0.0", debug=True)
