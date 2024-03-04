from django.db import models

# Create your models here.
class Article(models.Model):
	title = models.CharField()
	date = models.DateField(auto_now = True)

	def __str__(self):
		return self.title