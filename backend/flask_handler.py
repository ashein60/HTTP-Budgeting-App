from flask import Flask

app = Flask(__name__)


def get_database_path():
    return app.config["DATABASE"]


def set_database_path(path):
    app.config["DATABASE"] = path


set_database_path("database.db")
