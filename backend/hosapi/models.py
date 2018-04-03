from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import datetime

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
class Hospuser(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	email = models.EmailField(max_length=120)
	username = models.CharField(max_length=120, unique=True)

	ROLE = (
		('Subject editor','subject editor'),
		('Sample editor','sample editor'),
		('Admin','admin'),
		)

	role = models.CharField(
		max_length=30,
		choices = ROLE,
		default = 'subject editor'
		)

	def __str__(self):
		return self.username

class Subject(models.Model):
	# id
	created_id = models.CharField(max_length=120, unique=True)
	subject_code = models.CharField(max_length=120)
	create_date = models.DateTimeField(blank=True)

	BLOOD_TYPE = (
		('A+','a+'),
		('A-','a-'),
		('B+','b+'),
		('B-','b-'),
		('O','o'),
		('AB+','ab+')
		)

	blood_type = models.CharField(
		max_length=30,
		choices = BLOOD_TYPE,
		default = 'None'
		)

	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.subject_code


class Cancertype(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Sample(models.Model):
 	subject = models.ForeignKey('Subject', on_delete=models.CASCADE,)
 	cancer = models.ManyToManyField(Cancertype)

 	def __str__(self):
 		return str(self.subject_id)