import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password="", is_admin=False):
        super().__init__()
        self._validate_first_name(first_name)
        self._validate_last_name(last_name)
        self._validate_email(email)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def _validate_first_name(self, v):
        if not v or len(v) > 50:
            raise ValueError("first_name is required and max 50 chars")

    def _validate_last_name(self, v):
        if not v or len(v) > 50:
            raise ValueError("last_name is required and max 50 chars")

    def _validate_email(self, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")

    def update(self, data):
        if "first_name" in data: self._validate_first_name(data["first_name"])
        if "last_name" in data: self._validate_last_name(data["last_name"])
        if "email" in data: self._validate_email(data["email"])
        super().update(data)

    def to_dict(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "is_admin": self.is_admin,
                "created_at": self.created_at.isoformat(), "updated_at": self.updated_at.isoformat()}
