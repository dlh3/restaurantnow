from django.db.models.signals import post_save
from core.models import *

"""
Called when a Model object is saved.

If the Model is a User which is being created, create a UserProfile if necessary.
"""
def sigCreateUser(**kwargs):
    if kwargs['created'] and str(type(kwargs['instance'])) == str(type(User())):
        try:
            kwargs['instance'].get_profile()
        except UserProfile.DoesNotExist:
            UserProfile(user=kwargs['instance']).save()


post_save.connect(sigCreateUser)
