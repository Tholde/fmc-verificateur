from django.db import models


# Create your models here.
class User(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=250)
    contact = models.CharField(max_length=15)
    role = models.CharField(max_length=50)  # verificator or treasure
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname