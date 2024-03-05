from django.db import models

# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    passwd = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name