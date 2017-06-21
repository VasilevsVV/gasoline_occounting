''' Constants for keys from parser dictionary result '''
save_type_key = 'save_type'
last_save_type = 'last_save_type'

def config_parser_result():
	''' If config is empty it full fils result of parser with default values '''
	dictionary_result = read_from_configs("config")

	if (bool(dictionary_result) == False):
		dictionary_result = {save_type_key: 'sqll'}

	return dictionary_result

def last_session_data_save(type_of_save):
	with open ("configuration/.lastSessionData", "w") as fl:
		fl.write(last_save_type + "=" + type_of_save)

def last_session_save_type():
	dictionary_result = read_from_configs(".lastSessionData")

	if (bool(dictionary_result) == False):
		dictionary_result = {last_save_type: 'sqll'}

	return dictionary_result[last_save_type]

def read_from_configs(file_name):
	result = {}
	delimiter = "="
	comment_delimiter = "#"
	with open("configuration/" + file_name, "r") as fl:
		for line in fl:
			''' Skip of line that was commented '''
			if (line[0] != comment_delimiter):
				separate_list = line.split(delimiter)
				result[separate_list[0]] = separate_list[1]
				break

	return result