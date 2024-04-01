#!/usr/bin/python3
"""An API for retrieving Place data"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User
import models


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        place = [items.to_dict() for items in city.places]
        return jsonify(place)
    elif request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(404, description='Not a JSON')
        if 'name' not in request.json:
            abort(404, description='Missing name')
        if 'user_id' not in request.json:
            abort(404, description='Missing user_id')
        new_place = Place(**body_request)
        user_id = body_request.get('user_id')
        user = models.storage.get(User, user_id)
        if user is None:
            abort(404)
        models.storage.new(new_place)
        models.storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_modify(place_id):
    """Retrieve place data with place_id """
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        models.storage.delete(place)
        models.storage.save()
        return jsonify('{}'), 200
    elif request.method == 'PUT':
        body_request = request.json
        if not body_request:
            abort(404, description='Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, val in body_request:
            if key not in ignore:
                setattr(place, key, val)
        models.storage.save()
        return jsonify(place.to_dict())
