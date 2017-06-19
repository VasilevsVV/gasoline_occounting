import json
import entities as en


class JsonSerialize:
    @staticmethod
    def encode_trip(trip):
        if type(trip) is en.Trip:
            return {"start_date": trip.start_date,
                    "end_date": trip.end_date,
                    "fuel": trip.fuel}
        else:
            raise Exception("ERROR: Invalid type of object {}"
                            .format(type(trip)))

    @staticmethod
    def decode_trip(dict_trip):
        if isinstance(dict_trip, dict):
            start_date = dict_trip.get("start_date", None)
            end_date = dict_trip.get("end_date", None)
            fuel = dict_trip.get("fuel", None)
            if None in [start_date, end_date, fuel]:
                raise Exception("ERROR: decode of trip failed: {}"
                                .format(dict_trip))
            else:
                trip = en.Trip(start_date, end_date)
                trip.set_fuel(fuel)
                return trip

    @staticmethod
    def decode_tables(tables):
        if type(tables) is dict:
            if "start_date" and "end_date" and "fuel" in tables.keys():
                return JsonSerialize.decode_trip(tables)
            else:
                return {JsonSerialize.decode_tables(k):
                        JsonSerialize.decode_tables(v)
                        for k, v in tables.items()}
        elif type(tables) is list:
            return [JsonSerialize.decode_tables(val) for val in tables]
        elif type(tables) is str:
            if tables.isdecimal():
                return int(tables)
            else:
                try:
                    return float(tables)
                except:
                    return tables
        else:
            return tables

    @staticmethod
    def dump(data, file):
        json.dump(data, file, default=JsonSerialize.encode_trip)

    @staticmethod
    def load(file):
        return JsonSerialize.decode_tables(json.load(file))
