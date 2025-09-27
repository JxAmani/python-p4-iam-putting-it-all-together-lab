#!/usr/bin/env python3

from flask import Flask, request, session
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, User, Recipe

# ----------- Setup ----------- #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ----------- Resources ----------- #

# ✅ SIGNUP
class Signup(Resource):
    def post(self):
        # Prevent Flask 400 Bad Request
        data = request.get_json(force=True, silent=True) or {}

        username = data.get("username")
        password = data.get("password")
        bio = data.get("bio")
        image_url = data.get("image_url")

        if not username or not password:
            return {"error": "Username and password required"}, 422

        user = User(username=username, bio=bio, image_url=image_url)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id  # auto-login

        return user.to_dict(), 201


# ✅ LOGIN
class Login(Resource):
    def post(self):
        data = request.get_json(force=True, silent=True) or {}

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id
            return user.to_dict(), 200

        return {"error": "Invalid username or password"}, 401


# ✅ CHECK SESSION
class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if user_id:
            user = db.session.get(User, user_id)
            if user:
                return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401


# ✅ LOGOUT
class Logout(Resource):
    def delete(self):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401
        session.pop("user_id", None)
        return {}, 204


# ✅ RECIPES
class RecipeIndex(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = db.session.get(User, user_id)
        if not user:
            return {"error": "Unauthorized"}, 401

        recipes = [recipe.to_dict() for recipe in user.recipes]
        return recipes, 200

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json(force=True, silent=True) or {}

        instructions = data.get("instructions")
        if not instructions or len(instructions.split()) < 10:
            return {"error": "Instructions must be at least 10 words long"}, 422

        recipe = Recipe(
            title=data.get("title"),
            instructions=instructions,
            minutes_to_complete=data.get("minutes_to_complete"),
            user_id=user_id,
        )

        db.session.add(recipe)
        db.session.commit()

        return recipe.to_dict(), 201


# ✅ Home
@app.route("/")
def index():
    return {"message": "Welcome to the Recipe App!"}, 200


# ----------- Routes ----------- #
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")
api.add_resource(RecipeIndex, "/recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
