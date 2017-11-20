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

def get_date_today():
    return datetime.date.today().strftime("%Y-%m-%d")

def validate_date(date):
    try:
        time.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False

def is_today(date):
    if validate_date(date):
        if str(today().date()) == date:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    date = '2017-11-16'
    print type(get_date_today())
    print get_date_today()

