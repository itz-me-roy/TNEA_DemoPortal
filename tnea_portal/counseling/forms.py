from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, COMMUNITY_CHOICES, Branch


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    community = forms.ChoiceField(choices=COMMUNITY_CHOICES)
    phone = forms.CharField(max_length=15, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CutoffSearchForm(forms.Form):
    cutoff_mark = forms.DecimalField(label="Your cutoff mark (out of 200)", max_digits=6, decimal_places=2)
    community = forms.ChoiceField(choices=COMMUNITY_CHOICES)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, empty_label="All branches")