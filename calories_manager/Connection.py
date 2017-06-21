""" Module that provides conn object for the model """

import os
import sqlobject
from configuration.configParser import *

def establish_connection():
    """ Connect to the database """
    res_dict = config_parser_result()
    conn = None
    if res_dict[save_type_key] == "mysql":
        connection_str = "mysql://root:password@127.0.0.1/testdb"
        conn = sqlobject.connectionForURI(connection_str)
    elif res_dict[save_type_key] == "sqll":
        connection_str = "sqlite:" + os.path.abspath("mdata.db")
        conn = sqlobject.connectionForURI(connection_str)
    elif res_dict[save_type_key] == "psql":
        connection_str = "mysql://test:www@127.0.0.1/sammy"
        conn = sqlobject.connectionForURI(connection_str)
    return conn