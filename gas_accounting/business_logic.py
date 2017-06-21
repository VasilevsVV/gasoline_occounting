import entities
import utils
from serialize import Serialize as sr
import configparser as cp
import doctest


class GasolineTable:
    """ Class with main logic.
    Working with trips."""
    def __init__(self, test=False):
        """Initializes the GasolineTable class."""
        self.trips_table = {} if test else None
        self.trips_ids = 0
        self.__loaded = "test" if test else False
        self.__current_table_name = "test" if test else ""
        self.__new_table_name = None
        self.__config = cp.ConfigParser()
        method = self.__probe_config__()
        self.__serialize = sr.pickle
        if method == 'pickle':
            self.__serialize = sr.pickle
        elif method == 'json':
            self.__serialize = sr.json
        elif method == 'yaml':
            self.__serialize = sr.yaml

    def __del__(self):
        """ Saves (dumps) current table when session is over."""
        if not self.__loaded == "test":
            self.dump()

    def current_table_name(self):
        return self.__current_table_name

    def new_table_name(self):
        return self.__new_table_name

    def __probe_config__(self):
        """Tries to parse config file.
        >>> gas.__probe_config__()
        'pickle'"""
        self.__config.read(str(utils.home_name() + b'/.gasconfig', 'utf-8'))
        if 'settings' not in self.__config or self.__loaded == "test":
            self.__config['settings'] = {'serialize': 'pickle'}
            with open(str(utils.home_name() + b'/.gasconfig', 'utf-8'), 'w') as f:
                self.__config.write(f)
        return self.__config['settings'].get('serialize', 'pickle')

    def load(self, table_name):
        """Loads a table from storage by name.
        And dumps old tale if it was loaded.
        Args:
            table_name(string):The name of table which
            would be loaded.
        >>> gas.load("name")
        False"""
        if self.__loaded:
            self.dump()
        [self.trips_table, self.trips_ids] = sr.load(table_name,
                                                     self.__serialize)
        self.__current_table_name = table_name
        self.__loaded = True
        if self.trips_table.__len__() == 0:
            return False
        else:
            return True

    def dump(self):
        """Dumps a current table, and deletes
        a table with old name if name was changed."""
        try:
            if self.__new_table_name is not None:
                sr.delete(self.__current_table_name, self.__serialize)
                sr.dump(self.__new_table_name, [self.trips_table,
                                                self.trips_ids],
                        self.__serialize)
            else:
                sr.dump(self.__current_table_name,
                        [self.trips_table, self.trips_ids],
                        self.__serialize)
            return "dumped"
        except Exception as e:
            return "Failed to dump table:\n{}".format(e)

    def set_serialize(self, serialize):
        """Setts serialize to new value.
        Args:
            serialize: New __serialize value"""
        self.__serialize = serialize

    def get_serialize(self):
        """Returns current serialize"""
        return self.__serialize

    def is_loaded(self):
        """Returns a current state of table
        (loaded or not)
        >>> gas.is_loaded()
        'test'"""
        return self.__loaded

    def set_new_name(self, new_name):
        """Setts a new name for table.
        Args:
            new_name: New name for table.
        >>> gas.set_new_name('newname')
        'Name sett as newname'"""
        self.__new_table_name = new_name
        return ("Name sett as {}"
                .format(self.__new_table_name))

    def add_trip(self, start_date, final_date, fuel):
        """ Adds a trip to table.
        Args:
            start_date(time): Date of trips begin.
            final_date(time): Date of trips end.
            fuel(number): Amount of spent fuel.
        >>> gas.add_trip(100, 200, 50)
        0
        >>> gas.add_trip(150, 200, 70)
        1
        >>> gas.add_trip(150, 200, 80)
        2
        >>> gas.add_trip(50, 300, 90)
        3"""
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
            fuel_per_km(number): fuel/km consumption.
        >>> gas.add_trip_consumption(300, 500, 20, 11)
        4
        >>> gas.add_trip_consumption(230, 550, 40, 9)
        5"""
        trip = entities.Trip(start_date, final_date)
        trip.fuel = fuel_per_km * distance
        self.trips_table[self.trips_ids] = trip
        self.trips_ids += 1
        return self.trips_ids - 1

    def delete_trip(self, id):
        """Deletes trip by id.
        Args:
            id(integer): Id of trip.
        >>> gas.delete_trip(2).in_line()
        '150::200::80'"""
        return self.trips_table.pop(id)

    def get_trip_by_id(self, id):
        """ Returns trip by id.
        Args:
            id(integer): Id of trip.
        >>> gas.get_trip_by_id(0).in_line()
        '100::200::50'"""
        return self.trips_table[id]

    def list_all(self):
        """ Returns list of all trips.
        >>> [(k,v.in_line()) for k,v in gas.list_all()]
        [(0, '100::200::50'), (1, '150::200::70'), (3, '50::300::90'), (4, '300::500::220'), (5, '230::550::360')]"""
        return [(key, val) for key, val in self.trips_table.items()]

    def list_trips_between_dates(self, start_date, final_date, strict=False):
        """ Returns list of all trips between two dates.
        Args:
            start_date(time): minimal date.
            final_date(time): maximal date.
            strict(boolean): if false: trips with dates
             equal to min or max date would be listed.
        >>> [k for k,v in gas.list_trips_between_dates(150, 180)]
        [0, 1, 3, 4, 5]
        >>> [k for k,v in gas.list_trips_between_dates(140, 250, True)]
        [1]"""
        if strict:
            return [(key, val) for key, val in self.trips_table.items()
                    if (val.start_date > start_date and
                        val.end_date < final_date)]
        else:
            return [(key, val) for key, val in self.trips_table.items()
                    if ((val.end_date >= start_date) or
                        (final_date >= val.start_date))]

    def list_trips_after_date(self, date, strict=False):
        """ Return list of all trips after particular date.
        Args:
            date(time): minimal date of trip.
            strict(boolean): if false: trips with dates
             equal to minimal date would be listed.
        >>> [k for k,v in gas.list_trips_after_date(250)]
        [3, 4, 5]
        >>> [k for k,v in gas.list_trips_after_date(250, True)]
        [4]"""
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
             equal to maximal date would be listed.
        >>> [k for k,v in gas.list_trips_before_date(300)]
        [0, 1, 3, 4, 5]
        >>> [k for k,v in gas.list_trips_before_date(300, True)]
        [0, 1]"""
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
            date(time):Date of required trips.
        >>> [k for k,v in gas.search_trips_by_date(10)]
        []
        >>> [k for k,v in gas.search_trips_by_date(400)]
        []"""
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
             equal to min or max date would be added to sum.
        >>> gas.calculate_gasoline_between_dates(150, 250)
        870
        >>> gas.calculate_gasoline_between_dates(140, 250, True)
        150"""
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
             equal to minimal date would be added to sum.
        >>> gas.calculate_gasoline_after_date(250)
        670
        >>> gas.calculate_gasoline_after_date(250, True)
        220"""
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
                equal to maximal date would be added to sum.
        >>> gas.calculate_gasoline_before_date(300)
        870
        >>> gas.calculate_gasoline_before_date(300, True)
        200"""
        res = 0
        for i in self.list_trips_before_date(date, strict):
            res += i[1].fuel
        return res

    def delete(self, name=None):
        """Deletes a current table if name not spesified,
        or deletes a table srom storageby name
        Args:
            name:Name of table to delete.
        >>> gas.delete("some_name")
        False"""
        if name is None:
            self.__loaded = False
            name = (self.__current_table_name if self.__new_table_name
                    is None else self.__new_table_name)
            sr.delete(name, self.__serialize)
            self.trips_table = None
            self.trips_ids = 0
            return True
        else:
            return sr.delete(name, self.__serialize)

if __name__ == "__main__":
    doctest.testmod(extraglobs={"gas": GasolineTable(test=True)})
