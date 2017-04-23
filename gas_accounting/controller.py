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
        str = ""
        for i in res:
            str += "id:{} {}".format(i[0], i[1].get_print())
        return str

    def list_command(self, pars, args):
        return 1

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
            self.table.add_trip(utils.parse_time(args[1]),
                                utils.parse_time(args[-1]), float(args[0]))
        return 0

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


