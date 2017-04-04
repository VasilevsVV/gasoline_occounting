import time


class Purchase:
    def __init__(self, date, amount, price):
        self.date = date
        self.amount = amount
        self.price = price
        self.cost = self.amount * self.price


class Trip:
    def __init__(self, startDate, endDate, purchaseList):
        self.purchaseList = purchaseList
        self.startDate = startDate
        self.endDate = endDate


def make_time(year, month, day, hours, minutes):
    return time.mktime((year, month, day, hours, minutes, 0,0,0,0))




