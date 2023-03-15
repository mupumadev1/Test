# forms.py

from django import forms

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'class': 'col-md-4 col-form-label','disabled': True }))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'new-password'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'confirm-password'}))
