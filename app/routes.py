from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddEventForm,\
    ViewEventForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Events, Users_Events
from sqlalchemy import desc
from datetime import datetime, timedelta


@app.route('/')
@app.route('/Strona_domowa')
def index():
    return render_template('index.html', title="strona startowa")


@app.route('/Kalendarz/<offset>')
@login_required
def calendar(offset=0):
    offset = int(offset)
    today = datetime.today().isocalendar()
    monday = datetime.fromisocalendar(today.year, today.week, 1)
    week = [monday + timedelta(days=x, weeks=offset) for x in range(7)]
    events = Events.query.join(Users_Events.query.filter_by(users_id=current_user.id)).\
        where(Events.id == Users_Events.events_id).all()
    return render_template('calendar.html', title='Kalendarz',
                           offset=offset, week=week, events=events)


@app.route('/Logowanie', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calendar'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Błędna nazwa użytkownika lub hasło.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('calendar', offset=0))
    return render_template('login.html', title='Logowanie', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/Rejestracja', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('calendar'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password='')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Witaj {user.username}!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Rejestracja', form=form)


@app.route('/Dodaj_wydarzenie', methods=['GET', 'POST'])
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        event = Events(name=form.name.data,
                       start_date=form.start.data,
                       stop_date=form.stop.data,
                       types=0)
        db.session.add(event)
        db.session.commit()
        event_id = Events.query.filter_by(name=form.name.data).\
            order_by(desc(Events.id)).first().id
        user_event = Users_Events(users_id=current_user.id,
                                  events_id=event_id,
                                  owner=True,
                                  finish=False,
                                  description='')
        db.session.add(user_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html',
                           title='Dodawanie nowego wydarzenia',
                           form=form)


@app.route('/Zobacz_wydarzenie/<id>', methods=['GET', 'POST'])
@login_required
def view_event(id):
    event = Events.query.filter_by(id=id).first_or_404()
    user_event = Users_Events.query.\
        filter_by(events_id=id, users_id=current_user.id).\
        first_or_404()
    form = ViewEventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.start_date = form.start.data
        event.stop_date = form.stop.data
        db.session.commit()
        flash('Zapisano zmiany')
        return redirect(url_for('view_event', id=id))
    elif request.method == 'GET':
        form.start.data = event.start_date
        form.stop.data = event.stop_date
    return render_template('view_event.html', event=event,
                           user_event=user_event,
                           title=event.name, form=form)

