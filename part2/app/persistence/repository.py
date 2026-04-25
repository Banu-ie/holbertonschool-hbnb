class InMemoryRepository:
    def __init__(self):
        self.data = {}

    def add(self, obj):
        self.data[obj["id"]] = obj

    def get(self, obj_id):
        return self.data.get(obj_id)

    def get_all(self):
        return list(self.data.values())

    def update(self, obj_id, new_data):
        if obj_id in self.data:
            self.data[obj_id].update(new_data)
            return self.data[obj_id]
        return None

    def delete(self, obj_id):
        return self.data.pop(obj_id, None)
