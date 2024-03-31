#!/usr/bin/python3
"""Starting a Flask Application"""
from flask import Flask, Response, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_session(exception):
    """close database session"""
    storage.close()


@app.errorhandler(404)
def page_not_foud(error) -> Response:
    """Page not found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    port = int(os.getenv("HBNB_API_PORT", 5000))
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    app.run(host=host, port=port, threaded=True)
