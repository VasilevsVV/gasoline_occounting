import time
import doctest


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

    def add_fuel(self, fuel):
        """Adds a new used fuel to already used.
        Args:
            fuel:New used fuel.
        >>> trip.add_fuel(30)
        30"""
        self.fuel += fuel
        return self.fuel

    def set_fuel(self, fuel):
        """Sets trip.fuel to new value.
        Args:
            fuel:New value
        >>> trip.set_fuel(125)
        125"""
        self.fuel = fuel
        return self.fuel

    def prints(self):
        """Prints a trip to console.
        >>> trip.prints()
        Trip
            start date: 1970.01.01 03:02
            final date: 1970.01.01 03:10
            gasoline: 30"""
        print('Trip\n\tstart date: {}\n\tfinal date: {}\n\tgasoline: {}'.
              format(time.strftime("%Y.%m.%d %H:%M",
                                   time.localtime(self.start_date)),
                     time.strftime("%Y.%m.%d %H:%M",
                                   time.localtime(self.end_date)),
                     self.fuel))

    def get_print(self):
        """Returns string with printed trip to it.
        >>> trip.get_print()
        'Trip\\n\\tstart date: 1970.01.01 03:02\\n\\tfinal date: 1970.01.01 03:10\\n\\tgasoline: 30'"""
        return ('Trip\n\tstart date: {}\n\tfinal date: {}\n\tgasoline: {}'.
                format(time.strftime("%Y.%m.%d %H:%M",
                                     time.localtime(self.start_date)),
                       time.strftime("%Y.%m.%d %H:%M",
                                     time.localtime(self.end_date)),
                       self.fuel))

    def in_line(self):
        """Returns trip in one line.
        >>> trip.in_line()
        '150::600::30'"""
        return ('{}::{}::{}'.
                format(self.start_date,
                       self.end_date,
                       self.fuel))

    def __eq__(self, other):
        return (self.start_date == other.start_date and
                self.end_date == other.end_date and
                self.fuel == other.fuel)

    def __repr__(self):
        return ('{}::{}::{}'.
                format(self.start_date,
                       self.end_date,
                       self.fuel))

if __name__ == "__main__":
    doctest.testmod(extraglobs={"trip": Trip(150, 600)})
