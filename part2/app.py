from flask import Flask, request
import uuid

app = Flask(__name__)

# In-memory storage
users_data = []
amenities_data = []
places_data = []
reviews_data = []


# -------------------- HOME --------------------
@app.route("/")
def home():
    return "API is working"


# -------------------- USERS --------------------
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.json

        if "name" not in data:
            return {"error": "name is required"}, 400

        data["id"] = str(uuid.uuid4())
        users_data.append(data)
        return data, 201

    return users_data


@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user_detail(user_id):
    for user in users_data:
        if user["id"] == user_id:

            if request.method == "GET":
                return user

            if request.method == "PUT":
                data = request.json
                user.update(data)
                return user

            if request.method == "DELETE":
                users_data.remove(user)
                return {"message": "deleted"}

    return {"error": "not found"}, 404


# -------------------- AMENITIES --------------------
@app.route("/amenities", methods=["GET", "POST"])
def amenities():
    if request.method == "POST":
        data = request.json

        if "name" not in data:
            return {"error": "name is required"}, 400

        data["id"] = str(uuid.uuid4())
        amenities_data.append(data)
        return data, 201

    return amenities_data


@app.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"])
def amenity_detail(amenity_id):
    for amenity in amenities_data:
        if amenity["id"] == amenity_id:

            if request.method == "GET":
                return amenity

            if request.method == "PUT":
                data = request.json
                amenity.update(data)
                return amenity

            if request.method == "DELETE":
                amenities_data.remove(amenity)
                return {"message": "deleted"}

    return {"error": "not found"}, 404


# -------------------- PLACES --------------------
@app.route("/places", methods=["GET", "POST"])
def places():
    if request.method == "POST":
        data = request.json

        required = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in required:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        if "amenities" not in data:
            data["amenities"] = []

        data["id"] = str(uuid.uuid4())
        places_data.append(data)
        return data, 201

    return places_data


@app.route("/places/<place_id>", methods=["GET", "PUT", "DELETE"])
def place_detail(place_id):
    for place in places_data:
        if place["id"] == place_id:

            if request.method == "GET":
                return place

            if request.method == "PUT":
                data = request.json
                place.update(data)
                return place

            if request.method == "DELETE":
                places_data.remove(place)
                return {"message": "deleted"}

    return {"error": "not found"}, 404


# -------------------- REVIEWS --------------------
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        data = request.json

        required = ["text", "user_id", "place_id"]
        for field in required:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        data["id"] = str(uuid.uuid4())
        reviews_data.append(data)
        return data, 201

    return reviews_data


@app.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def review_detail(review_id):
    for review in reviews_data:
        if review["id"] == review_id:

            if request.method == "GET":
                return review

            if request.method == "PUT":
                data = request.json
                review.update(data)
                return review

            if request.method == "DELETE":
                reviews_data.remove(review)
                return {"message": "deleted"}

    return {"error": "not found"}, 404


# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
