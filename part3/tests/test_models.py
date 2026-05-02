import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class TestBaseModel(unittest.TestCase):
    def test_id_is_string(self):
        u = User("Alice", "Smith", "alice@example.com")
        self.assertIsInstance(u.id, str)
    def test_ids_are_unique(self):
        u1 = User("A", "B", "a@b.com")
        u2 = User("C", "D", "c@d.com")
        self.assertNotEqual(u1.id, u2.id)
    def test_created_at_set_on_creation(self):
        u = User("A", "B", "a@b.com")
        self.assertIsNotNone(u.created_at)
    def test_save_updates_updated_at(self):
        import time
        u = User("A", "B", "a@b.com")
        before = u.updated_at
        time.sleep(0.01)
        u.save()
        self.assertGreater(u.updated_at, before)
    def test_update_method_changes_attribute(self):
        u = User("A", "B", "a@b.com")
        u.update({"first_name": "Zara"})
        self.assertEqual(u.first_name, "Zara")
    def test_update_cannot_change_id(self):
        u = User("A", "B", "a@b.com")
        original_id = u.id
        u.update({"id": "hacked"})
        self.assertEqual(u.id, original_id)

class TestUser(unittest.TestCase):
    def test_valid_user_creation(self):
        u = User("Alice", "Smith", "alice@example.com")
        self.assertEqual(u.first_name, "Alice")
    def test_empty_first_name_raises(self):
        with self.assertRaises(ValueError):
            User("", "Smith", "a@b.com")
    def test_first_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            User("A" * 51, "Smith", "a@b.com")
    def test_empty_last_name_raises(self):
        with self.assertRaises(ValueError):
            User("Alice", "", "a@b.com")
    def test_last_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            User("Alice", "B" * 51, "a@b.com")
    def test_invalid_email_raises(self):
        with self.assertRaises(ValueError):
            User("Alice", "Smith", "not-an-email")
    def test_is_admin_defaults_false(self):
        u = User("Alice", "Smith", "alice@example.com")
        self.assertFalse(u.is_admin)
    def test_to_dict_excludes_password(self):
        u = User("Alice", "Smith", "alice@example.com", password="secret")
        self.assertNotIn("password", u.to_dict())
    def test_to_dict_has_required_keys(self):
        u = User("Alice", "Smith", "alice@example.com")
        for key in ("id", "first_name", "last_name", "email"):
            self.assertIn(key, u.to_dict())

class TestAmenity(unittest.TestCase):
    def test_valid_amenity_creation(self):
        a = Amenity("WiFi")
        self.assertEqual(a.name, "WiFi")
    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            Amenity("")
    def test_name_too_long_raises(self):
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.owner = User("Bob", "Jones", "bob@example.com")
    def _make_place(self, **kwargs):
        defaults = dict(title="Cozy Flat", description="Nice", price=50.0,
                        latitude=40.7, longitude=-74.0, owner=self.owner)
        defaults.update(kwargs)
        return Place(**defaults)
    def test_valid_place_creation(self):
        p = self._make_place()
        self.assertEqual(p.title, "Cozy Flat")
    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self._make_place(price=-1)
    def test_latitude_too_high_raises(self):
        with self.assertRaises(ValueError):
            self._make_place(latitude=91.0)
    def test_longitude_too_high_raises(self):
        with self.assertRaises(ValueError):
            self._make_place(longitude=181.0)
    def test_add_amenity(self):
        p = self._make_place()
        a = Amenity("WiFi")
        p.add_amenity(a)
        self.assertIn(a, p.amenities)
    def test_to_dict_includes_owner(self):
        p = self._make_place()
        self.assertIn("owner", p.to_dict())

class TestReview(unittest.TestCase):
    def setUp(self):
        self.user = User("Dave", "Kim", "dave@example.com")
        self.owner = User("Eve", "Park", "eve@example.com")
        self.place = Place("Studio", "", 30.0, 0.0, 0.0, self.owner)
    def test_valid_review_creation(self):
        r = Review("Loved it", 5, self.place, self.user)
        self.assertEqual(r.rating, 5)
    def test_empty_text_raises(self):
        with self.assertRaises(ValueError):
            Review("", 4, self.place, self.user)
    def test_rating_zero_raises(self):
        with self.assertRaises(ValueError):
            Review("Good", 0, self.place, self.user)
    def test_rating_six_raises(self):
        with self.assertRaises(ValueError):
            Review("Good", 6, self.place, self.user)
    def test_to_dict_has_place_and_user(self):
        r = Review("Nice", 3, self.place, self.user)
        d = r.to_dict()
        self.assertIn("place_id", d)
        self.assertIn("user_id", d)

if __name__ == "__main__":
    unittest.main()
