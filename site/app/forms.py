from app import app, photos, db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, FloatField, DateTimeField, TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import DataRequired, InputRequired, ValidationError, EqualTo, Email
from bson.objectid import ObjectId

races_col = db.races
users_col = db.users
runners_col = db.runners
checkpoints_col = db.checkpoints

class RegisterRunnerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Register Runner')

    def validate_id(self, id):
        list = runners_col.distinct(key='id')
        if id.data in list:
            raise ValidationError('Please use a different id.')

class AddCheckpointForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    operator = StringField('Operator', validators=[DataRequired()])
    id = HiddenField()
    submit = SubmitField('Add Checkpoint')

    def validate_name(self, name):
        race = races_col.find({"_id":self.id.data})[0]
        list = [checkpoints_col.find({"_id":checkpoint})[0]['name'] for checkpoint in race['checkpoints']]
        if name.data in list:
            raise ValidationError('Please use a different name.')

class EditCheckpointForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    operator = StringField('Operator', validators=[DataRequired()])
    id = HiddenField()
    submit = SubmitField('Edit Checkpoint')

    def validate_name(self, name):
        checkpoint = checkpoints_col.find({"_id":ObjectId(self.id.data)})[0]
        race = races_col.find({"_id":checkpoint['race']})[0]
        list = [checkpoints_col.find({"_id":checkpoint})[0]['name'] for checkpoint in race['checkpoints']]
        list.remove(checkpoint['name'])
        if name.data in list:
            raise ValidationError('Please use a different name.')

    def add_data(self, checkpoint):
        self.name.data = checkpoint['name']
        self.operator.data = checkpoint['operator']
        self.id.data = checkpoint['_id']

class RegisterRaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    logo = FileField('Logo', validators=[FileAllowed(photos, 'File is not an image.'), FileRequired('File was empty.')])
    admin = SelectField('Admin User', choices=[('Admin', 'Admin'), ('Organizer', 'Organizer')])
    laps_number = SelectField('Number of laps', coerce=int)
    distance = FloatField('Distance of the race (km)', validators=[InputRequired(), DataRequired('Not a right data format.')])
    date_and_time_of_race = DateTimeField('Date (Format: 01.01.2000 12:00)', format='%d.%m.%Y %H:%M', validators=[InputRequired(), DataRequired('Not a right data format.')])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Register Race')

class EditRaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    logo = FileField('Logo', validators=[FileAllowed(photos, 'File is not an image.')])
    admin = SelectField('Admin User', choices=[('admin', 'Admin'), ('organizer', 'Organizer')])
    laps_number = SelectField('Number of laps', coerce=int)
    distance = FloatField('Distance of the race (km)', validators=[InputRequired(), DataRequired('Not a right data format.')])
    date_and_time_of_race = DateTimeField('Date (Format: 01.01.2000 12:00)', format='%d.%m.%Y %H:%M', validators=[InputRequired(), DataRequired('Not a right data format.')])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit Race')

    def add_data(self, race):
        self.name.data = race['name']
        self.admin.data = race['admin']
        self.laps_number.data = race['laps_number']
        self.distance.data = race['distance']
        self.date_and_time_of_race.data = race['date_and_time_of_race']
        self.description.data = race['description']

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForRace(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Register for race')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        list = users_col.distinct(key='username')
        if username.data in list:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        list = users_col.distinct(key='email')
        if email.data in list:
            raise ValidationError('Please use a different email.')
