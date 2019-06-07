from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from bson.objectid import ObjectId

users_col = db.users


class User(UserMixin):
    def __init__(self, username=None, first_name=None, last_name=None, age=None, email=None, dict=None):
        if dict is None:
            self.username = username
            self.first_name = first_name
            self.last_name = last_name
            self.age = age
            self.email = email
        else:
            self.username = dict['username']
            self.first_name = dict['first_name']
            self.last_name = dict['last_name']
            self.age = dict['age']
            self.email = dict['email']
            self.id = dict['_id']
            self.password_hash = dict['password_hash']

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    user = User(dict = users_col.find({"_id":ObjectId(id)})[0])
    return user

class Event:
    def __init__(self, checkpoint_id, tag, time):
        self.checkpoint_id = checkpoint_id
        self.tag = tag
        self.time = time

class Race:
    def __init__(self, name, logo, admin, laps_number, distance, date_and_time_of_race, description, checkpoints, runners):
        self.name = name
        self.logo = logo
        self.admin = admin
        self.laps_number = laps_number
        self.distance = distance
        self.date_and_time_of_race = date_and_time_of_race
        self.description = description
        self.checkpoints = checkpoints
        self.runners = runners

class Runner:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class Checkpoint:
    def __init__(self, name, operator, race):
        self.name = name
        self.operator = operator
        self.race = race
