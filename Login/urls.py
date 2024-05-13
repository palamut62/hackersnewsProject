from django.urls import path
from . import views
from .views import profile_view

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', profile_view.as_view(), name='profile'),
    path('change_password/', views.change_password, name='change_password'),

]

