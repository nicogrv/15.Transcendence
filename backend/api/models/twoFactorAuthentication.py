import secrets, string
import os
import re

def isEmailValid(email):
	regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	if re.match(regex, email):
		return True
	return False

def isEmailAvailable(email):
	return True

def randomSlug(length):
	slug = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))
	return slug

def randomNumber(length):
	slug = ''.join(secrets.choice(string.digits) for i in range(length))
	return slug

def maxLength(lst):
	max_len = 0
	for item in lst:
		max_len = max(max_len, len(item))
	return max_len

def replaceVars(string, dictionary):
	def replace_variable(match):
		variable = match.group(1)
		return dictionary.get(variable, match.group(0))

	import re
	pattern = r'\${([^}]*)}'
	new_string = re.sub(pattern, replace_variable, string)
	return new_string

import os, mailjet_rest
from django.template.loader import render_to_string

class SendEmail():
	def send(self, **kwargs):
		kwargs = kwargs or {}
		if 'sender_name' not in kwargs:
			kwargs['sender_name'] = 'ft_transcendence'
		if 'sender_email' not in kwargs:
			kwargs['sender_email'] = 'ft_transcendence@titouanck.fr'

		try:
			html_data = render_to_string(kwargs['html_body'], kwargs)
		except Exception:
			html_data = None

		mailjet = mailjet_rest.Client(auth=(os.environ['MAILJET_API_KEY'], os.environ['MAILJET_API_SECRET']), version='v3.1')
		data = {
			'Messages': [
				{
					"From": {
						"Email": kwargs['sender_email'],
						"Name": kwargs['sender_name']
					},
					"To": [
						{
							"Email": kwargs.get('recipient_email', None),
							"Name": kwargs.get('recipient_name', None),
						}
					],
					"Subject": kwargs.get('email_subject', None),
					"TextPart": kwargs.get('plain_text', None),
					"HTMLPart": html_data

				}
			]
		}
		result = mailjet.send.create(data=data)
		return True if result and result.status_code == 200 else False

from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string
from uuid import uuid4
import os

from api.models.playerModel import Player

# **************************************************************************** #

LINK_LIFETIME = timezone.timedelta(hours=1)
STATUS_VALUES = ['DEFAULT', 'PENDING', 'SENT', 'COMPLETED', 'FAILED']

# **************************************************************************** #

def random_code():
	return randomNumber(length=8)

class TwoFactorAuthentication(models.Model, SendEmail):

	STATUS_VALUES = [
		('DEFAULT', 'Default'),
		('PENDING', 'Pending'),
		('SENT', 'Sent'),
		('COMPLETED', 'Completed'),
		('FAILED', 'Failed'),
	]

	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
	player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
	code = models.IntegerField(null=True, default=random_code)
	sended_at = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=60,default='DEFAULT',choices=STATUS_VALUES)
	
	def send(self, resend=False):
		if self.sended_at and not resend:
			return False
		if super().send(
			recipient_email=self.player.email, 
			recipient_name=self.player.username,
			email_subject=f'Your transcendence verification code: {self.code}',
			plain_text=f'{self.code} is your transcendence verification code.',
			html_body='emails/two_factor_authentification.html',

			verification_code_12=str(self.code)[0:2],
			verification_code_34=str(self.code)[2:4],
			verification_code_56=str(self.code)[4:6],
			verification_code_78=str(self.code)[6:8]
		):
			self.sended_at = timezone.now()

	def checkCode(self, code):
		try:
			if int(code) == int(self.code):
				return True
			return False
		except ValueError:
			return False
	
	def is_expired(self):
		if timezone.now() >= self.sended_at + LINK_LIFETIME:
			return True
		return False

	def save(self, *args, **kwargs):
		self.send()
		super(TwoFactorAuthentication, self).save(*args, **kwargs)

	def __str__(self):
		if self:
			return f"{self.player.username} ({self.code}) -> {self.uid}"
