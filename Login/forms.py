from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)



    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',  'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'last_name']


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(SetPasswordForm):
    old_password = None  # Bu, formda eski şifre alanını gizler

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']