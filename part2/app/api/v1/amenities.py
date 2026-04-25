from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True),
})


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity created")
    @api.response(400, "Bad request")
    def post(self):
        """Create a new amenity"""
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "OK")
    def get(self):
        """Get all amenities"""
        return [a.to_dict() for a in facade.get_all_amenities()], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "OK")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=False)
    @api.response(200, "Updated")
    @api.response(400, "Bad request")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            amenity = facade.update_amenity(amenity_id, api.payload)
            if not amenity:
                api.abort(404, "Amenity not found")
            return amenity.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))