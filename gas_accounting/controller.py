from business_logic import GasolineTable
import utils


class Controller:

    def __init__(self):
        self.table = GasolineTable()

    def __del__(self):
        del self.table

    @staticmethod
    def args_test(pars, count1, args, count2):
        """Tests parameters and arguments for
        lengths validness."""
        return (count1[0] <= len(pars) <= count1[-1] and
                count2[0] <= len(args) <= count2[-1])

    @staticmethod
    def pars_test(pars, expected):
        """Tests parameters for validness.
        Args:
            pars:Parameters
            expected:Expected parameters."""
        if not len(pars) <= len(expected):
            return False
        for i in pars:
            if i not in expected:
                return False
        return True

    @staticmethod
    def test(pars, count1, args, count2, expected):
        """Makes all tests on parameters and arguments."""
        if not Controller.args_test(pars, count1, args, count2):
            return "Invalid amount of parameters."
        elif not Controller.pars_test(pars, expected):
            return "Invalid parameters."
        return False

    @staticmethod
    def gen_string(lst):
        """Makes a string from result."""
        str = ""
        for i in lst:
            str += "id:{} {}\n".format(i[0], i[1].get_print())
        return str

    def search_command(self, pars, args):
        """Command for search trip in table."""
        test = self.test(pars, [0], args, [1, 2], [])
        if test:
            return test
        if len(args) == 1:
            date = utils.parse_time(args[0])
        else:
            date = utils.parse_time_with_format(args[0], args[1])
        res = self.table.search_trips_by_date(date)
        return self.gen_string(res)

    def list_command(self, pars, args):
        """Command for list trips from table."""
        test = self.test(pars, [0, 2], args, [1, 2], ["s", "a", "b"])
        if test:
            return test
        if len(args) == 1 and args[0] == "all":
            return self.gen_string(self.table.list_all())
        strict = True if 's' in pars else False
        if "a" in pars and "b" not in pars:
            res = self.table.list_trips_after_date(utils.parse_time(args[0]),
                                                   strict)
        elif "b" in pars and "a" not in pars:
            res = self.table.list_trips_before_date(utils.parse_time(args[0]),
                                                    strict)
        elif "a" not in pars and "b" not in pars and len(args) == 2:
            res = self.table.list_trips_between_dates(
                utils.parse_time(args[0]),
                utils.parse_time(args[1]))
        else:
            return "Invalid arguments."
        return self.gen_string(res)

    def add_command(self, pars, args):
        """Command for adding trip to table"""
        test = self.test(pars, [0, 1], args, [2, 3], ["c"])
        if test:
            return test
        if "c" in pars:
            id = self.table.add_trip_consumption(utils.parse_time(args[2]),
                                                 utils.parse_time(args[-1]),
                                                 float(args[0]), float(args[1]))
        else:
            id = self.table.add_trip(
                utils.parse_time(args[1]),
                utils.parse_time(args[-1]), float(args[0]))
        return "{} \nAdded.".format(self.table.trips_table[id].get_print())

    def delete_command(self, pars, args):
        """Command for deleting trip from table."""
        test = self.test(pars, [0], args, [1], [])
        if test:
            return test
        try:
            res = self.table.delete_trip(int(args[0]))
        except KeyError as e:
            return "There is no trip with id:{}".format(e)
        except Exception as e:
            return "{}".format(e)
        return "Deleted {}".format(res.get_print())

    def gas_command(self, pars, args):
        """Command for calculating spent gasoline."""
        test = self.test(pars, [0, 2], args, [1, 2], ["s", "a", "b"])
        if test:
            return test
        strict = True if 's' in pars else False
        if "a" in pars and "b" not in pars:
            res = self.table.calculate_gasoline_after_date(
                utils.parse_time(args[0]), strict)
        elif "b" in pars and "a" not in pars:
            res = self.table.calculate_gasoline_before_date(
                utils.parse_time(args[0]), strict)
        elif "a" not in pars and "b" not in pars and len(args) == 2:
            res = self.table.calculate_gasoline_between_dates(
                utils.parse_time(args[0]),
                utils.parse_time(args[1]), strict)
        else:
            return "Invalid arguments."
        return "Total gasoline: {}".format(res)

    def load(self, pars, args):
        """Command for loading some table."""
        test = self.test(pars, [0], args, [1], [])
        if test:
            return test
        if self.table.load(args[0]):
            return "Loaded"
        else:
            return "Created new"

    def dump(self, pars, args):
        """Command for dumping table."""
        test = self.test(pars, [0], args, [0], [])
        if test:
            return test
        return self.table.dump()

    def delete(self, pars, args):
        """Command for deleting table from storage."""
        test = self.test(pars, [0], args, [0, 1], [])
        if test:
            return test
        if len(args) == 1:
            self.table.delete(args[0])
            return "Table {} deleted".format(args[0])
        else:
            self.table.delete()
            return "Table deleted"

    def process_console_request(self, command, modifiers, parameters):
        """Processor of commands."""
        if command.lower() != "load" and not self.table.is_loaded():
            return "Table is not loaded!"
        try:
            if command.lower() == "search":
                return self.search_command(modifiers, parameters)
            elif command.lower() == "list":
                return self.list_command(modifiers, parameters)
            elif command.lower() == "add":
                return self.add_command(modifiers, parameters)
            else:
                return self.command_processor1(command, modifiers, parameters)
        except Exception as e:
            return "{}".format(e)

    def command_processor1(self, command, modifiers, parameters):
        if command.lower() == "delete":
            return self.delete_command(modifiers, parameters)
        elif command.lower() == "gas":
            return self.gas_command(modifiers, parameters)
        elif command.lower() == "load":
            return self.load(modifiers, parameters)
        else:
            return self.command_processor2(command, modifiers, parameters)

    def command_processor2(self, command, modifiers, parameters):
        if command.lower() == "dump":
            return self.dump(modifiers, parameters)
        elif command.lower() == "deltable":
            return self.delete(modifiers, parameters)
        else:
            return "Invalid command: {}".format(command)
