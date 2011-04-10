from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django import forms
from project import locale
from logging import debug as log
import logging
import re
logging.basicConfig(filename='snort.coke',level=logging.DEBUG)

#Managers
class UserProfileManager(models.Manager):
    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        profile = UserProfile(user=user)
        profile.save()
        return profile

#Phone Number Category extension
class PhoneCategory(models.Model):
    description = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural='Phone Categories'
    def __unicode__(self):
        return self.description

#Phone Number UserProfile extenstion
class Phone(models.Model):
    user = models.ForeignKey(User)
    description = models.ForeignKey(PhoneCategory)
    number = models.CharField(max_length=20, default=locale['PHONE_NUMBER'])
    class Meta:
        verbose_name_plural='Phone Numbers'

    def __unicode__(self):
        return str(self.id)

    def clean(self):
        cleaned_data = {}
        pattern = re.compile(r'^\s*(1)?[\s.-]?\(?(\d{3})?\)?[\s.-]?(\d{3})[\s.-]?(\d{4})\s*$')
        cleaned_data['number'] = ''
        match = pattern.match(self.number)
        if match is None:
            raise ValidationError('Enter a 10 or 11 digit phone number (XXX-XXX-XXXX)')

        if match.group(1) is not None:
            cleaned_data['number'] = cleaned_data['number'] + str(match.group(1))
        if match.group(2) is not None:
            cleaned_data['number'] = cleaned_data['number'] + str(match.group(2))
        else:
            raise ValidationError('Please include your area code')
        cleaned_data['number'] = cleaned_data['number'] + str(match.group(3)) + str(match.group(4))
        self.cleaned_data = cleaned_data

#Address Category extension
class AddressCategory(models.Model):
    description = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural='Address Categories'
    def __unicode__(self):
        return self.description

#Address UserProfile extention
class Address(models.Model):
    user = models.ForeignKey(User)
    description = models.ForeignKey(AddressCategory)
    address1 = models.CharField(max_length=30, default=locale['ADDRESS_LINE1'])
    address2 = models.CharField(max_length=30, default=locale['ADDRESS_LINE2'], blank=True, null=True)
    buzzcode = models.CharField(max_length=30, blank=True, null=True, default=locale['ADDRESS_BUZZCODE'])
    city = models.CharField(max_length=30, default=locale['ADDRESS_CITY'])
    state = models.CharField(max_length=30, default=locale['ADDRESS_STATE'])
    country = models.CharField(max_length=30, default=locale['ADDRESS_COUNTRY'])
    postalcode = models.CharField(max_length=30, default=locale['ADDRESS_POSTALCODE'], blank=True, null=True)
    drivernotes = models.CharField(max_length=30,blank=True, null=True, default=locale['ADDRESS_DRIVERNOTES'])
    class Meta:
        verbose_name_plural='Addresses'
    def __unicode__(self):
        return u"%s" % (self.description)

    def clean(self):
        try:
            if len(self.address1) == 0:
                raise ValueError
            elif len(self.city) == 0:
                raise ValueError
            elif len(self.state) == 0:
                raise ValueError
            elif len(self.country) == 0:
                raise ValueError
            elif len(self.postalcode) == 0:
                raise ValueError
        except ValueError:
            raise ValidationError('Invalid Address')

#UserProfile User extension
class UserProfile(models.Model):
    objects = UserProfileManager()
    user = models.ForeignKey(User, primary_key=True)
    notes = models.TextField(blank=True, default=locale['USERPROFILE_NOTES'])

    def save(self, *args, **kwargs):
        self.user.save()
        super(UserProfile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.delete()
        Phone.objects.filter(userprofile=self).delete()
        Address.objects.filter(userprofile=self).delete()
        super(UserProfile, self).delete(*args, **kwargs)
    def __unicode__(self):
        return u"%s" % (self.user)

class Category(models.Model):
    description = models.CharField(max_length=30, default=locale['CATEGORY_DESCRIPTION'])
    class Meta:
        verbose_name_plural='Categories'

    def __unicode__(self):
        return self.description

class Menu(models.Model):
    description = models.CharField(max_length=30, default=locale['MENU_DESCRIPTION'])
    category = models.ForeignKey(Category)
    taxcode = models.IntegerField(default=locale['MENU_TAXCODE'])
    image = models.ImageField(upload_to='food', default=locale['MENU_IMAGE'], blank=True, null=True)

    def __unicode__(self):
        return self.description

class MenuItem(models.Model):
    item = models.ForeignKey(Menu)
    size = models.CharField(max_length=30, default=locale['MENUITEM_SIZE'])
    price = models.DecimalField(max_digits=5, decimal_places=2, default=locale['MENUITEM_PRICE'])
    available = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    extratext = models.CharField(max_length=300, default=locale['MENUITEM_EXTRATEXT'])

    def __unicode__(self):
        return self.item.description + '(' + self.extratext + ')'

class Order(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    address = models.ForeignKey(Address, blank=True, null=True)
    phone = models.ForeignKey(Phone, blank=True, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    def addItem(self, item, quantity):
        OrderItem(order=self, item_id=item, quantity=quantity).save()
        self.total = self.total + (MenuItem.objects.get(id=item).price * quantity)
        self.save()
        return self
    def __unicode__(self):
        return str(self.id)

class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem)
    order = models.ForeignKey(Order)
    quantity = models.IntegerField(default=1)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user','address','phone','completed')

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'notes')

class NewUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username')
