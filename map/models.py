from django.db import models

# Create your models here.

AGE_CHOICES = (
    ('below 10','below 10'),
    ('10 - 20', '10 - 20'),
    ('21 - 30', '21 - 30'),
    ('31 - 40','31 - 40'),
    ('41 - 50','41 - 50'),
    ('51 - 60','51 - 60'),
    ('over 60','over 60'),
)

class Volunteer(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    age = models.CharField(max_length=10, choices=AGE_CHOICES)
    phone = models.IntegerField()
    city = models.CharField(max_length=20)
    pincode = models.IntegerField()

    
    def __str__(self):
        return f"{self.name}"

class Event(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    date = models.DateField()
    details = models.CharField(max_length=255)
    notify = models.BooleanField()
    
    def __str__(self):
        return f"{self.name}"