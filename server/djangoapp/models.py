from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
# - Name
    make_name = models.CharField(max_length=300, default="name")
# - Description
    make_description = models.CharField(max_length=1000, default="description")
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
    def __str__(self):
        return self.make_name + ' ' + self.make_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):

# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
# - Name
    model_name = models.CharField(max_length=300, default="model")
# - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    choices = (("sedan", "Sedan"), ("suv", "SUV"), ("wagon", "Wagon"))
    model_type = models.CharField(max_length=6, choices=choices, default="type")
# - Year (DateField)
    model_year = models.DateField()
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
    def __str__(self):
        return self.model_name + ' ' + self.car_make + ' ' + self.model_type + ' ' + self.model_year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:


    def __init__(self, address, city, full_name, short_name, id, lat, long, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
