from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self._validate_name(name)
        self.name = name

    def _validate_name(self, v):
        if not v or len(v) > 50:
            raise ValueError("name is required and max 50 chars")

    def update(self, data):
        if "name" in data: self._validate_name(data["name"])
        super().update(data)

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()}
