from sqlobject import *
from Connection import *

class Book(SQLObject):
    _connection = establish_connection()
    bookName = StringCol(length=100, unique=True)
    bookAuthor = StringCol(length=100)
    bookYear = IntCol(default=None)
    bookRate = StringCol(default="")
    user = ForeignKey('User', default=None)

    def __repr__(self):
        return "name = '{0}', author = '{1}'".format(self.bookName, self.bookAuthor)

Book.createTable(ifNotExists=True)