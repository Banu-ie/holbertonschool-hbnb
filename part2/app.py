from flask import Flask, request
import uuid

app = Flask(__name__)

users_data = []
amenities_data = []
places_data = []
reviews_data = []

@app.route("/")
def home():
    return "API is working"

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.json
        data["id"] = str(uuid.uuid4())
        users_data.append(data)
        return data, 201

    return users_data

@app.route("/users/<user_id>")
def get_user(user_id):
    for user in users_data:
        if user["id"] == user_id:
            return user
    return {"error": "not found"}, 404

@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json

    for user in users_data:
        if user["id"] == user_id:
            user.update(data)
            return user

    return {"error": "not found"}, 404

@app.route("/amenities", methods=["GET", "POST"])
def amenities():
    if request.method == "POST":
        data = request.json
        data["id"] = str(uuid.uuid4())
        amenities_data.append(data)
        return data, 201

    return amenities_data


@app.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    for amenity in amenities_data:
        if amenity["id"] == amenity_id:
            return amenity
    return {"error": "not found"}, 404


@app.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    data = request.json

    for amenity in amenities_data:
        if amenity["id"] == amenity_id:
            amenity.update(data)
            return amenity

    return {"error": "not found"}, 404

@app.route("/places", methods=["GET", "POST"])
@app.route("/places", methods=["GET", "POST"])
def places():
    if request.method == "POST":
        data = request.json

        required = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in required:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        # если нет amenities — создаём пустой список
        if "amenities" not in data:
            data["amenities"] = []

        data["id"] = str(uuid.uuid4())
        places_data.append(data)
        return data, 201

    return places_data


@app.route("/places/<place_id>")
def get_place(place_id):
    for place in places_data:
        if place["id"] == place_id:
            return place
    return {"error": "not found"}, 404


@app.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    data = request.json

    for place in places_data:
        if place["id"] == place_id:
            place.update(data)
            return place

    return {"error": "not found"}, 404

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


@app.route("/reviews/<review_id>")
def get_review(review_id):
    for review in reviews_data:
        if review["id"] == review_id:
            return review
    return {"error": "not found"}, 404


@app.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    data = request.json

    for review in reviews_data:
        if review["id"] == review_id:
            review.update(data)
            return review

    return {"error": "not found"}, 404


@app.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    for review in reviews_data:
        if review["id"] == review_id:
            reviews_data.remove(review)
            return {"message": "deleted"}

    return {"error": "not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)
