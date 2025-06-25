from django import forms
from .models import users_data

class users_data(forms.ModelForm):
    class Meta:
        model = users_data
        fields = ['user_name', 'user_email']
