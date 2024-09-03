from django.db import models

# Create your models here.


class Register(models.Model):
    description = models.TextField()
    date = models.DateField()
    value = models.FloatField()
    category = models.CharField(max_length=100)
    payment_form = models.CharField(max_length=100)

    def __str__(self):
        return self.description
