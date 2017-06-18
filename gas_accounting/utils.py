import time
import os


def make_time(year, month, day, hours, minutes):
    return time.mktime((year, month, day, hours, minutes, 0, 0, 0, 0))


def parse_time(string):
    dots = string.count(":")
    try:
        if dots == 4:
            return time.mktime(time.strptime(string, "%Y:%m:%d:%H:%M"))
        elif dots == 3:
            return time.mktime(time.strptime(string, "%Y:%m:%d:%H"))
        elif dots == 2:
            return time.mktime(time.strptime(string, "%Y:%m:%d"))
        else:
            return "Invalid date format"
    except Exception as e:
        return "Error while parsing time:\n\t{}".format(e)


def parse_time_with_format(string, form):
    try:
        return time.mktime(time.strptime(string, form))
    except Exception as e:
        return "{}".format(e)


def home_name():
    return dict(os.environb)[b'HOME']
