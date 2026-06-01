from django.urls import path
from analytics.views import hello_world

urlpatterns = [
    path("hello/", hello_world, name='hello_world'),
]