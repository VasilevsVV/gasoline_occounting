from gas_accounting import utils


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
        self.cost = 0

    def calc_cost_add(self, fuel, price):
        self.fuel += fuel
        self.cost  += fuel * price
        return self.cost

    def add_fuel(self, fuel):
        self.fuel += fuel
        return self.fuel

    # def get_fuel_from_purchases(self):
    #     for p in self.purchaseList:




