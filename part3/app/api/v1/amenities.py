from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/', methods=['GET'])
def get_amenities():
    return jsonify([a.to_dict() for a in facade.get_all_amenities()]), 200

@amenities_bp.route('/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = facade.get_amenity(amenity_id)
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict()), 200

@amenities_bp.route('/', methods=['POST'])
@jwt_required()
def create_amenity():
    claims = get_jwt()
    if not claims.get('is_admin', False):
        return jsonify({'error': 'Admin privileges required'}), 403
    data = request.get_json(silent=True) or {}
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    try:
        amenity = facade.create_amenity(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    return jsonify(amenity.to_dict()), 201

@amenities_bp.route('/<amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin', False):
        return jsonify({'error': 'Admin privileges required'}), 403
    data = request.get_json(silent=True) or {}
    amenity = facade.update_amenity(amenity_id, data)
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict()), 200
