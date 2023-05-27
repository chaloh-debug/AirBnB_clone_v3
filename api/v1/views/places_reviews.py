#!/usr/bin/python3
""" places endpoints """
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import Flask, abort, make_response, jsonify, request


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """retrieve all review objects """
    review_place = []
    place = storage.get('Place', place_id)
    reviews = storage.all(Review)
    if not place or not reviews:
        abort(404)
    for review in reviews.values():
        if review.place_id == place_id:
            review_place.append(review.to_dict())
    return jsonify(review_place)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ retrieve a review based on id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete a review based on id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Misssing name")
    if "text" not in data:
        abort(400, "Missing text")
    users = storage.all(User)
    found = False
    for user in users.values():
        if user.id == data['user_id']:
            found = True
    if not found:
        abort(404)
    review = Review(**data)
    review.place_id = place.id
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ update a review based on id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        ignore_keys = ['id', 'place_id', 'user_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(review, k, v)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)
