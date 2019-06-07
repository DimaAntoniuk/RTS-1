from app import app, db, mqtt, photos
from flask import render_template, redirect, url_for, flash, request
from app.forms import RegisterRunnerForm, AddCheckpointForm, SignInForm, SignUpForm, RegisterRaceForm, EditRaceForm, EditCheckpointForm, RegisterForRace, SignUpForm
from app.models import User, Event, Race, Runner, Checkpoint
from flask_login import current_user, login_user, logout_user
from bson.objectid import ObjectId
from werkzeug.urls import url_parse

races_col = db.races
users_col = db.users
events_col = db.events
runners_col = db.runners
checkpoints_col = db.checkpoints

user = User(username = 'admin')
user.set_password('admin')
users_col.insert_one(user.__dict__)


@app.route('/')
def index():
	list = [race for race in races_col.find()]
	return render_template('index.html', races=list)


@app.route('/sign_in', methods=['GET', 'POST'])
def login():
	title = "Login"
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignInForm()
	if form.validate_on_submit():
		user = User(dict = users_col.find({"username":form.username.data})[0])
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('index'))
		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', form=form)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	mqtt.subscribe('myTopic')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	payload=message.payload.decode().split(' ')
	payload[0]=payload[0].strip()
	payload[2]+=(' ' + payload[3])
	payload.pop()
	print(payload)
	event = Event(payload[0], payload[1], payload[2])
	events_col.insert_one(event.__dict__)


@app.route("/clear")
def clear():
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	events_col.remove()
	return redirect(url_for('table'))

@app.route("/clear/<race_id>")
def clear_checkpoints(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	for checkpoint in race['checkpoints']:
		checkpoints_col.delete_one({"_id":checkpoint})
	races_col.update_one({"_id":ObjectId(race_id)}, {"$set":{"checkpoints":[]}})
	return redirect(url_for('race_checkpoints', race_id=race_id))

@app.route("/clear2/<race_id>")
def clear_runners(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	races_col.update_one({"_id":ObjectId(race_id)}, {"$set":{"runners":[]}})
	return redirect(url_for('race_runners', race_id=race_id))

@app.route("/results")
def table():
	title = "Results"
	list = [event for event in events_col.find()]
	list.reverse()
	return render_template("table.html", events=list, title=title)


@app.route('/register_runner', methods=['GET', 'POST'])
def register_runner():
	title = "Runner Registration"
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	form = RegisterRunnerForm()
	if form.validate_on_submit():
		runner = Runner(form.first_name.data, form.last_name.data, form.id.data)
		runners_col.insert_one(runner.__dict__)
		flash('Runner {} {} is successfully registered.'.format(runner.first_name, runner.last_name))
		return redirect(url_for('runners_table'))
	return render_template('register_runner.html', form=form, title=title)

@app.route('/runners')
def runners_table():
	title = "Runners"
	list = [runner for runner in runners_col.find()]
	return render_template('runners_table.html', runners=list, title=title)

@app.route('/register_race', methods=['GET', 'POST'])
def register_race():
	title = "Race Registration"
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	form = RegisterRaceForm()
	form.laps_number.choices = [(i, i) for i in range(1,11)]
	if form.validate_on_submit():
		filename = photos.save(form.logo.data)
		url = photos.url(filename)
		race = Race(form.name.data, url, form.admin.data, form.laps_number.data, form.distance.data, form.date_and_time_of_race.data, form.description.data, [], [])
		races_col.insert_one(race.__dict__)
		flash('Race {} is successfully registered.'.format(race.name))
		return redirect(url_for('races'))
	return render_template('register_race.html', form=form, title=title)

@app.route("/races")
def races():
	title = "Races"
	list = [race for race in races_col.find()]
	return render_template("races.html", races=list, title=title)

@app.route("/race/<race_id>")
def race(race_id):
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	return render_template("race.html", race=race)

@app.route("/race/<race_id>/delete")
def delete_race(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	races_col.delete_one(race)
	return redirect(url_for('races'))

@app.route("/race/<race_id>/edit", methods=['GET', 'POST'])
def edit_race(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	checkpoints = race['checkpoints']
	runners = race['runners']
	form = EditRaceForm()
	form.laps_number.choices = [(i, i) for i in range(1,11)]
	if form.validate_on_submit():
		if form.logo.data == None:
			url = race['logo']
		else:
			filename = photos.save(form.logo.data)
			url = photos.url(filename)
		race = Race(form.name.data, url, form.admin.data, form.laps_number.data, form.distance.data, form.date_and_time_of_race.data, form.description.data, checkpoints, runners)
		races_col.replace_one({"_id":ObjectId(race_id)}, race.__dict__)
		flash('Race {} is successfully edited.'.format(race.name))
		return redirect(url_for('race', race_id=race_id))
	elif request.method == 'GET':
		form.add_data(race)

	return render_template('race.html', form=form, race_name=race['name'], race_id=race_id)

@app.route("/race/<race_id>/checkpoints")
def race_checkpoints(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	list = [checkpoints_col.find({"_id":checkpoint})[0] for checkpoint in race['checkpoints']]
	return render_template('race_checkpoints.html', race_name=race['name'], checkpoints=list, race_id=race_id)

@app.route('/race/<race_id>/add_checkpoint', methods=['GET', 'POST'])
def register_checkpoint(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	form = AddCheckpointForm()
	form.id.data = ObjectId(race_id)
	if form.validate_on_submit():
		checkpoint = Checkpoint(form.name.data, form.operator.data, ObjectId(race_id))
		checkpoints_col.insert_one(checkpoint.__dict__)
		checkpoint_in_db = checkpoints_col.find(checkpoint.__dict__)[0]
		races_col.update_one({"_id":ObjectId(race_id)}, {"$addToSet":{"checkpoints":checkpoint_in_db['_id']}})
		flash('Checkpoint {} is successfully registered.'.format(checkpoint.name))
		return redirect(url_for('race_checkpoints', race_id=race_id))
	return render_template('register_checkpoint.html', form=form)

@app.route("/race/<race_id>/checkpoint/<checkpoint_id>/edit", methods=['GET', 'POST'])
def edit_checkpoint(race_id, checkpoint_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	checkpoint = checkpoints_col.find({"_id":ObjectId(checkpoint_id)})[0]
	form = EditCheckpointForm()
	if form.validate_on_submit():
		checkpoint = Checkpoint(form.name.data, form.operator.data, ObjectId(race_id))
		checkpoints_col.replace_one({"_id":ObjectId(checkpoint_id)}, checkpoint.__dict__)
		flash('Checkpoint {} is successfully edited.'.format(checkpoint.name))
		return redirect(url_for('race_checkpoints', race_id=race_id))
	elif request.method == 'GET':
		form.add_data(checkpoint)

	return render_template('edit_checkpoint.html', form=form, checkpoint_name=checkpoint['name'], race_id=race_id, checkpoint_id=checkpoint_id)

@app.route("/race/<race_id>/checkpoint/<checkpoint_id>/delete")
def delete_checkpoint(race_id, checkpoint_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	checkpoint = checkpoints_col.find({"_id":ObjectId(checkpoint_id)})[0]
	races_col.update_one({"_id":ObjectId(race_id)}, {"$pullAll":{"checkpoints":[ObjectId(checkpoint_id)]}})
	checkpoints_col.delete_one(checkpoint)
	return redirect(url_for('race_checkpoints', race_id=race_id))

@app.route('/race/<race_id>/register_for_race', methods=['GET', 'POST'])
def register_for_race(race_id):
	form = RegisterForRace()
	if form.validate_on_submit():
		flash('Runner {} {}  is successfully registered.'.format(form.first_name.data, form.last_name.data))
		runner = Runner(form.first_name.data, form.last_name.data, form.age.data)
		races_col.update_one({"_id":ObjectId(race_id)}, {"$addToSet":{"runners":runner.__dict__}})
		return redirect(url_for('index'))
	return render_template('register_for_race.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignUpForm()
	if form.validate_on_submit():
		user = User(form.username.data, form.first_name.data, form.last_name.data, form.age.data, form.email.data)
		user.set_password(form.password.data)
		users_col.insert_one(user.__dict__)
		flash('User {} is successfully registered.'.format(user.username))
		return redirect(url_for('login'))

	return render_template('register_on_site.html', form=form)

@app.route("/race/<race_id>/runners")
def race_runners(race_id):
	if current_user.is_anonymous:
		return redirect(url_for('index'))
	race = races_col.find({"_id":ObjectId(race_id)})[0]
	print(race['runners'])
	return render_template('race_runners.html', race_name=race['name'], runners=race['runners'], race_id=race_id)

@app.route('/sign_out')
def logout():
	logout_user()
	return redirect(url_for('index'))
