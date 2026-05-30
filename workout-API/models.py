# models.py
# defines users & workout models, enforce constraints, hashes passwords securely, & sets up serialization schemas 

from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property 
from marshmallow import Schema, fields
from config import db, bcrypt 

class User(db.Model): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    # relationship: 1 user -> many workouts 
    workouts = db.relationship('Workout', back_populates='user', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self): 
        raise AttributeError('Password hashes cannot be viewed directly.')

    @password_hash.setter
    def password_hash(self, password): 
        if not password or len(password) < 6: 
            raise ValueError("Password must be at least 6 characters long.")
        hashed = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed.decode('utf-8')

    def authenticate(self, password): 
        return bcrypt.check_password_hash(self._password_hash, password.ecode('utf-8'))

    @validates('username')
    def validate_username(self, key, username): 
        if not username or len(username.strip()) == 0: 
            raise ValueError("Username is required.")
        return username.strip()

class Workout(db.Model): 
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=Flase)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.Foreignkey('users.id'), nullable=False)

    # relationship: back to user
    user = db.relationship('User', back_populates='workouts')
    
    @validates('title')
    def validate_title(self, key, title): 
        if not title or len(title.strip()) == 0: 
            raise ValueError("workout title is required.")
        return title.strip()

    @validates('duration_minutes')
    def validate_duration(self, key, duration): 
        if duration is None or int(duration) <= 0: 
            raise ValueError("Duration must be a positive integer greater than 0.")
        return int(duration)

# MARSHMALLOW SERIALIZATION SCHEMAS
class UserSchema(Schema): 
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)

class WorkoutSchema(Schema): 
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    duration_minutes = fields.Integer(required=True)
    user_id = fields.Integer(dump_only=True)

user_schema = UserSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)