
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name="evoting"

urlpatterns = [
	
    path('mainad/', views.mainad, name="mainad"),
	path('mainvtr/', views.mainvtr, name="mainvtr"),

	path('castedvotes/', views.castedvotes, name="castedvotes"),
	path('candprf/', views.candprf, name="candprf"),
	path('dashboardad/', views.dashboardad, name="dashboardad"),
	path('dashboardvtr/', views.dashboardvtr, name="dashboardvtr"),
	path('castvote/', views.castvote, name="castvote"),
	path('admindashboard/', views.addcandidate, name="addcandidate"),
	path('admindashboard/update/<int:id>/', views.updateparty, name="updatepartylist"),
	path('admindashboard/delete/<int:id>/', views.deleteparty, name="deletepartylist"),
	#path('admindash/', views.candidatelookup, name="addpartylistncandidate"),
]