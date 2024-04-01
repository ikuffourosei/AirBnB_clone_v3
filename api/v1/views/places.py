#!/usr/bin/python3
"""An API for retrieving Place data"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
import models


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    elif request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, description='Not a JSON')
        if 'name' not in body_request or 'user_id' not in body_request:
            abort(400, description='Missing name or user_id')
        user_id = body_request['user_id']
        user = models.storage.get(User, user_id)
        if user is None:
            abort(404)
        new_place = Place(city_id=city_id, **body_request)
        models.storage.new(new_place)
        models.storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_modify(place_id):
    """Retrieve, delete, or update a Place object by id"""
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        models.storage.delete(place)
        models.storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        body_request = request.get_json()
        if not body_request:
            abort(400, description='Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, val in body_request.items():
            if key not in ignore:
                setattr(place, key, val)
        models.storage.save()
        return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on criteria in request body"""
    body_request = request.get_json()
    if not body_request:
        abort(400, description='Not a JSON')

    states = body_request.get('states', [])
    cities = body_request.get('cities', [])
    amenities = body_request.get('amenities', [])

    places = []
    if not states and not cities:
        places = models.storage.all(Place).values()
    else:
        for state_id in states:
            state = models.storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city.id not in cities:
                        cities.append(city.id)

        for city_id in cities:
            city = models.storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities:
        places = [place for place in places if all(amenity_id
                                                   in place.amenities
                                                   for amenity_id in
                                                   amenities)]

    places_dict = [place.to_dict() for place in places]
    return jsonify(places_dict)
