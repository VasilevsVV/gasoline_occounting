from gas_accounting import business_logic


def search_command(mods, args):
    return 1


def list_command(mods, args):
    return 1


def add_command(mods, args):
    return 1


def delete_command(mods, args):
    return 1


def process_console_request(command, modifiers, parameters):
    if command.lower() == "search":
        return search_command(modifiers, parameters)
    else:
        return "Invalid command: {}".format(command)


