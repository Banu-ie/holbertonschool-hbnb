from models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, user_id, place_id):
        super().__init__()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
