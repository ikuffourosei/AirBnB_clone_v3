#!/usr/bin/python3
"""Starting a Flask Application"""
from sys import argv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """close database session"""
    storage.close()


if __name__ == "__main__":
    port = 5000
    host = '0.0.0.0'
    for items in argv:
        if "HBNB_API_PORT" in items:
            result = items.split('=')
            port = eval(result[1])
        if "HBNB_API_HOST" in items:
            result = items.split('=')
            host = str(result[1])
    app.run(host=host, port=port, threaded=True)
