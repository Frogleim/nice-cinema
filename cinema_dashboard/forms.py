from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Room, Movie


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if password1.isdigit():
            raise ValidationError('Password must contain at least one non-numeric character')
        return password1

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'rows', 'columns']



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'poster', 'room', 'start_time', 'end_time', 'date']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }




