from gas_accounting import entities
import pickle


class GasolineTable:

    def __init__(self):
        try:
            with open('gas_storage.pickle', 'rb') as f:
                [self.trips_table, self.trips_ids] = pickle.load(f)
        except Exception as e:
            print("{}\nCreating new table.".format(e))
            self.trips_table = {}
            self.trips_ids = 0

    def __del__(self):
        try:
            with open('gas_storage.pickle', 'wb') as f:
                pickle.dump([self.trips_table, self.trips_ids], f)
        except Exception as e:
            print("Error while dumping table!!!\n{}".format(e))

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

    def list_all(self):
        return [(key, val) for key, val in self.trips_table.items()]

    def list_trips_between_dates(self, start_date, final_date, strict=False):
        if strict:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.start_date > start_date and
                        val.end_date < final_date)]
        else:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.end_date > start_date > val.start_date or
                        val.end_date > final_date > val.start_date)]

    def list_trips_after_date(self, date):
        return [(key, val) for key, val in self.trips_table.items() if (val.end_date > date)]

    def list_trips_before_date(self, date):
        return [(key, val) for key, val in self.trips_table.items() if (val.start_date < date)]

    def search_trips_by_date(self, date):
        return [(key, val) for key, val in self.trips_table.items()
                if (val.end_date > date > val.start_date)]
