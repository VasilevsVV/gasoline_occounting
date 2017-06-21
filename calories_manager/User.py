import sqlobject
from Connection import *

class User(sqlobject.SQLObject):
	_connection = establish_connection()
	userName = sqlobject.StringCol(length=100, unique=False)
	age = sqlobject.IntCol(default=None)
	height = sqlobject.IntCol(default=None)
	weight = sqlobject.IntCol(default=None)
	gender = sqlobject.StringCol(length=6)
	activity = sqlobject.FloatCol(default=None)

	def __repr__(self):
		return "name: {}\nage: {}\nheight: {}\nweight: {}\ngender: {}\nactv: {}".format(self.userName,\
												self.age, self.height, self.weight, self.gender, self.activity)

User.createTable(ifNotExists=True)