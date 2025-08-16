"""career_guide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view),
    path('addvechile',views.add_vehicle,name='addvechile'),
    path('vehicle-list',views.vehicle_list,name='vehicle_list'),
    path('add-equipment/',views.add_equipment, name='add_equipment'),
    path('equipment-list/<int:pk>/',views.equipment_list,name='equipment_list'),
    path('add-equipment/<int:pk>/',views.add_equipment,name='add_equipment'),
    path('delete-equipment/<int:pk>/',views.delete_equipment,name='delete_equipment'),
    path('bookvehicle/<int:pk>/',views.book_vehicle,name="book_vehicle"),
    path('view-bookings',views.view_bookings,name='view_bookings'),
    path('cancel-booking/<int:pk>/',views.cancel_booking,name="cancel_booking"),
    path('confirm-booking/<int:pk>/',views.confirm_booking,name='confirm_booking'),
    path('confirmed-list',views.confirm_list,name='confirm_list')
]

