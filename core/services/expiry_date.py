from datetime import timedelta, datetime

def generate_expiry_date(seconds = 0.0, minutes = 0.0, hours = 0.0, days = 0.0):
    _current_time = datetime.now()

    _next_n_time = timedelta(seconds = seconds, minutes = minutes, hours = hours, days = days)

    return _current_time + _next_n_time