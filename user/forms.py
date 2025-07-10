from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as BaseUserCreationForm
from .models import (User)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

class UserRegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
        
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email','phone_number', 'role', 'is_active', 'password']

