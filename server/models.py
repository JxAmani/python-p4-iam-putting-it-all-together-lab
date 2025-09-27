from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ------------------- USER ------------------- #
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String)

    recipes = db.relationship("Recipe", backref="user", lazy=True)

    # password helpers
    def set_password(self, password):
        self._password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "image_url": self.image_url,
        }


# ------------------- RECIPE ------------------- #
class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @validates("instructions")
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructions": self.instructions,
            "minutes_to_complete": self.minutes_to_complete,
            "user_id": self.user_id,
        }
