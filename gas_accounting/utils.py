import time


def make_time(year, month, day, hours, minutes):
    return time.mktime((year, month, day, hours, minutes, 0,0,0,0))
