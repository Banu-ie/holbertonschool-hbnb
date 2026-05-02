from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        base = super().to_dict()
        base.update({'name': self.name})
        return base
