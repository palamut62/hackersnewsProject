from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ExtendedUserCreationForm
from .models import User



def signup_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = ExtendedUserCreationForm(request.POST)
    return render(request, 'Login/signup.html', {'form': form})

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or password is incorrect.')
            return redirect('login')

    return render(request, 'Login/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

from .forms import UserProfileForm

@method_decorator(login_required, name='dispatch')
class profile_view(View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'Login/profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        return render(request, 'Login/profile.html', {'form': form})


from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomPasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'Login/change_password.html', {'form': form})