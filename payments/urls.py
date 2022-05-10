from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("rzp_payment/<str:pid>", views.order_payment, name="rzp_payment"),
    path("callback/<str:pid>", views.callback, name="callback"),
]