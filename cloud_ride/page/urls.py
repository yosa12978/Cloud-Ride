from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login/", views.loginn),
    path("logout/", views.logoutt),
    path("signup/", views.signup),
    path("search/", views.search),
    path("self/<name>/", views.self),
    path("self/<name>/upload", views.upload),
    path("self/<name>/delete/<id>", views.delete),
]