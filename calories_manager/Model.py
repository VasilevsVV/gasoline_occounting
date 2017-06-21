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

    def detailed_info(self, day):
        date = "{}-{}-{}".format(day['year'], day['month'], day['day'])
        items = Product.select(Product.q.date == date)
        total = self.total(day)
        return (items, total)

    def _query(self, kwargs):
        if len(kwargs) == 3:
            date = "{}-{}-{}".format(kwargs['year'], kwargs['month'], kwargs['day'])
            products = Product.select(Product.q.date == date)
        elif "month" in kwargs.keys() and "year" in kwargs.keys():
            prev_month = datetime.date(kwargs['year'], kwargs['month'], 1) - relativedelta(months=1)
            next_mounth = datetime.date(kwargs['year'], kwargs['month'], 1) + relativedelta(months=1)
            products = Product.select(sqlobject.AND(Product.q.date > prev_month,\
                                     Product.q.date < next_mounth))
        elif "year" in kwargs.keys():
            now = datetime.datetime.now()
            products = Product.select(sqlobject.AND(Product.q.date > datetime.date(kwargs['year'] -1, 12, 31),\
                                     Product.q.date < datetime.date(kwargs['year'] + 1, 1, 1)))
        return products

    def current_product_list(self):
        now = datetime.datetime.now()
        return self._query(dict((("year", now.year), ("month", now.month), ("day", now.day))))

    def total(self, kwargs):
        products = self._query(kwargs)
        if list(products) == []:
            raise Exception("Sorry, but you do not have such records.")
        return reduce(lambda x, y: x.energyPoints + y.energyPoints, products) if len(list(products)) > 1\
                                                                            else products[0].energyPoints

