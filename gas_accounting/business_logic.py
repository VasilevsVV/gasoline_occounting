from gas_accounting import entities
from gas_accounting import utils


class GasolineTable:

    def __init__(self):
        self.purchase_table = {}
        self.trips_table = {}
        self.purchase_ids = 0
        self.trips_ids = 0

    def add_trip(self, start_date, final_date, fuel):
        trip = entities.Trip(start_date, final_date)
        trip.fuel = fuel
        self.trips_table[self.trips_ids] = trip
        self.trips_ids += 1
        return self.trips_ids - 1

    def add_trip_consumption(self, start_date, final_date, distance, fuel_per_km):
        trip = entities.Trip(start_date, final_date)
        trip.fuel = fuel_per_km * distance
        self.trips_table[self.trips_ids] = trip
        self.trips_ids += 1
        return self.trips_ids - 1

    def delete_trip(self, id):
        return self.trips_table.pop(id)

    def list_trips_between_dates(self, start_date, final_date):
        return [val for val in self.trips_table.values()
                if (val.end_date > start_date > val.start_date or
                    val.end_date > final_date > val.start_date)]

    def list_trips_after_date(self, date):
        return [val for val in self.trips_table.values() if (val.end_date > date)]

    def list_trips_before_date(self, date):
        return [val for val in self.trips_table.values() if (val.start_date < date)]

    def search_trips_by_date(self, date):
        return [val for val in self.trips_table.values()
                if (val.end_date > date > val.start_date)]
