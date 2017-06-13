#!/usr/bin/python3

import controller


def show_help(category):
    return 1


def parse_string(str):
    str = str.lstrip()
    lst = str.split()
    command = lst.pop(0)
    if lst and lst[0].startswith("-"):
        params_str = lst.pop(0)
        params = [ch for ch in params_str[1:len(str)]]
    else:
        params = []
    args = lst
    return [command, params, args]


def start_console():
    loop_flag = True
    c = controller.Controller()
    while loop_flag:
        str = input(" > ").strip()
        if str == "exit":
            del c
            loop_flag = False
        elif str != "":
            res = parse_string(str)
            print(c.process_console_request(res[0], res[1], res[2]))

# start_console()
