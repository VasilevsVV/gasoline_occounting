from gas_accounting import business_logic
from gas_accounting import utils

class Controller:

    def __init__(self):
        self.table = business_logic.GasolineTable()

    def search_command(self, mods, args):
        if len(mods) > 0:
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

    def list_command(self, mods, args):
        return 1

    def add_command(self, mods, args):
        return 1

    def delete_command(self, mods, args):
        return 1

    def process_console_request(self, command, modifiers, parameters):
        if command.lower() == "search":
            return search_command(modifiers, parameters)
        elif command.lower() == "list":
            return list_command(modifiers, parameters)
        elif command.lower() == "add":
            return add_command(modifiers, parameters)
        elif command.lower() == "delete":
            return delete_command(modifiers, parameters)
        else:
            return "Invalid command: {}".format(command)


