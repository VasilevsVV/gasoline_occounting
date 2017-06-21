from Connection import *

class Product(sqlobject.SQLObject):
    _connection = establish_connection()
    productName = sqlobject.StringCol(length=100)
    energyPoints = sqlobject.IntCol(default=None)
    # date = sqlobject.DateCol()
    date = sqlobject.StringCol()
    def __repr__(self):
        return "date: {} name = {}, energy = {}".format(self.date,\
                                                self.productName, self.energyPoints)

Product.createTable(ifNotExists=True)