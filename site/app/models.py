from flask_login import UserMixin
from app import login


class User(UserMixin):
    id
    username = ''
    password = ''
    role = ''

@login.user_loader
def load_user(id):
    user = User()
    if id == 1:
        user.username = 'admin'
        user.password = 'admin'
        user.role = 'admin'
        user.id = 1

    if id == 2:
        user.username = 'organizer'
        user.password = 'organizer'
        user.role = 'organizer'
        user.id = 2
    return user

class Event:
    def __init__(self, checkpoint_id, tag, time):
        self.checkpoint_id = checkpoint_id
        self.tag = tag
        self.time = time

class Race:
    def __init__(self, name, logo, admin, laps_number, distance, date_and_time_of_race, description, checkpoints):
        self.name = name
        self.logo = logo
        self.admin = admin
        self.laps_number = laps_number
        self.distance = distance
        self.date_and_time_of_race = date_and_time_of_race
        self.description = description
        self.checkpoints = checkpoints

class Runner:
    def __init__(self, first_name, last_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

class Checkpoint:
    def __init__(self, name, operator, race):
        self.name = name
        self.operator = operator
        self.race = race
        
class RegisteredUser:
    def __init__(self, username = None, first_name = None , last_name = None, age = None, password = None, email = None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.password = password
        self.email = email
