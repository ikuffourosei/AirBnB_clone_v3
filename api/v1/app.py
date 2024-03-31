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
    port = next((int(arg.split('=')[1])
                 for arg in argv if 'HBNB_API_PORT' in arg), 5000)
    host = next((arg.split('=')[1] for arg in argv if 'HBNB_API_HOST' in arg),
                '0.0.0.0')
    app.run(host=host, port=port, threaded=True)
