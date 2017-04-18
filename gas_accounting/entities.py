import time


class Purchase:
    def __init__(self, date, fuel, price):
        self.date = date
        self.fuel = fuel
        self.price = price
        self.cost = self.fuel * self.price


class Trip:
    def __init__(self, start_date, end_date=0):
        self.start_date = start_date
        self.end_date = end_date
        self.fuel = 0

    def calc_cost_add(self, fuel, price):
        self.fuel += fuel
        self.cost += fuel * price
        return self.cost

    def add_fuel(self, fuel):
        self.fuel += fuel
        return self.fuel

    def prints(self):
        print('Trip\n\tstart date: {}\n\tfinal date: {}'.
              format(time.strftime("%Y.%m.%d %H:%M", time.localtime(self.start_date)),
                     time.strftime("%Y.%m.%d %H:%M", time.localtime(self.end_date))))

    def get_print(self):
        return ('Trip\n\tstart date: {}\n\tfinal date: {}'.
                format(time.strftime("%Y.%m.%d %H:%M", time.localtime(self.start_date)),
                       time.strftime("%Y.%m.%d %H:%M", time.localtime(self.end_date))))





