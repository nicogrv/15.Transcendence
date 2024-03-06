from django.db import models

# Create your models here.
class Person(models.Model):
    username = models.SlugField(max_length=24)
    first_name = models.CharField(max_length=50)
    age = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def firstLetter(self):
        return self.username[:1]
