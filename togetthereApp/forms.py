from django import forms
from django.forms import ModelForm
from .models import *

class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['facebook_id', 'first_name', 'last_name','email', 'birthday']



class SPForm(ModelForm):
    class Meta:
         model = SP
         fields = ['name', 'desc', 'category', 'longitude',
                   'latitude', 'phone', 'discount', 'website']


class AddressForm(ModelForm):
    class Meta:
         model = Address
         fields = ['street_num', 'street', 'city']


#class EditSPForm(ModelForm):
#class RankSPForm(ModelForm):

class AddReviewForm(ModelForm):
    class Meta:
         model = Review
         fields = ['title', 'content', 'user']