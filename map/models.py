from django.db import models

# Create your models here.
class Volunteer(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    age = models.IntegerField()
    phone = models.IntegerField()
    city = models.CharField(max_length=20)
    pincode = models.IntegerField()

    
    def __str__(self):
        return f"{self.name}"