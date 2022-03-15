from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-weather/', get_weather),

]
