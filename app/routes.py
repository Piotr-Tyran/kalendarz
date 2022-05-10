from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddEventForm,\
    ViewEventForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Events, Users_Events, Reminders
from sqlalchemy import desc
from datetime import datetime, timedelta, time
from app.funcs import to_timedelta, from_timedelta


@app.route('/')
@app.route('/Strona_domowa')
def index():
    return render_template('index.html', title="strona startowa")


@app.route('/Kalendarz')
@app.route('/Kalendarz%<x>')
@login_required
def calendar(x=0):
    offset = int(x)
    current_day = datetime.today().date()
    today = datetime.today().isocalendar()
    monday = datetime.fromisocalendar(today.year, today.week, 1)
    week = [monday + timedelta(days=x, weeks=offset) for x in range(7)]
    hour = [timedelta(hours=0+x) for x in range(0, 24)]
    events = Events.query.join(Users_Events.query.filter_by(users_id=current_user.id)).\
        where(Events.id == Users_Events.events_id).all()
    return render_template('calendar.html', title='Kalendarz',
                           offset=offset, week=week, events=events, current_day=current_day, hour=hour)


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
@login_required
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


@app.route('/Dodaj_wydarzenie', methods=['POST'])
def add_event_post():
    form = AddEventForm()
    if form.validate_on_submit():
        event = Events(name=form.name.data,
                       start_date=datetime.strptime(str(form.start.data) + " " + str(form.time[0].od_godziny.data), "%Y-%m-%d %H:%M:%S"),
                       stop_date=datetime.strptime(str(form.stop.data) + " " + str(form.time[0].do_godziny.data), "%Y-%m-%d %H:%M:%S"),
                       types=0)
        db.session.add(event)
        db.session.commit()
        event_id = Events.query.filter_by(name=form.name.data). \
            order_by(desc(Events.id)).first().id
        user_event = Users_Events(users_id=current_user.id,
                                  events_id=event_id,
                                  owner=True,
                                  finish=False,
                                  description='')
        db.session.add(user_event)
        db.session.commit()
        user_event_id = Users_Events.query. \
            filter_by(users_id=current_user.id,
                      events_id=event_id). \
            first().id
        for reminder in form.reminders.data:
            if reminder['delete']:
                r = Reminders(rem_before=to_timedelta(reminder),
                                     id_users_events=user_event_id)
                db.session.add(r)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/Dodaj_wydarzenie')
def add_event_get():
    form = AddEventForm()
    reminder_list = [{'value': 0, 'time': 'hour', 'delete': True}]
    time_list = [{'od_godziny': time(00,00), 'do_godziny': time(00,00), 'caly_dzien': False}]
    form.process(data={'reminders': reminder_list, 'time': time_list})
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
    reminders = Reminders.query.filter_by(id_users_events=user_event.id).all()
    form = ViewEventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.start_date = form.start.data
        event.stop_date = form.stop.data
        rem_len = len(reminders)
        for i in range(rem_len + 1):
            if i < rem_len:
                r = Reminders.query.filter_by(id=reminders[i].id).first()
                if form.reminders.data[i]['delete']:
                    db.session.delete(r)
                else:
                    r.rem_before = to_timedelta(form.reminders.data[i])
            elif not form.reminders.data[i]['delete']:
                r = Reminders(rem_before=to_timedelta(form.reminders.data[-1]),
                              id_users_events=user_event.id)
                db.session.add(r)

        db.session.commit()

        flash('Zapisano zmiany')
        return redirect(url_for('view_event', id=id))
    elif request.method == 'GET':
        reminders_list = [from_timedelta(reminder.rem_before) for
                          reminder in reminders]
        reminders_list.append({'value': 0, 'time': 'week', 'delete': True})
        time_list = [{'od_godziny': time(00,00), 'do_godziny': time(00,00), 'caly_dzien': False}]
        form.process(data={'reminders': reminders_list,
                           'time': time_list,
                           'name': event.name,
                           'start': event.start_date,
                           'stop': event.stop_date})

    return render_template('view_event.html', form=form,
                           user_event=user_event,
                           title=event.name)
