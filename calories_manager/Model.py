from User import User
from Product import Product


class Model():

    def __init__(self):
        """ Initialize Model class """
        super().__init__()

    @property
    def show_user(self):
        """ Show user """
        return list(User.select())

    @property
    def products(self):
        """ Return all items in the database """
        return list(Product.select())
