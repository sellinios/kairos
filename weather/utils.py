# weather/utils.py

from datetime import datetime

def get_current_date():
    return datetime.now().date()

def get_current_time():
    return datetime.now().time()
