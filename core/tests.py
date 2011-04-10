"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from core.models import *

__test__ = {"doctest":
"""
# Create a user, make some changes, save, add phone numbers
>>> john = UserProfile.objects.create_user('JohnDoe', 'John@doe.com')
>>> john.user.set_password('NULLandVOID')
>>> john.notes = 'An alright guy'
>>> john.save()
>>> Phone(userprofile=john, number=34565675).save()

# Confirm data
>>> uid = john.user.pk
>>> User.objects.get(pk=uid).username
u'JohnDoe'
>>> User.objects.get(pk=uid).password == john.user.password
True
>>> Phone.objects.get(userprofile=john).userprofile.user.username
u'JohnDoe'
>>> Phone.objects.get(userprofile=john).number
u'34565675'

# Delete and confirm actions
>>> john.delete()
>>> User.objects.filter(pk=uid)
[]
>>> Phone.objects.filter(userprofile=john)
[]
"""}
