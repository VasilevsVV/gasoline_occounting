import datetime
from View import View
from Model import Model
from random import *
'''Implemenation of Controller class'''

class Controller:
	''' The class is responsible for connection with
	bussiness logic and it represantation.
	'''

	def __init__(self, main_model):
		""" Initialize Model class
        Args:
            main_model(Model): The model stores the data 
            of the app
        """
		self.model = main_model
		super().__init__()

	def start(self):
		'''Method implement the main menu logic.'''
		self.set_up_user() # +
		mode = 0
		View.main_menu()

		while mode != 7:
			try: 
				mode = int(input("Choose option: "))
			except ValueError:
				View.wrong_option()
				mode = 0

			if mode == 1:
				#add product +
				self.create_product_manager()
				View.main_menu()
			elif mode == 2:
				#remove product +
				self.remove_product_manager()
				View.main_menu()
			elif mode == 3:
				#show detailed info
				self.detailed_info_manager()
				View.main_menu()
			elif mode == 4:
				#Show stat
				self.show_stat_manager()
				View.main_menu()
			elif mode == 5:
				#upd user +
				self.update_manager()
				View.main_menu()
			elif mode == 6:
				self.today_manager()
			elif mode == 7:
				View.exit_message()
			elif mode not in range(1, 8):
				View.main_menu()


	def set_up_user(self):
		if self.model.show_user == []:
			self.create_user_manager()



	def create_user_manager(self):
		'''Controller manager is responsible for create 
		user process.'''
		print("Hint: Activity coef must be one of those numbers 1.2, 1.375, 1.55, 1.7, 1.9")
		try:
			name = str(input("Enter user name: "))
			age = int(input("Enter your age: "))
			height = int(input("Enter your height in centimeters: "))
			weight = int(input("Enter your weight: "))
			gender = str(input("Enter your gender: "))
			if gender not in ["female", "male"]:
				raise ValueError
			activity = float(input("Enter activity coef.: "))
		except ValueError:
			View.wrong_input()
			return

		try:
			self.model.setUp(name, age, height, weight, gender, activity)
		except Exception as e:
			print (e)
			return

		View.success_user_create_message()
		return

#------------------------------------------under work-----------------------------------------------

	def update_manager(self):
		if self.model.show_user != []:
			View.print_user(self.model.show_user[0])
		choice = -1
		params_to_upd = dict()
		while choice != 0:
			View.update_user_menu()
			try:
				choice = int(input("Your choice: "))

				if choice == 1:
					params_to_upd['productName'] = str(input("New name: ")) 
				elif choice == 2:
					params_to_upd['age'] = int(input("New age: "))
				elif choice == 3:
					params_to_upd['height'] = str(input("New height: "))
				elif choice == 4:
					params_to_upd['weight'] = str(input("New weight: "))
				elif choice == 5:
					params_to_upd['gender'] = str(input("New gender: "))
				elif choice == 6:
					params_to_upd['activity'] = str(input("New activity: "))

			except ValueError:
				View.wrong_input()
				choice = -1

		try:
			self.model.update_user_param(params_to_upd)
		except Exception as e:
			print(e)


	def detailed_info_manager(self):
		View.detailed_info_menu()
		try:
			choice = int(input("Your choice: "))
			if choice not in [1, 2]:
				raise ValueError
		except ValueError:
			View.wrong_input()
			return

		if choice == 1:
			try:
				today = datetime.datetime.now()
				items, total = self.model.detailed_info(dict((("year", today.year),\
														("month", today.month), ("day", today.day))))
			except Exception as err:
				print(err)
				return 
		else:
			try:
				year = int(input("Year: "))
				month = int(input("Month: "))
				day = int(input("Day: "))
				items, total = self.model.detailed_info(dict((("year", year), ("month", month), ("day", day))))
			except Exception:
				View.wrong_input()
				return 
		View.print_products(items)
		print("Total: {}(calories)\nShould consume: {}(calories)".format(total, self.model.should_consume()))

	def show_stat_manager(self):
		View.statisics_menu()
		try:
			choice = int(input("Your choice: "))
			if choice not in range(1, 5):
				raise ValueError
		except ValueError:
			View.wrong_input()
			return
		
		if choice == 1:
			try:
				today = datetime.datetime.now()
				total = self.model.total(dict((("year", today.year),\
										("month", today.month), ("day", today.day))))
			except Exception as e:
				print(e)
				return 
		elif choice == 2:
			try:
				year = int(input("Year: "))
				month = int(input("Month: "))
				day = int(input("Day: "))
				total = self.model.total(dict((("year", year), ("month", month), ("day", day))))
			except Exception:
				View.wrong_input()
				return 
		elif choice == 3:
			try:
				year = int(input("Year: "))
				month = int(input("Month: "))
				total = self.model.total(dict((("year", year), ("month", month))))
			except Exception as e:
				print(e)
				#View.wrong_input()
				return 
		elif choice == 4:
			try:
				year = int(input("Year: "))
				total = self.model.total({"year": year})
			except ValueError as e:
				#View.wrong_input()
				print(e)
				return 

		View.print_stat(total, self.model.should_consume())

#---------------------------------------------------------------------------------------------------
	def create_product_manager(self):
		'''Method is responsbile for creating a book'''
		try:
			name = str(input("Enter product name: "))
			energy_points = int(input("Enter calories: "))
		except ValueError:
			View.wrong_input()
			return
		else:
			self.model.add_product(name, energy_points)
			View.success_product_create_message()


	def remove_product_manager(self):
		'''Method is responsbile for removing a product from the present items list.'''
		View.print_products(self.model.current_product_list())
		try:
			product_name = str(input("Enter product name: "))
		except ValueError:
			View.wrong_input()
			return

		try:
			self.model.remove_product(product_name)
		except Exception as e:
			print(e)
		

		

	def today_manager(self):
		View.print_products(self.model.current_product_list())
		today = datetime.datetime.now()
		try:
			total = self.model.total(dict((("year", today.year),\
										("month", today.month), ("day", today.day))))
		except Exception as e:
			print(e)
			return 
		View.print_stat(total, self.model.should_consume())

