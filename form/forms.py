from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username*', 'type': 'text'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email*', 'type': 'email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password*', 'type': 'password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*', 'type': 'password'})
    )

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']