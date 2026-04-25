class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()

        if not first_name or not last_name:
            raise ValueError("Name fields required")

        if "@" not in email:
            raise ValueError("Invalid email")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False
