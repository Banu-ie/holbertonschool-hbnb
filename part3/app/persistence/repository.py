from app import db


class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def get_by_attribute(self, attr, value):
        return self.model.query.filter(
            getattr(self.model, attr) == value
        ).first()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if key not in ('id', 'created_at'):
                setattr(obj, key, value)
        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
        return obj


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.user import User
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.get_by_attribute('email', email)


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.place import Place
        super().__init__(Place)


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.review import Review
        super().__init__(Review)

    def get_by_user_and_place(self, user_id, place_id):
        from app.models.review import Review
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()

    def get_by_place(self, place_id):
        from app.models.review import Review
        return Review.query.filter_by(place_id=place_id).all()


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        from app.models.amenity import Amenity
        super().__init__(Amenity)
