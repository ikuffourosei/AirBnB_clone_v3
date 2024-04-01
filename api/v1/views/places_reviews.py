#!/usr/bin/python3
"""View for place_review objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def view_place_reviews(place_id):
    """Returns a list containing all Review objects from a particular place"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            reviews = []
            for review in storage.all(Review).values():
                if review.place_id == place_id:
                    reviews.append(review.to_dict())
            return jsonify(reviews)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new review object"""
    try:
        rd = request.get_json(silent=True)  # review data
        if not rd:
            raise ValueError("Not a JSON")
    except ValueError as e:
        raise abort(400, description=str(e))
    for place in storage.all(Place).values():
        if place.id == place_id:
            if 'user_id' not in rd:
                raise abort(400, description="Missing user_id")
            for user in storage.all(User).values():
                if user.id == rd['user_id']:
                    if 'text' not in rd:
                        raise abort(400, description="Missing text")
                    new_review = Review(place_id=place_id, **rd)
                    new_review.save()
                    return jsonify(new_review.to_dict()), 201
            abort(404)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def view_review(review_id):
    """Returns the review with id 'review_id'"""
    for review in storage.all(Review).values():
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT', 'PATCH'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates the review with id 'review_id'"""
    try:
        rd = request.get_json(silent=True)  # review data
        if not rd:
            raise ValueError("Not a JSON")
    except ValueError as e:
        raise abort(400, description=str(e))
    for review in storage.all(Review).values():
        if review.id == review_id:
            ignore = ['created_at', 'place_id', 'updated_at', 'user_id']
            for k, v in rd.items():
                if k not in ignore:
                    setattr(review, k, v)
            review.save()
            return jsonify(review.to_dict()), 200
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes the review with id 'review_id'"""
    for review in storage.all(Review).values():
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    abort(404)
