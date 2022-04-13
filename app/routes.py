from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddEventForm, CalendarForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Events, Users_Events
from sqlalchemy import desc


@app.route('/')
@app.route('/Strona_domowa')
def index():
    return render_template('index.html', title="strona startowa")


@app.route('/Kalendarz')
@login_required
def calendar():
    form = CalendarForm()
    return render_template('calendar.html', title='Kalendarz', form=form)


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
        return redirect(url_for('calendar'))
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


@app.route('/add_event', methods=['GET', 'POST'])
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
                                  events_id=event_id)
        db.session.add(user_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html',
                           title='Dodawanie nowego wydarzenia',
                           form=form)

