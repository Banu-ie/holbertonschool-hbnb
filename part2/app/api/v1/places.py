from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title":       fields.String(required=True),
    "description": fields.String(required=False, default=""),
    "price":       fields.Float(required=True),
    "latitude":    fields.Float(required=True),
    "longitude":   fields.Float(required=True),
    "owner_id":    fields.String(required=True),
    "amenity_ids": fields.List(fields.String, required=False, default=[]),
})


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place created")
    @api.response(400, "Bad request")
    def post(self):
        """Create a new place"""
        data = dict(api.payload)
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "OK")
    def get(self):
        """Get all places"""
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in facade.get_all_places()
        ], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.response(200, "OK")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get a place by ID (includes owner and amenities)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200

    @api.expect(place_model, validate=False)
    @api.response(200, "Updated")
    @api.response(400, "Bad request")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """Update a place"""
        data = dict(api.payload)
        try:
            place = facade.update_place(place_id, data)
            if not place:
                api.abort(404, "Place not found")
            return place.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>/reviews")
class PlaceReviews(Resource):
    @api.response(200, "OK")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return [r.to_dict() for r in facade.get_reviews_by_place(place_id)], 200