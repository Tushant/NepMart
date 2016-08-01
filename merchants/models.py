from django.db import models
# from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# User = get_user_model()

class Merchant(models.Model):
	user = models.ForeignKey(User)
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return str(self.user)

	# def get_absolute_url(self):
	# 	return reverse('products:merchant_detail', kwargs={"merchant name":self.user.username})
