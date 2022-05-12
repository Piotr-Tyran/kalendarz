from datetime import timedelta
from dateutil.relativedelta import relativedelta


def to_timedelta(reminder):
    td = timedelta()

    if reminder['time'] == 'week':
        td = timedelta(weeks=reminder['value'])
    elif reminder['time'] == 'day':
        td = timedelta(days=reminder['value'])
    elif reminder['time'] == 'hour':
        td = timedelta(hours=reminder['value'])
    else:
        td = timedelta(minutes=reminder['value'])

    return td


def from_timedelta(td):
    if not td % timedelta(weeks=1):
        time = 'week'
        value = td / timedelta(weeks=1)
    elif not td % timedelta(days=1):
        time = 'day'
        value = td / timedelta(days=1)
    elif not td % timedelta(hours=1):
        time = 'hour'
        value = td / timedelta(hours=1)
    else:
        time = 'minute'
        value = td / timedelta(minutes=1)

    return {'value': value, 'time': time, 'delete': False}


def to_relativedelta(string):
    if string == 'relativedelta(days=+1)':
        rd = relativedelta(days=1)
    elif string == 'relativedelta(days=+7)':
        rd = relativedelta(weeks=1)
    elif string == 'relativedelta(months=+1)':
        rd = relativedelta(months=1)
    else:
        rd = None

    return rd


def from_relativedelta(string):
    string = str(string)

    if string == '1 day, 0:00:00':
        rd = relativedelta(days=1)
    elif string == '7 days, 0:00:00':
        rd = relativedelta(weeks=1)
    elif string in ('28 days, 0:00:00', '29 days, 0:00:00',
                    '30 days, 0:00:00', '31 days, 0:00:00'):
        rd = relativedelta(months=1)
    else:
        rd = relativedelta()

    return rd
