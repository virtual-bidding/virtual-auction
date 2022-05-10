from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("rzp_payment", views.order_payment, name="rzp_payment"),
    path("callback", views.callback, name="callback"),
]