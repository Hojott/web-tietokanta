""" Flask app """

from flask import Flask
from flask_dotenv import DotEnv

from routes import load_routes
from dbs import Database

def run() -> None:
    """ Run the webserver """

    # Create the Flask object
    app = Flask("eventcalendar")

    # Load environment variables
    env = DotEnv(app)

    # Load the database using the application
    # Note app context is required
    with app.app_context():
        db = Database(app)

    # Load Flask routes, using the db and app
    load_routes(app, db)

    # Run server
    app.run(host="0.0.0.0", debug=True)
