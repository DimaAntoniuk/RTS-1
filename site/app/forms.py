from app import app, photos, db
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, FloatField, DateTimeField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from bson.objectid import ObjectId

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
    submit = SubmitField('Add Checkpoint')

    def validate_name(self, name):
        list = checkpoints_col.distinct(key='name')
        if name.data in list:
            raise ValidationError('Please use a different name.')

class EditCheckpointForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    operator = StringField('Operator', validators=[DataRequired()])
    id = HiddenField()
    submit = SubmitField('Edit Checkpoint')

    def validate_name(self, name):
        list = checkpoints_col.distinct(key='name')
        checkpoint = checkpoints_col.find({"_id":ObjectId(self.id.data)})[0]
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
    admin = SelectField('Admin User', choices=[('admin', 'Admin'), ('organizer', 'Organizer')])
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
