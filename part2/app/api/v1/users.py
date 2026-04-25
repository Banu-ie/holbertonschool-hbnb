from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "first_name": fields.String(required=True),
    "last_name":  fields.String(required=True),
    "email":      fields.String(required=True),
    "password":   fields.String(required=False),
})


@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User created")
    @api.response(400, "Bad request")
    def post(self):
        """Create a new user"""
        data = api.payload
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "OK")
    def get(self):
        """Get all users"""
        return [u.to_dict() for u in facade.get_all_users()], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.response(200, "OK")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict(), 200

    @api.expect(user_model, validate=False)
    @api.response(200, "Updated")
    @api.response(400, "Bad request")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update a user"""
        data = api.payload
        try:
            user = facade.update_user(user_id, data)
            if not user:
                api.abort(404, "User not found")
            return user.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))