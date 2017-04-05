from gas_accounting import entities


class GasolineTable:

    def __init__(self):
        self.purchase_table = {}
        self.trip_table = {}
        self.purchase_ids = 0
        self.trips_ids = 0

    def add_purchase(self, fuel, price, date):
        self.purchase_table[self.purchase_ids] = entities.Purchase(date, fuel, price)
        self.purchase_ids += 1
        return self.purchase_ids - 1

    def add_trip(self, start_date, end_date = 0):
        self.trip_table[self.trips_ids] = entities.Trip(start_date, end_date)


