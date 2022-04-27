from app.models import Reminders
from datetime import timedelta


def to_timedelta(reminder):
    td = timedelta()

    if reminder['time'] == 'week':
        td = timedelta(weeks=reminder['value'])
    elif reminder['time'] == 'day':
        td = timedelta(days=reminder['value'])
    elif reminder['time'] == 'hour':
        td = timedelta(hours=reminder['value'])
    elif reminder['time'] == 'minutes':
        td = timedelta(minutes=reminder['value'])

    return td


def from_timedelta(td):
    print(td)
    if not td % timedelta(weeks=1):
        time = 'week'
        value = td / timedelta(weeks=1)
    elif not td % timedelta(days=1):
        time = 'day'
        value = td / timedelta(days=1)
    elif not td % timedelta(hours=1):
        time = 'hour'
        value = td / timedelta(hours=1)
    elif not td % timedelta(minutes=1):
        time = 'minute'
        value = td / timedelta(minutes=1)

    return {'value': value, 'time': time, 'delete': False}
