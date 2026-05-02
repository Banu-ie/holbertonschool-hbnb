from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self._validate_text(text)
        self._validate_rating(rating)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def _validate_text(self, v):
        if not v:
            raise ValueError("text is required")

    def _validate_rating(self, v):
        if not isinstance(v, int) or not (1 <= v <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

    def update(self, data):
        if "text" in data: self._validate_text(data["text"])
        if "rating" in data: self._validate_rating(data["rating"])
        super().update(data)

    def to_dict(self):
        return {"id": self.id, "text": self.text, "rating": self.rating,
                "place_id": self.place.id, "user_id": self.user.id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()}
