from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=250)
    contact = models.CharField(max_length=15)
    role = models.CharField(max_length=50)  # verificateur or treasure
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class Recap(models.Model):
    number = models.IntegerField(null=True)
    date = models.DateField(null=True)
    church = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=250, null=True)
    dimes = models.FloatField(null=True)
    total = models.FloatField(null=True)
    period = models.DateField(max_length=250, null=True)
    reference = models.CharField(max_length=250, null=True)
    datereg = models.DateField(null=True)
    montant = models.FloatField()
    ref = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)