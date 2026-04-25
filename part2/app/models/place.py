from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._validate_title(title)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)
        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.amenities = []
        self.reviews = []

    def _validate_title(self, v):
        if not v or len(v) > 100:
            raise ValueError("title is required and max 100 chars")

    def _validate_price(self, v):
        if float(v) < 0:
            raise ValueError("price must be non-negative")

    def _validate_latitude(self, v):
        if not (-90.0 <= float(v) <= 90.0):
            raise ValueError("latitude must be between -90 and 90")

    def _validate_longitude(self, v):
        if not (-180.0 <= float(v) <= 180.0):
            raise ValueError("longitude must be between -180 and 180")

    def update(self, data):
        if "title" in data: self._validate_title(data["title"])
        if "price" in data: self._validate_price(data["price"])
        if "latitude" in data: self._validate_latitude(data["latitude"])
        if "longitude" in data: self._validate_longitude(data["longitude"])
        super().update(data)

    def add_amenity(self, amenity):
        if amenity not in self.amenities: self.amenities.append(amenity)

    def add_review(self, review):
        if review not in self.reviews: self.reviews.append(review)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description,
                "price": self.price, "latitude": self.latitude, "longitude": self.longitude,
                "owner": self.owner.to_dict(), "amenities": [a.to_dict() for a in self.amenities],
                "created_at": self.created_at.isoformat(), "updated_at": self.updated_at.isoformat()}
