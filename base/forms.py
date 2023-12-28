from django.forms import ModelForm
from .models import Room, User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    exclude = ['host', 'participants']

class NewUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['full_name', 'username', 'email', 'password1', 'password2']
  

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['full_name', 'username', 'email', 'avatar', 'bio']