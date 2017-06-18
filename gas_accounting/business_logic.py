import entities
import pickle
import utils
from serialize import Serialize as sr


class GasolineTable:
    """ Class with main logic.
    Working with trips."""
    def __init__(self):
        """Initializes the GasolineTable class."""
        self.trips_table = {}
        self.trips_ids = 0
        self.__loaded = False
        self.__current_table_name = ""
        self.__new_table_name = None
        self.__dump_type = sr.pickle
        # try:
        #     with open('gas_storage.pickle', 'rb') as f:
        #         [self.trips_table, self.trips_ids] = pickle.load(f)
        # except Exception as e:
        #     print("{}\nCreating new table.".format(e))
        #     self.trips_table = {}
        #     self.trips_ids = 0

    def __del__(self):
        """ Saves (dumps) current table when session is over."""
        if self.__new_table_name is not None:
            sr.delete(self.__current_table_name, sr.pickle)
            sr.dump(self.__new_table_name, [self.trips_table, self.trips_ids], sr.pickle)
        else:
            sr.dump(self.__current_table_name, [self.trips_table, self.trips_ids], sr.pickle)
        # try:
        #     with open('gas_storage.pickle', 'wb') as f:
        #         pickle.dump([self.trips_table, self.trips_ids], f)
        # except Exception as e:
        #     print("Error while dumping table!!!\n{}".format(e))

    def add_trip(self, start_date, final_date, fuel):
        """ Adds a trip to table. 
        Args:
            start_date(time): Date of trips begin.
            final_date(time): Date of trips end.
            fuel(number): Amount of spent fuel."""
        trip = entities.Trip(start_date, final_date)
        trip.fuel = fuel
        self.trips_table[self.trips_ids] = trip
        self.trips_ids += 1
        return self.trips_ids - 1

    def add_trip_consumption(self, start_date, final_date,
                             distance, fuel_per_km):
        """ Adds a trip to table by distance and fuel/km.
        Args:
            start_date(time): Date of trips begin.
            final_date(time): Date of trips end.
            distance(number): Distance of trip.
            fuel_per_km(number): fuel/km consumption."""
        trip = entities.Trip(start_date, final_date)
        trip.fuel = fuel_per_km * distance
        self.trips_table[self.trips_ids] = trip
        self.trips_ids += 1
        return self.trips_ids - 1

    def delete_trip(self, id):
        """Deletes trip by id.
        Args:
            id(integer): Id of trip."""
        return self.trips_table.pop(id)

    def get_trip_by_id(self, id):
        """ Returns trip by id.
        Args:
            id(integer): Id of trip."""
        return self.trips_table[id]

    def list_all(self):
        """ Returns list of all trips."""
        return [(key, val) for key, val in self.trips_table.items()]

    def list_trips_between_dates(self, start_date, final_date, strict=False):
        """ Returns list of all trips between two dates.
        Args:
            start_date(time): minimal date.
            final_date(time): maximal date.
            strict(boolean): if false: trips with dates
             equal to min or max date would be listed."""
        if strict:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.start_date > start_date and
                        val.end_date < final_date)]
        else:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.end_date > start_date > val.start_date or
                        val.end_date > final_date > val.start_date)]

    def list_trips_after_date(self, date, strict=False):
        """ Return list of all trips after particular date.
        Args:
            date(time): minimal date of trip.
            strict(boolean): if false: trips with dates
             equal to minimal date would be listed."""
        if strict:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.start_date > date)]
        else:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.end_date >= date)]

    def list_trips_before_date(self, date, strict=False):
        """ Returns list of all trips before particular date.
        Args:
            date(time): maximal date of trip.
            strict(boolean): if false: trips with dates
             equal to maximal date would be listed."""
        if strict:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.end_date < date)]
        else:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.start_date <= date)]

    def search_trips_by_date(self, date):
        """ Return list of all trips which took place on
        particular date.
        Args:
            date(time): Date of required trips."""
        return [(key, val) for key, val in self.trips_table.items()
                if (val.end_date >= date >= val.start_date)]

    def calculate_gasoline_between_dates(self, start_date, final_date,
                                         strict=False):
        """ Returns amount of fuel which was spent between 
        particular dates.
        Args:
            start_date(time): minimal date.
            final_date(time): maximal date.
            strict(boolean): if false: fuel from trips with dates
             equal to min or max date would be added to sum."""
        res = 0
        for i in self.list_trips_between_dates(start_date, final_date, strict):
            res += i[1].fuel
        return res

    def calculate_gasoline_after_date(self, date, strict=False):
        """ Returns amount of fuel which was spent after
        particular date.
        Args:
            date(time): minimal date of trips.
            strict(boolean): if false: fuel from trips with dates
             equal to minimal date would be added to sum."""
        res = 0
        for i in self.list_trips_after_date(date, strict):
            res += i[1].fuel
        return res

    def calculate_gasoline_before_date(self, date, strict=False):
        """ Returns amount of fuel which was spent after
                particular date.
        Args:
            date(time): maximal date of trips.
            strict(boolean): if false: fuel from trips with dates 
                equal to maximal date would be added to sum."""
        res = 0
        for i in self.list_trips_before_date(date, strict):
            res += i[1].fuel
        return res
