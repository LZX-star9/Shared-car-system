from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path("", views.EVSlogin, name="login"),

    path("logout/", views.EVSlogout, name="logout"),

    path("register/", views.register, name="register"),

    path("captcha", views.send_captcha, name="email_captcha"),

    path('profile/', views.profile_view, name='profile'),

]