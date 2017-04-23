from gas_accounting import business_logic
from gas_accounting import utils


class Controller:

    def __init__(self):
        self.table = business_logic.GasolineTable()

    def __del__(self):
        del self.table

    @staticmethod
    def args_test(pars, count1, args, count2):
        return (count1[0] <= len(pars) <= count1[-1] and
                count2[0] <= len(args) <= count2[-1])

    @staticmethod
    def pars_test(pars, expected):
        if not len(pars) <= len(expected):
            return False
        for i in pars:
            if i not in expected:
                return False
        return True

    @staticmethod
    def gen_string(lst):
        str = ""
        for i in lst:
            str += "id:{} {}\n".format(i[0], i[1].get_print())
        return str

    def search_command(self, pars, args):
        if len(pars) > 0:
            return "Invalid parameters"
        if len(args) < 1 or len(args) > 2:
            return "Invalid arguments"
        if len(args) == 1:
            date = utils.parse_time(args[0])
        else:
            date = utils.parse_time_with_format(args[1])
        res = self.table.search_trips_by_date(date)
        return self.gen_string(res)

    def list_command(self, pars, args):
        if not self.args_test(pars, [0, 2], args, [1, 2]):
            return "Invalid amount of parameters."
        if not self.pars_test(pars, ["s", "a", "b"]):
            return "Invalid parameters."
        if len(args) == 1 and args[0] == "all":
            return self.gen_string(self.table.list_all())
        if "s" in pars:
            strict = True
        else:
            strict = False
        if "a" in pars and "b" not in pars:
            res = self.table.list_trips_after_date(utils.parse_time(args[0]), strict)
        elif "b" in pars and "a" not in pars:
            res = self.table.list_trips_before_date(utils.parse_time(args[0]), strict)
        elif "a" not in pars and "b" not in pars and len(args) == 2:
            res = self.table.list_trips_between_dates(utils.parse_time(args[0]),
                                                      utils.parse_time(args[1]))
        else:
            return "Invalid arguments."

        return self.gen_string(res)

    def add_command(self, pars, args):
        # raise NotImplementedError

        if not self.args_test(pars, [0, 1], args, [2, 3]):
            return "Invalid amount of parameters."
        if not self.pars_test(pars, ["c"]):
            return "Invalid parameters."
        if "c" in pars:
            self.table.add_trip_consumption(utils.parse_time(args[2]),
                                            utils.parse_time(args[-1]),
                                            float(args[0]), float(args[1]))
        else:
            id = self.table.add_trip(utils.parse_time(args[1]),
                                utils.parse_time(args[-1]), float(args[0]))
        return "{} \nAdded.".format(self.table.trips_table[id].get_print())

    def delete_command(self, pars, args):
        return 1

    def process_console_request(self, command, modifiers, parameters):
        if command.lower() == "search":
            return self.search_command(modifiers, parameters)
        elif command.lower() == "list":
            return self.list_command(modifiers, parameters)
        elif command.lower() == "add":
            return self.add_command(modifiers, parameters)
        elif command.lower() == "delete":
            return self.delete_command(modifiers, parameters)
        else:
            return "Invalid command: {}".format(command)


