from django.db import models
from django.utils.timezone import now

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
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
        # Dealer Short Name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, id, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make 
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review + "/n" + "Sentiment: " + str(self.sentiment)

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=60)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=60)

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    MINIVAN = 'minivan'
    PICKUP_TRUCK = 'pickup'
    SUPERCAR = 'supercar'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Station Wagon'),
        (HATCHBACK, 'Hatchback'),
        (MINIVAN, 'Minivan'),
        (PICKUP_TRUCK, 'Pickup Truck'),
        (SUPERCAR, 'Supercar')
    ]

    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=CAR_TYPE_CHOICES,
        default=SUPERCAR
    )

    year = models.DateField(null=False)
    
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
