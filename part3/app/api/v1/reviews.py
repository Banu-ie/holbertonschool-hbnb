from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    data['user_id'] = current_user_id
    required = ('place_id', 'text', 'rating')
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    place = facade.get_place(data['place_id'])
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    if place.owner_id == current_user_id:
        return jsonify({'error': 'You cannot review your own place'}), 400
    existing = facade.get_review_by_user_and_place(current_user_id, data['place_id'])
    if existing:
        return jsonify({'error': 'You have already reviewed this place'}), 400
    try:
        review = facade.create_review(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(review.to_dict()), 201

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    if not is_admin and review.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    data = request.get_json(silent=True) or {}
    review = facade.update_review(review_id, data)
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    review = facade.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    if not is_admin and review.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    facade.delete_review(review_id)
    return jsonify({'message': 'Review deleted'}), 200
