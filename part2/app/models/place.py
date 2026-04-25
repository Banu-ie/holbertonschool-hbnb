class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner_id):
        super().__init__()

        if not title:
            raise ValueError("title required")

        if price <= 0:
            raise ValueError("price must be positive")

        if not (-90 <= latitude <= 90):
            raise ValueError("invalid latitude")

        if not (-180 <= longitude <= 180):
            raise ValueError("invalid longitude")

        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []
