# from django.test import TestCase

# Create your tests here.
import datetime

dat = datetime.datetime
my_date = dat.strptime("20.06.2017 15:15:15", "%d.%m.%Y %H:%M:%S")
print(my_date)