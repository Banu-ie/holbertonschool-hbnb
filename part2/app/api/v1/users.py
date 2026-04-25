from flask_restx import Namespace, Resource, fields
import uuid
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# ---------- MODEL ----------
user_model = api.model('User', {
    'id': fields.String(readOnly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})


# ---------- ROUTES ----------
@api.route('/')
class UserList(Resource):

    @api.marshal_list_with(user_model)
    def get(self):
        return facade.get_all_users()

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = api.payload

        # validation
        required = ["first_name", "last_name", "email"]
        for field in required:
            if field not in data or not data[field]:
                return {"error": f"{field} is required"}, 400

        if "@" not in data["email"]:
            return {"error": "invalid email"}, 400

        # unique email
        for u in facade.get_all_users():
            if u["email"] == data["email"]:
                return {"error": "email already exists"}, 400

        user = {
            "id": str(uuid.uuid4()),
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "is_admin": False
        }

        return facade.create_user(user), 201


@api.route('/<user_id>')
class UserResource(Resource):

    @api.marshal_with(user_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if user:
            return user
        return {"error": "not found"}, 404

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        data = api.payload

        # email validation
        if "email" in data and "@" not in data["email"]:
            return {"error": "invalid email"}, 400

        updated = facade.update_user(user_id, data)
        if updated:
            return updated

        return {"error": "not found"}, 404