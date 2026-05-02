from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text     = db.Column(db.Text, nullable=False)
    rating   = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'),  nullable=False)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'text':     self.text,
            'rating':   self.rating,
            'place_id': self.place_id,
            'user_id':  self.user_id,
        })
        return base
