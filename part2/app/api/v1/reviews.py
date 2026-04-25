from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text":     fields.String(required=True),
    "rating":   fields.Integer(required=True),
    "user_id":  fields.String(required=True),
    "place_id": fields.String(required=True),
})


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review created")
    @api.response(400, "Bad request")
    def post(self):
        """Create a new review"""
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "OK")
    def get(self):
        """Get all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    @api.response(200, "OK")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.expect(review_model, validate=False)
    @api.response(200, "Updated")
    @api.response(400, "Bad request")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update a review"""
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, "Review not found")
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "Deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        result = facade.delete_review(review_id)
        if not result:
            api.abort(404, "Review not found")
        return {"message": "Review deleted successfully"}, 200