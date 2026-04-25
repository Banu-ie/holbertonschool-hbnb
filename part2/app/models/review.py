class Review(BaseModel):
    def __init__(self, text, user_id, place_id, rating):
        super().__init__()

        if not text:
            raise ValueError("text required")

        if not (1 <= rating <= 5):
            raise ValueError("rating must be 1-5")

        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
