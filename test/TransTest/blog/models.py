from django.db import models
import uuid

class UserPong(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	Name = models.CharField()
	Age = models.CharField()
	date = models.DateField(auto_now = True)

	def __str__(self):
		return self.Name