from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from core.models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')
    ordering = ['-is_superuser', 'is_staff', 'is_active', 'id']

class PhoneAdmin(admin.ModelAdmin):
    model = Phone
    fk_name = 'user'
    fields = []
    for field in Phone._meta.fields:
        fields.append(field.name)
    fields.remove('id')
    list_display = tuple(fields)
    #list_display = ('user','description', 'number')
    #fields = ['user', 'description', 'number']
    list_filter = ['description']
    search_fields = ['number', 'user__username']

class AddressAdmin(admin.ModelAdmin):
    model = Address
    fk_name = 'user'
    fields = []
    for field in Address._meta.fields:
        fields.append(field.name)
    fields.remove('id')
    list_display = tuple(fields)
    list_filter = ['description']
    #search_fields = ['Address1', 'user__username']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fields = ['description']
    display = ('description')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(PhoneCategory)
admin.site.register(Address, AddressAdmin)
admin.site.register(AddressCategory)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Order)