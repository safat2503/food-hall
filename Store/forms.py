from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import MerchantDiscount


class CreateUserForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username','email', 'password1','password2', 'group']

class MerchantDiscountForm(forms.ModelForm):
    class Meta:
        model = MerchantDiscount
        fields = ['store', 'discount_percentage']