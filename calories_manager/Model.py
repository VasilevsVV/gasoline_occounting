import datetime
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

    def setUp(self, name, age, height, weight, gender, actv):
        """ Set up user """
        if actv not in [1.2, 1.375, 1.55, 1.7, 1.9]:
            raise Exception("Activity should be one of these values: 1.2, 1.375, 1.55, 1.7, 1.9.")
        User(userName=name, age=age, height=height, weight=weight, gender=gender, activity=actv)


    def update_user_param(self, kwargs):
        """ Update user """
        if not self._is_user_exists():
            raise Exception("[ERROR]: You should set up user first.")
        user = User.get(1)
        user.userName = kwargs['userName'] if 'userName' in kwargs.keys() else user.userName
        user.age = kwargs['age'] if 'age' in kwargs.keys() else user.age
        user.height = kwargs['height'] if 'height' in kwargs.keys() else user.height
        user.weight = kwargs['weight'] if 'weight' in kwargs.keys() else user.weight
        user.gender = kwargs['gender'] if 'gender' in kwargs.keys() else user.gender
        user.activity = kwargs['activity'] if 'activity' in kwargs.keys() else user.activity


    def add_product(self, name, energy_points):
        """ add product to the database """
        now = datetime.datetime.now()
        date = "{}-{}-{}".format(now.year, now.month, now.day)
        Product(productName=name, energyPoints=energy_points, date=date)


    def remove_product(self, product_name):
        now = datetime.datetime.now()
        date = "{}-{}-{}".format(now.year, now.month, now.day)
        if not self._is_product_exists(product_name, date):
            raise Exception("[ERROR]::There is no item with shuch name.")

        item = Product.select(Product.q.productName == product_name)[0]
        Product.delete(item.id)
