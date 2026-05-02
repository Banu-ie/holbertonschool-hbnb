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
