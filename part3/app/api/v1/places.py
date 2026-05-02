from flask import Blueprint, request, jsonify
from app.services.facade import facade

places_bp = Blueprint('places', __name__)

@places_bp.route('/', methods=['GET'])
def get_places():
    return jsonify([p.to_dict() for p in facade.get_all_places()]), 200

@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    place = facade.get_place(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(place.to_dict()), 200

@places_bp.route('/', methods=['POST'])
def create_place():
    data = request.get_json(silent=True) or {}
    required = ('title', 'price', 'latitude', 'longitude', 'owner_id')
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    try:
        place = facade.create_place(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(place.to_dict()), 201

@places_bp.route('/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json(silent=True) or {}
    place = facade.update_place(place_id, data)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(place.to_dict()), 200
