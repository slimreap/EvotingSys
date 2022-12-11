
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name="public"
urlpatterns = [

    path('signup', views.Signup, name="signup"),
    path('home/logout', auth_views.LogoutView.as_view(), name="logout"),
    path('', views.home, name="home"),
]
