from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_demo, name='base-api'),
]