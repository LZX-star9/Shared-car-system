from django.urls import path

from . import views

app_name = "operater"

urlpatterns = [
    path("add/location", views.add_location, name="add_location"),
    # path("delete/<int:id>", views.delete, name="delete")

    path("show/location", views.show_locations, name="show_location"),

    path("update/location", views.update_location, name="update_location"),

    path("delete/location/<int:location_id>", views.delete_location, name="delete_location"),

    path("add/vehicle", views.add_vehicle, name="add_vehicle"),

    path("show/vehicle", views.show_vehicle, name="show_vehicle"),

    path("vehicle/<ButtonName>/", views.button_function, name="function"),

    path("test", views.addtestdata),

    path("rent_logs/", views.show_rent_logs, name="show_rent_logs"),

    path("payment_logs/", views.show_payment, name="show_payment"),

    path("repair_logs/", views.show_repairlogs, name="show_repairlogs"),

]