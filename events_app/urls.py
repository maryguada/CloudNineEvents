from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('create_event', views.create_event),
    path('new_event', views.new_event),

]
