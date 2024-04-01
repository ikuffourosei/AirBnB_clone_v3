#!/usr/bin/python3
"""Blueprint of views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route('/status', methods=['GET'])
def index():
    '''returns a JSON: "status": "OK" '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_status():
    """an endpoint that retrieves the number of each objects by type:"""
    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }

    return jsonify(data)
