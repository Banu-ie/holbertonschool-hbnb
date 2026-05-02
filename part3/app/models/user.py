from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    _password  = db.Column('password', db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def hash_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def verify_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin,
        })
        return base
