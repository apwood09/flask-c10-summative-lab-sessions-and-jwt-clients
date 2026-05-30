# seed.py
# faker: securely create sample operational datasets for debugging endpoints

from faker import Faker 
import random 
from config import app, db 
from models import User, Workout

fake = Faker()

with app.app_context(): 
    print("Clearing database records...")
    Workout.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating sample target users...")
    users_list = []
    # fixed testing acounts
    demouser1 = User(username="iron_athlete")
    demouser1.password_hash = "password123"
    demouser2 = User(username="cardio_king")
    demouser2.password_hash = "password123"

    db.session.add_all([demouser1, demouser2])
    users_list.extend([demouser1, demouser2])

    # dynamic generation 
    for _ in range(5):
        u = User(username=fake.user_name())
        u.password_hash = "securepassword!"
        db.session.add(u)
        users_list.append(u)
    
    db.session.commit()

    print("Generating randomized paginated workout data entries...")
    workout_types = ["Upper Body Hypertrophy", "Steady State Rowing", "HIIT Sprint Circuit", "Yoga Flexibility Flow", "Leg Day Core Focus"]
    
    for user in users_list:
        # gnerate: 8 to 12 workout routines per user to verify pagination limits
        for _ in range(random.randint(8, 12)):
            w = Workout(
                title=random.choice(workout_types),
                description=fake.sentence(nb_words=8),
                duration_minutes=random.choice([30, 45, 60, 75, 90]),
                user_id=user.id
            )
            db.session.add(w)
            
    db.session.commit()
    print("Database seeding completed successfully.")