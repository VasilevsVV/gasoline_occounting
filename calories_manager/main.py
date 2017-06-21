from configuration.configParser import *

import Connection as cn

from Model import Model
from Controller import Controller

if __name__ == '__main__':
	result_dict = config_parser_result()

	model = Model()

	controller = Controller(model)

	controller.start()