from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo     = InMemoryRepository()
        self.amenity_repo  = InMemoryRepository()
        self.place_repo    = InMemoryRepository()
        self.review_repo   = InMemoryRepository()

    # ------------------------------------------------------------------ USERS
    def create_user(self, data):
        if self.user_repo.get_by_attribute("email", data.get("email")):
            raise ValueError("Email already registered")
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        # prevent email collision on update
        new_email = data.get("email")
        if new_email and new_email != user.email:
            if self.user_repo.get_by_attribute("email", new_email):
                raise ValueError("Email already registered")
        user.update(data)
        return user

    # --------------------------------------------------------------- AMENITIES
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    # ----------------------------------------------------------------- PLACES
    def create_place(self, data):
        owner = self.user_repo.get(data.get("owner_id"))
        if not owner:
            raise ValueError("owner_id does not reference a valid user")

        amenity_ids = data.pop("amenity_ids", [])
        data.pop("owner_id")

        place = Place(owner=owner, **data)

        for aid in amenity_ids:
            amenity = self.amenity_repo.get(aid)
            if not amenity:
                raise ValueError(f"Amenity {aid} not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # don't let caller overwrite owner/amenities via plain update
        data.pop("owner_id", None)
        data.pop("amenity_ids", None)
        place.update(data)
        return place

    # ---------------------------------------------------------------- REVIEWS
    def create_review(self, data):
        user  = self.user_repo.get(data.get("user_id"))
        place = self.place_repo.get(data.get("place_id"))
        if not user:
            raise ValueError("user_id does not reference a valid user")
        if not place:
            raise ValueError("place_id does not reference a valid place")

        review = Review(
            text=data["text"],
            rating=data["rating"],
            place=place,
            user=user,
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.update(data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        # remove from place.reviews too
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        return self.review_repo.delete(review_id)


# Singleton — import this everywhere
facade = HBnBFacade()
