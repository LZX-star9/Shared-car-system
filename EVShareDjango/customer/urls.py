from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [

    path('', views.index, name='index'),

    path('rent_vehicle',views.rent_vehicle,name='rent_vehicle'),

    path('return_vehicle',views.return_vehicle,name='return_vehicle'),

    path('report_problem',views.report_problem,name='report_problem')
]