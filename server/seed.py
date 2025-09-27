from app import create_app, db, User, Recipe
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Clear existing data
    Recipe.query.delete()
    User.query.delete()
    db.session.commit()

    # Create sample users with hashed passwords
    ash = User(
        username="ashketchum",
        bio="""I wanna be the very best
Like no one ever was
To catch them is my real test
To train them is my cause
I will travel across the land
Searching far and wide
Teach Pokémon to understand
The power that's inside""",
        image_url="https://cdn.vox-cdn.com/thumbor/I3GEucLDPT6sRdISXmY_Yh8IzDw=/0x0:1920x1080/1820x1024/filters:focal(960x540:961x541)/cdn.vox-cdn.com/uploads/chorus_asset/file/24185682/Ash_Ketchum_World_Champion_Screenshot_4.jpg",
        password_hash=generate_password_hash("pikachu")
    )

    misty = User(
        username="misty",
        bio="Gym Leader of Cerulean City",
        image_url="https://upload.wikimedia.org/wikipedia/en/f/f0/Misty_Pokemon.png",
        password_hash=generate_password_hash("staryu")
    )

    db.session.add_all([ash, misty])
    db.session.commit()

    # Create sample recipes for Ash
    recipes = [
        Recipe(
            title="Pikachu's Thunder Snack",
            instructions="Mix berries with electricity-infused water. Serve fresh.",
            minutes_to_complete=15,
            user=ash
        ),
        Recipe(
            title="Pokéball Pancakes",
            instructions="Make pancakes and decorate like Pokéballs. Enjoy!",
            minutes_to_complete=25,
            user=ash
        )
    ]

    db.session.add_all(recipes)
    db.session.commit()

    print("Database seeded successfully!")
