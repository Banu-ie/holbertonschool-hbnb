from flask import Blueprint, request, jsonify
from app.services.facade import facade

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    return jsonify([r.to_dict() for r in facade.get_all_reviews()]), 200

@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/places/<place_id>', methods=['GET'])
def get_reviews_by_place(place_id):
    if not facade.get_place(place_id):
        return jsonify({'error': 'Place not found'}), 404
    return jsonify([r.to_dict() for r in facade.get_reviews_by_place(place_id)]), 200

@reviews_bp.route('/', methods=['POST'])
def create_review():
    data = request.get_json(silent=True) or {}
    required = ('place_id', 'text', 'rating', 'user_id')
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    try:
        review = facade.create_review(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(review.to_dict()), 201

@reviews_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json(silent=True) or {}
    review = facade.update_review(review_id, data)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = facade.delete_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify({'message': 'Review deleted'}), 200
