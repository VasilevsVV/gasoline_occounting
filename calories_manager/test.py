import sqlobject 
from sqlobject.sqlite import builder

conn = builder()('sqltest.db')

print (conn)