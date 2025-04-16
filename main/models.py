from django.db import models
from django.contrib.auth.models import User
from .brand_models import MODELS_BY_BRAND

BRAND_CHOICES = [
    ("Audi", "Audi"),
    ("BMW", "BMW"),
    ("Lamborghini", "Lamborghini"),
    ("Mercedes", "Mercedes"),
    ("Ford", "Ford"),
    ("Toyota", "Toyota"),
    ("Volkswagen", "Volkswagen"),
    ("Opel", "Opel"),
    ("Renault", "Renault"),
    ("Peugeot", "Peugeot"),
    ("Hyundai", "Hyundai"),
]
CAR_BODY_CHOICES = [
    ("Sedan", "Sedan"),
    ("SUV", "SUV"),
    ("Hatchback", "Hatchback"),
    ("Coupe", "Coupe"),
    ("Cabrio", "Cabrio"),
    ("Pickup", "Pickup"),
    ("Break", "Break"),
    ("Minivan", "Minivan"),
    ("Sport", "Sport"),
]

TRANSMISSION_CHOICES = [
    ('Manuală', 'Manuală'),
    ('Automată', 'Automată'),
]

BRAND_CHOICES = [(brand, brand) for brand in MODELS_BY_BRAND.keys()]

ALL_MODEL_CHOICES = [(model, model) for models_list in MODELS_BY_BRAND.values() for model in models_list]

class Car(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField(max_length=50, choices=ALL_MODEL_CHOICES)
    year = models.IntegerField(default=2020)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField()
    engine = models.CharField(max_length=100)
    horsepower = models.IntegerField()
    engine_capacity = models.IntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=20)
    car_body = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Manuală')
    main_image = models.ImageField(upload_to='car_images/')
    images = models.ManyToManyField('CarImage', blank=True, related_name="car_images")

    featured = models.BooleanField(default=False)  # Pentru anunțul zilei (home)
    premium = models.BooleanField(default=False)  # Pentru badge + top în ads

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="extra_images")
    image = models.ImageField(upload_to='car_images/')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    favorites = models.ManyToManyField('Car', blank=True, related_name='favorited_by')

    def __str__(self):
        return self.user.username
