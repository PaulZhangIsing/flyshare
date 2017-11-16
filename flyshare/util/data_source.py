

def is_tushare(source):
    if source in ['tushare', 'ts', 'Tushare']:
        return True
    else:
        return False

def is_flyshare(source):
    if source in ['flyshare', 'fs', 'Flyshare']:
        return True
    else:
        return False

def is_datareader(source):
    if source in ['datareader']:
        return True
    else:
        return False