import time
import datetime

def date_stamp(date):
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date

def now():
    return datetime.datetime.now()

def today():
    return datetime.datetime.today()

def validate_date(date):
    try:
        time.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False

