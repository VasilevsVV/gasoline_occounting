import time


class Purchase:
    def __init__(self, date, fuel, price):
        self.date = date
        self.fuel = fuel
        self.price = price
        self.cost = self.fuel * self.price


class Trip:
    def __init__(self, start_date, end_date=0):
        """Initializes a trip.
        Args:
            start_date:Date when trip begun.
            end_date:Date when trip ended."""
        self.start_date = start_date
        self.end_date = end_date
        self.fuel = 0

    def calc_cost_add(self, fuel, price):
        """Calculates a cost of all used fuel
        based on it price.
        Args:
            fuel:fuel
            price:price of the fuel
        >>> trip.calc_cost_add(50, 10)
        500"""
        self.fuel += fuel
        self.cost += fuel * price
        return self.cost

    def add_fuel(self, fuel):
        """Adds a new used fuel to already used.
        Args:
            fuel:New used fuel.
        >>> trip.add_fuel(30)
        80"""
        self.fuel += fuel
        return self.fuel

    def set_fuel(self, fuel):
        self.fuel = fuel
        return self.fuel

    def prints(self):
        print('Trip\n\tstart date: {}\n\tfinal date: {}\n\tgasoline: {}'.
              format(time.strftime("%Y.%m.%d %H:%M",
                                   time.localtime(self.start_date)),
                     time.strftime("%Y.%m.%d %H:%M",
                                   time.localtime(self.end_date)),
                     self.fuel))

    def get_print(self):
        return ('Trip\n\tstart date: {}\n\tfinal date: {}\n\tgasoline: {}'.
                format(time.strftime("%Y.%m.%d %H:%M",
                                     time.localtime(self.start_date)),
                       time.strftime("%Y.%m.%d %H:%M",
                                     time.localtime(self.end_date)),
                       self.fuel))

    def in_line(self):
        return ('{}::{}::{}'.
                format(self.start_date,
                       self.end_date,
                       self.fuel))

if __name__ == "__main__":
    doctest.testmod(extraglobs={"trip": Trip(150, 600)})
