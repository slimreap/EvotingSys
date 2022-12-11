
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name="accounts"

urlpatterns = [

    path('login', views.LoginUser, name='login'),
	path('voterprf/update', views.UpdateUserProf, name="myprofile_update"),
	path('adminprf/', views.adminprf, name="adminprf"),
	path('voterprf/', views.UserProf, name="regvoterprf"),
	path('changepad/', views.changepadvtr, name="changepad"),
	path('changepadvtr/', views.changepadvtr, name="changepadvtr"),

	#path('admindash/', views.candidatelookup, name="addpartylistncandidate"),
]