from django.urls import path, include
from django.contrib import admin
from . import views

app_name = "manager"

urlpatterns = [
    path("show/reports", views.show_reports, name="show_reports"),
    path('money-earned-per-location/', views.money_earned_per_location, name='money_earned_per_location'),
    path('cars-per-location/', views.cars_per_location, name='cars_per_location'),
    path('most-reported-broken-cars/', views.most_reported_broken_cars, name='most_reported_broken_cars'),
    path('most-used-rental-location/', views.most_used_rental_location, name='most_used_rental_location'),
    path('most-rented-vehicle-types/', views.most_rented_vehicle_types, name='most_rented_vehicle_types'),
]