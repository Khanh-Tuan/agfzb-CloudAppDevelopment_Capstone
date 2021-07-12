from django.db import models
from django.utils.timezone import now
from django.conf import settings
import uuid
import sys

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False,max_length=1000)
    description = models.CharField(max_length=3000)
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False,max_length=1000)
    dealer_id = models.IntegerField()
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    type_choices = [(SEDAN, 'Sedan'),(SUV, 'SUV'),(WAGON, 'Wagon'),(HATCHBACK, 'Hatchback')]
    car_type = models.CharField(null=False,choices=type_choices,max_length=1000)
    year = models.DateField()
    def __str__(self):
        return "Name: " + self.name + ", " + "Type: " + self.car_type + ', ' + 'Year: ' + self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):    
    city = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    st = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    zipcode = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    short_name = models.CharField(max_length=1000)
    full_name = models.CharField(max_length=1000)

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    name = models.CharField(max_length=1000)
    dealer_id = models.IntegerField()
    review = models.CharField(max_length=3000)
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    carmake = models.CharField(max_length=1000)
    carmodel = models.CharField(max_length=1000)
    car_year = models.DateField()
