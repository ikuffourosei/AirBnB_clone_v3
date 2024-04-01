#!/usr/bin/python3
"""An API for retrieving Place data"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User
import models


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [items.to_dict() for items in city.places]
    return jsonify(places)


@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_modify(place_id):
    """Retrieve place data with place_id """
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place data"""
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)
    models.storage.delete(place)
    models.storage.save()
    return jsonify('{}'), 200


@app_views.route('cities/<city_id>/places')
def create_place(city_id):
    """Creates a place data"""
    body_request = request.get_json()
    if not body_request:
        abort(404, description='Not a JSON')
    if 'name' not in request.json:
        abort(404, description='Missing name')
    if 'user_id' not in request.json:
        abort(404, description='Missing user_id')
    user_id = body_request.get('user_id')
    user = models.storage.get(User, user_id)
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **body_request)
    models.storage.new(new_place)
    models.storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates place with data for a given place_id"""
    place = models.storage.get(Place, place_id)
    body_request = request.json
    if not body_request:
        abort(404, description='Not a JSON')
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in body_request:
        if key not in ignore:
            setattr(place, key, val)
    models.storage.save()
    return jsonify(place.to_dict())