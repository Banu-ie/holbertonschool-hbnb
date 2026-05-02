from app import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:

    # ------------------------------------------------------------------ USERS
    def create_user(self, data):
        if User.query.filter_by(email=data.get('email')).first():
            raise ValueError('Email already registered')
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            is_admin=data.get('is_admin', False),
        )
        user.password = data['password']
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_all_users(self):
        return User.query.all()

    def update_user(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None
        if 'email' in data:
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise ValueError('Email already in use')
        if 'password' in data:
            user.password = data.pop('password')
        for key, value in data.items():
            if key not in ('id', 'created_at'):
                setattr(user, key, value)
        db.session.commit()
        return user

    # --------------------------------------------------------------- AMENITIES
    def create_amenity(self, data):
        amenity = Amenity(name=data['name'])
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity(self, amenity_id):
        return Amenity.query.get(amenity_id)

    def get_all_amenities(self):
        return Amenity.query.all()

    def update_amenity(self, amenity_id, data):
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            if key not in ('id', 'created_at'):
                setattr(amenity, key, value)
        db.session.commit()
        return amenity

    # ----------------------------------------------------------------- PLACES
    def create_place(self, data):
        owner = User.query.get(data.get('owner_id'))
        if not owner:
            raise ValueError('owner_id does not reference a valid user')
        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner_id=data['owner_id'],
        )
        db.session.add(place)
        db.session.commit()
        return place

    def get_place(self, place_id):
        return Place.query.get(place_id)

    def get_all_places(self):
        return Place.query.all()

    def update_place(self, place_id, data):
        place = Place.query.get(place_id)
        if not place:
            return None
        data.pop('owner_id', None)
        for key, value in data.items():
            if key not in ('id', 'created_at'):
                setattr(place, key, value)
        db.session.commit()
        return place

    def delete_place(self, place_id):
        place = Place.query.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
        return place

    # ---------------------------------------------------------------- REVIEWS
    def create_review(self, data):
        place = Place.query.get(data.get('place_id'))
        if not place:
            raise ValueError('place_id does not reference a valid place')
        review = Review(
            text=data['text'],
            rating=data['rating'],
            place_id=data['place_id'],
            user_id=data['user_id'],
        )
        db.session.add(review)
        db.session.commit()
        return review

    def get_review(self, review_id):
        return Review.query.get(review_id)

    def get_all_reviews(self):
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def get_review_by_user_and_place(self, user_id, place_id):
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()

    def update_review(self, review_id, data):
        review = Review.query.get(review_id)
        if not review:
            return None
        for key, value in data.items():
            if key not in ('id', 'created_at'):
                setattr(review, key, value)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
        return review


facade = HBnBFacade()
