"""Implementation of View class."""


class View:
	"""The class is responsible for information output.
	Class consist of static methods, due to the absent
	of it initialization.
	"""

	@staticmethod
	def separator_line():
		print ("\n|-----------------------------------------------|\n")


	@staticmethod
	def main_menu():
		View.separator_line()
		print ("Enter a number to choose the option")
		print ("1. Add product.")
		print ("2. Remove product.")
		print ("3. Show detailed info.")
		print ("4. Show statisics.")
		print ("5. Update user info.")
		print ("6. Show current list")
		print ("7. Exit.")
		View.separator_line()

	@staticmethod
	def user_create():
		View.separator_line()
		print ("Enter the information about new user\n.")


	@staticmethod
	def add_product():
		View.separator_line()
		print ("Enter the information about product\n.")


	@staticmethod
	def print_user(user):
		View.separator_line()
		print(user)


	@staticmethod
	def print_products(product_list):
		View.separator_line()
		for i in range(0, product_list.count()):
			product = product_list[i]
			print ("{}. {}".format(i + 1, product))
		View.separator_line()


	def update_user_menu():
		View.separator_line()
		print("Enter a number to choose quality for update:")
		print("1. Name")
		print("2. Age")
		print("3. Height")
		print("4. Weight")
		print("5. gender")
		print("6. Activity")
		print("0. Exit")


	def detailed_info_menu():
		View.separator_line()
		print("1. Today")
		print("2. Particular day")


	def statisics_menu():
		View.separator_line()
		print("1. Today")
		print("2. Particular day")
		print("3. Month statistic")
		print("4. Year statistic")


	def print_stat(total, norm):
		print("Total: {}(calories) Should consume: {}(calories)".format(total, norm))


	@staticmethod
	def success_user_create_message():
		print ("The user created successfully")


	@staticmethod
	def success_product_create_message():
		print ("The product added successfully")


	@staticmethod
	def wrong_input():
		print ("The input is invalid")


	@staticmethod
	def wrong_option():
		print ("No current option.")


	@staticmethod
	def exit_message():
		print ("See you!")
